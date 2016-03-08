from flask import Flask, render_template, request
import requests
import collections
import pickle
import fcntl
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
    if errored:
        return  "error, please try again"
    return render_template('yes_no.html', is_busy=roomOccupied(samples))

def roomOccupied(samples):
    sumSamples = 0
    for sample in samples:
        if sample == 1:
            sumSamples += 1
        print sample
    return sumSamples > len(samples)
        

if __name__ == '__main__':
    app.run(debug=True)


