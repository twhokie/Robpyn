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
    tree = ET.parse('fair-scheduler.xml')
    root = tree.getroot()
    for newQueue in jsonPosted:
        print newQueue
        for queue in root.findall('queue'):
            if queue.get('name') == newQueue:
                minResources = queue.find('minResources')
                if minResources is not None:
                    newValues = `jsonPosted[newQueue]['minMemory']` + " mb," + `jsonPosted[newQueue]["minVcores"]` +"vcores"
                    minResources.text = newValues
                    tree.write('fair-scheduler-new.xml') 
    return "{\"success\" : True}"

@app.route('/groups/create',methods=["POST"])
def createGroup():
    jsonPosted = request.get_json(force=True)
    tree = ET.parse('fair-scheduler.xml')
    root = tree.getroot()
    for newQueue in jsonPosted:
        newQueueElem = ET.SubElement(root, 'queue',attrib={'name':newQueue})
        newMinResourcesElem = ET.SubElement(newQueueElem, 'minResources')
        newMinResourcesElem.text = `jsonPosted[newQueue]['minMemory']` + " mb," + `jsonPosted[newQueue]["minVcores"]` +"vcores"
        newWeightElem = ET.SubElement(newQueueElem, 'weight')
        newWeightElem.text = `jsonPosted[newQueue]['weight']` 
    tree.write('fair-scheduler-new.xml') 
    return "{\"success\" : True}"

@app.route('/groups/delete',methods=["POST"])
def deleteGroup():
    jsonPosted = request.get_json(force=True)
    tree = ET.parse('fair-scheduler.xml')
    root = tree.getroot()
    for newQueue in jsonPosted:
        for queue in root.findall('queue'):
            if queue.get('name') == newQueue:
                root.remove(queue)
    tree.write('fair-scheduler-new.xml') 
    return "{\"success\" : True}"

if __name__ == '__main__':
    app.run(debug = True)