#!flask/bin/python
import re
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from algorithm import *

app = Flask(__name__)

# CORS
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'])
def welcome():
    return jsonify({'data': 'res'}), 200

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
        time = re.compile(r'(\d+)[\s*]')
        for paragraph in file['text']:
            # Split into sentences
            sentence_regex = r'([\.\?!][\'\"\u2018\u2019\u201c\u201d\)\]]*\s*(?<!\w\.\w.)(?<![A-Z][a-z][a-z]\.)(?<![A-Z][a-z]\.)(?<![A-Z]\.)\s+)'
            sentences = re.compile(sentence_regex, flags=re.UNICODE).split(paragraph)
            for txt in sentences:
                # Apply algorithm
                if request.json['algorithm'] == 'Regex':
                    if len(searchRegex(request.json['keyword'], txt)) != 0:
                        res.append(element(file['name'], txt))
                if request.json['algorithm'] == 'Boyer':
                    if searchBM(request.json['keyword'], txt) != -1:
                        res.append(element(file['name'], txt))
                if request.json['algorithm'] == 'KMP':
                    if searchKMP(request.json['keyword'], txt) != -1:
                        res.append(element(file['name'], txt))
    return jsonify({'data': res}), 200

def element(filename, text):
    return {'filename': filename, 'text': text }

if __name__ == '__main__':
    app.run(debug=True)
