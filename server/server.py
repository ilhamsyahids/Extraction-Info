#!flask/bin/python
import re
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from algorithm import *
from regex import *

app = Flask(__name__)

# CORS
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'])
def welcome():
    return 'It\'s Works!', 200

@app.route('/', methods=['POST'])
def searchPattern():

    # Validate request
    if (not request.json 
        or not 'algorithm' in request.json
        or not 'keyword' in request.json
        or not 'files' in request.json
        or not request.json['keyword']
        or not request.json['algorithm']
        or not request.json['files']
        ):
        abort(400)

    res = []
    for file in request.json['files']:
        el = {
            'filename': file['name'],
            'text': []
        }
        allText = '\n'.join(file['text'])
        date_file = ""
        numbers_file = ""
        match_date = matcher(date_regex(), allText)
        if match_date:
            date_file = match_date.group(0)
        match_numbers = matcher(numbers_regex(), allText)
        if match_numbers:
            numbers_file = match_numbers.group(1)
        for paragraph in file['text']:
            # Split into sentences
            sentences = re.compile(sentences_regex(), flags=re.UNICODE).split(paragraph)
            for txt in sentences:
                # Apply algorithm
                if request.json['algorithm'] == 'Regex':
                    res_regex = searchRegex(request.json['keyword'], txt)
                    if len(res_regex) != 0:
                        res.append(allGroup(file['name'], date_file, numbers_file, txt, res_regex[0]))
                if request.json['algorithm'] == 'Boyer':
                    res_bm = searchBM(request.json['keyword'], txt)
                    if res_bm != -1:
                        res.append(allGroup(file['name'], date_file, numbers_file, txt, res_bm))
                if request.json['algorithm'] == 'KMP':
                    res_kmp = searchKMP(request.json['keyword'], txt)
                    if res_kmp != -1:
                        res.append(allGroup(file['name'], date_file, numbers_file, txt, res_kmp))
    return jsonify({'data': res}), 200

def allGroup(filename, defaultDate, defaultNumber, text, res_regex):
    date = matcher(date_regex(), text)
    number = matcher(numbers_regex(), text)

    return element(filename, text, res_regex, dateGroup(defaultDate, date), numberGroup(defaultNumber, number))

def dateGroup(default, date):
    if date:
        return date.group(0)
    return default

def numberGroup(default, number):
    if number:
        return number.group(1)
    return default

def element(filename, text, idx, date, number):
    return {'filename': filename, 'text': text, 'idx': idx, 'date': date, 'number': number}

def matcher(regex:str, text:str):
    return re.search(regex, text, flags=re.IGNORECASE|re.MULTILINE|re.UNICODE)

if __name__ == '__main__':
    app.run(debug=True)
