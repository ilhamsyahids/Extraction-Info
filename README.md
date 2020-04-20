# My Extraction Info 

## Prerequisite
Make sure you have installed:
1. [node js](https://nodejs.org/en/)
2. [npm](https://www.npmjs.com/get-npm)
3. [flask](https://pypi.org/project/Flask/)

## Dependency
Client dependency in `app/package.json`
<br>
Server dependency `flask` and `flask_cors`

## How To Use
In this directory (root), run:
1. Client:
```
npm run client
```
2. Server:
```
npm run server
```
Alternative (Tested: Mac OS/Linux) :
```
$ cd server
$ virtualenv flask
$ flask/bin/pip install flask flask_cors
$ chmod a+x server.py
$ ./server.py
```


## Note
This program work fluenty and tested in Mac OS. It should be well in Windows and Linux.