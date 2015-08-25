import requests
import json

class Beep:
    url = "http://ec2-54-235-125-114.compute-1.amazonaws.com/bees/lastMeasurementByNode?name="

    def __init__(self, nodeName):
        self.nodeName = nodeName

    def getBatteryVoltage(self):
        r = requests.get(self.url + self.nodeName)
        data = r.json()
        data = data[0]['data'][0]['value']
        return data

    def getSignalStrength(self):
        r = requests.get(self.url + self.nodeName)
        data = r.json()
        data = data[0]['data'][1]['value']
        return data

    def getWeight(self):
        r = requests.get(self.url + self.nodeName)
        data = r.json()
        data = data[1]['data'][0]['value']
        return data
