'''
Created on Jan 22, 2016

@author: Thomas
'''

from flask.app import Flask
from flask import request
import xml.etree.ElementTree as ET
import json

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/groups/list')
def readGroups():
    tree = ET.parse('fair-scheduler.xml')
    root = tree.getroot()
    queueList = {"queues" : {} }
    for queue in root.findall('queue'):
        queueList["queues"][queue.get('name')] = {}
        minResources = queue.find('minResources')
        if minResources is not None:
            minResourcesPieces = minResources.text.split(',')
            memory = minResourcesPieces[0].split(' mb')[0]
            vcores = minResourcesPieces[1].split('vcores')[0]
            queueList["queues"][queue.get('name')]["minMemory"] = memory
            queueList["queues"][queue.get('name')]["minVcores"] = vcores
        weight = queue.find('weight')
        if weight is not None:
            queueList["queues"][queue.get('name')]["weight"] = weight.text
    return json.dumps(queueList)

@app.route('/groups/update',methods=["POST"])
def editGroup():
    jsonPosted = request.get_json(force=True)
    print jsonPosted
    return json.dumps(jsonPosted)

if __name__ == '__main__':
    app.run(debug = True)