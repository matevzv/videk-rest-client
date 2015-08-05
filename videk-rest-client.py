import sys
import requests
import json

class Videk:
    api_url = "https://www.e-osu.si/api"
    nodes_url = "/nodes"
    sensors_url = "/sensors"
    clusters_url = "/clusters"
    measurements_url = "/measurements"
    token = ""
    headers = {'Content-Type': 'application/json', 'Authorization': ''}

    def __init__(self, token):
        self.token = token
        self.headers = {'Content-Type': 'application/json', 'Authorization': token}

    def createCluster(self, clusterName):
        json_str = '''{ "title": "''' + clusterName + '''", "id": "''' + clusterName + '''", "tag": null, "type": "none",
         "URL": null, "scan" : "false", "comment":""  }'''
        r = requests.post(self.api_url + self.clusters_url, data=json_str, headers=self.headers)
        print r.text
        if "error" in r.text:
            print "Error: Cluster with the name " + clusterName + " already exists"
            sys.exit()

    def getClusterID(self, clusterName):
        r = requests.get(self.api_url + self.clusters_url + "?name=" + clusterName, headers=self.headers)
        cluster_id = r.json()
        if len(cluster_id) == 0:
            print "Error: Cluster with the name " + clusterName + " not found"
        else:
            return cluster_id[0]['id']

    def getClusterName(self, clusterID):
        r = requests.get(self.api_url + self.clusters_url + "?id=" + clusterID, headers=self.headers)
        cluster_name = r.json()
        if len(cluster_name) == 0:
            print "Error: Cluster with the id " + clusterID + " not found"
        else:
            return cluster_name[0]['name']

    def createNode(self, nodeName, clusterID):
        clusterName = self.getClusterName(clusterID)
        r = requests.get(self.api_url + self.nodes_url + "?name=" + nodeName, headers=self.headers)
        if "No nodes found" in r.text:
            json_str = '''{ "name": "''' + nodeName + '''", "location": "", "loc_lat": null, "loc_lon": null,
             "cluster": "''' + str(clusterID) + '''", "cluster_name": "''' + clusterName + '''", "status": "active",
             "setup": "", "scope": "", "project": "", "user_comment": "", "box_label": "", "serial_no": "", "mac": "",
             "network_addr": null, "network_addr2"  : null, "firmware": "", "bootloader": "", "role": "device", "sensors":
             [], "components": [] }'''
            r = requests.post(self.api_url + self.nodes_url, data=json_str, headers=self.headers)
            print r.text
            if "error" in r.text:
                print "Error: Node with the name  " + nodeName + " already exists"
                sys.exit()

    def getNodeID(self, nodeName):
        r = requests.get(self.api_url + self.nodes_url + "?name=" + nodeName, headers=self.headers)
        node_id = r.json()
        if len(node_id) == 0:
            print "Error: Node with the name " + nodeName + " not found"
        else:
            return node_id[0]['id']

    def getNodeName(self, nodeID):
        r = requests.get(self.api_url + self.nodes_url + "?id=" + nodeID, headers=self.headers)
        node_name = r.json()
        if len(node_name) == 0:
            print "Error: Node with the id " + nodeID + " not found"
        else:
            return node_name[0]['name']

    def createSensor(self, nodeID, sensorType, sensorQuantity, sensorUnit):
        sensor_id = str(nodeID) + "-" + sensorType + "-" + sensorQuantity
        r = requests.get(self.api_url + self.sensors_url + "?id=" + sensor_id, headers=self.headers)
        if "No sensors found" in r.text:
            r = requests.get(self.api_url + self.nodes_url + "?id=" + str(nodeID), headers=self.headers)
            node_id = r.json()[0]['_id']
            json_str = '''{ "id": "''' + sensor_id + '''", "type": "''' + sensorType + '''", "quantity":
            "''' + sensorQuantity + '''", "unit": "''' + sensorUnit + '''", "node_id": "''' + node_id + '''",
            "node": ''' + str(nodeID) + ''' }'''
            r = requests.post(self.api_url+self.sensors_url, data=json_str, headers=self.headers)
            print r.text
        else:
            print "Sensor already exists"

    def getSensorID(self, nodeName, sensorType, sensorQuantity):
        r = requests.get(self.api_url + self.nodes_url + "?name=" + nodeName, headers=self.headers)
        data = r.json()
        node_id = data[0]['id']
        sensor_id = str(node_id) + "-" + sensorType + "-" + sensorQuantity
        r = requests.get(self.api_url + self.sensors_url + "?id=" + str(sensor_id), headers=self.headers)
        if "No sensors found" in r.text:
            print "No sensors found"
        else:
            return sensor_id

    def uploadMesurements(self, mesurements, nodeID, sensorID):
        r = requests.get(self.api_url + self.sensors_url + "?id=" + sensorID, headers=self.headers)
        sensor_mongo_id = r.json()[0]['_id']
        r = requests.get(self.api_url + self.nodes_url + "?id=" + str(nodeID), headers=self.headers)
        node_mongo_id = r.json()[0]['_id']
        measurement = '''{"sensor_id":"''' + sensor_mongo_id + '''","node_id": "''' + node_mongo_id + '''","sensor":
        "''' + sensorID + '''","node": ''' + str(nodeID) + ''', "latitude": 99.999999 , "longitude": 99.999999 ,"ts":
         "2014-07-24T15:14:30.850Z","value": 0,"context":"data"}'''
        preparedData = []
        for x in mesurements:
            data = json.loads(measurement)
            data['value'] = x['value']
            data['ts'] = x['ts']
            data['latitude'] = x['latitude']
            data['longitude'] = x['longitude']
            preparedData.append(data)
        r = requests.post(self.api_url+self.measurements_url, data=json.dumps(preparedData), headers=self.headers)
        print r.text