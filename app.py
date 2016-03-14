from flask import Flask, render_template, request
import requests
import collections
import pickle
import fcntl
import os.path, time
from flask import jsonify
from flask import json


app = Flask(__name__)


#TODO: still need to handle the file age case
@app.route('/')
def hello_world():
    errored = False
    r = {}
    samples = []
    pickle_file = open("save.p", "rb")
    try:
        fcntl.flock(pickle_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        d = pickle.load(pickle_file)
        samples = list(d)
        r["data"] = list(d)
    except IOError as e:
        # raise on unrelated IOErrors
        errored = True
        print 'IOError'
    except EOFError as e2:
        print "EOFError"
    pickle_file.close()
    timestamp = getTimestamp()
    if errored:
        return  "error, please try again"
    return render_template('yes_no.html', is_busy=roomOccupied(samples), timestamp=timestamp)

def getTimestamp():
    s = 'unknown'
    try:
        s = time.ctime(os.path.getctime('save.p'))
    except OSError:
        pass
    return s

def roomOccupied(samples):
    sumSamples = 0
    for sample in samples:
        if int(sample) == 1:
            sumSamples += 1
        print sample
    print "total 1s: " + str(sumSamples)
    print "total length: " + str(len(samples))
    return sumSamples > (len(samples)/4)
        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


