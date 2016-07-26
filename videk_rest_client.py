import sys
import requests
import json
import urllib2

class Videk:
    server_url = "http://localhost:3000"
    api_url = server_url + "/api"
    nodes_url = "/nodes"
    sensors_url = "/sensors"
    clusters_url = "/clusters"
    measurements_url = "/measurements"
    latitude = "null"
    longitude = "null"
    token = ""
    headers = {'Content-Type': 'application/json', 'Authorization': ''}

    def __init__(self, token):
        self.token = token
        self.headers = {'Content-Type': 'application/json', 'Authorization': token}

    def createCluster(self, clusterName):
        json_str = '''{ "name": "''' + clusterName + '''", "id": "''' + clusterName + '''", "tag": null, "type": "none",
        "URL": null, "scan" : "false", "comment":""  }'''
        try:
            r = requests.post(self.api_url + self.clusters_url, data=json_str, headers=self.headers)
            print r.text
            if "error" in r.text:
                print "Error: Cluster with the name " + clusterName + " already exists"
                sys.exit()
        except requests.exceptions.RequestException as e:
            print e

    def getClusterID(self, clusterName):
        try:
            r = requests.get(self.api_url + self.clusters_url + "?name=" + clusterName, headers=self.headers)
            cluster_id = r.json()
            if len(cluster_id) == 0:
                print "Error: Cluster with the name " + clusterName + " not found"
            else:
                return cluster_id[0]['id']
        except requests.exceptions.RequestException as e:
            print e

    def getClusterName(self, clusterID):
        try:
            r = requests.get(self.api_url + self.clusters_url + "?id=" + clusterID, headers=self.headers)
            cluster_name = r.json()
            if len(cluster_name) == 0:
                print "Error: Cluster with the id " + clusterID + " not found"
            else:
                return cluster_name[0]['name']
        except requests.exceptions.RequestException as e:
            print e

    def createNode(self, nodeName, clusterID):
        try:
            clusterName = self.getClusterName(clusterID)
            r = requests.get(self.api_url + self.nodes_url + "?name=" + nodeName, headers=self.headers)
            if "No nodes found" in r.text:
                json_str = '''{ "name": "''' + nodeName + '''", loc_lat": ''' + latitude + ''',
                "loc_lon": ''' + longitude + ''', "cluster": "''' + str(clusterID) + '''",
                "cluster_name": "''' + clusterName + '''", "status": "active", "components": [] }'''
                r = requests.post(self.api_url + self.nodes_url, data=json_str, headers=self.headers)
                print r.text
                if "error" in r.text:
                    print "Error: Node with the name  " + nodeName + " already exists"
                    sys.exit()
        except requests.exceptions.RequestException as e:
            print e

    def getNodeID(self, nodeName):
        try:
            r = requests.get(self.api_url + self.nodes_url + "?name=" + nodeName, headers=self.headers)
            node_id = r.json()
            if len(node_id) == 15:
                print "Error: Node with the name " + nodeName + " not found"
            else:
                return node_id[0]['id']
        except requests.exceptions.RequestException as e:
            print e

    def getNodeName(self, nodeID):
        try:
            r = requests.get(self.api_url + self.nodes_url + "?id=" + nodeID, headers=self.headers)
            node_name = r.json()
            if len(node_name) == 0:
                print "Error: Node with the id " + nodeID + " not found"
            else:
                return node_name[0]['name']
        except requests.exceptions.RequestException as e:
            print e

    def createSensor(self, nodeID, sensorType, sensorQuantity, sensorUnit):
        try:
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
        except requests.exceptions.RequestException as e:
            print e

    def getSensorID(self, nodeName, sensorType, sensorQuantity):
        try:
            r = requests.get(self.api_url + self.nodes_url + "?name=" + nodeName, headers=self.headers)
            data = r.json()
            node_id = data[0]['id']
            sensor_id = str(node_id) + "-" + sensorType + "-" + sensorQuantity
            r = requests.get(self.api_url + self.sensors_url + "?id=" + str(sensor_id), headers=self.headers)
            if "No sensors found" in r.text:
                print "No sensors found"
            else:
                return sensor_id
        except requests.exceptions.RequestException as e:
            print e

    def uploadMesurements(self, mesurements, nodeID, sensorID):
        try:
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
        except requests.exceptions.RequestException as e:
            print e

    def deleteCluster(self, clusterName):
        try:
            r = requests.get(self.api_url + self.clusters_url + "?name=" + clusterName, headers=self.headers)
            data = r.json()
            if len(data) == 0:
                print "No sensors found."
            else:
                cluster_id = data[0]['_id']
                r = requests.delete(self.api_url + self.clusters_url + "/" + str(cluster_id), headers=self.headers)
                print r.text
        except requests.exceptions.RequestException as e:
            print e

    def deleteNode(self, nodeName):
        try:
            r = requests.get(self.api_url + self.nodes_url + "?name=" + nodeName, headers=self.headers)
            data = r.json()
            if "No nodes found." in data:
                print data
            else:
                node_id = data[0]['_id']
                r = requests.delete(self.api_url + self.nodes_url + "/" + str(node_id), headers=self.headers)
                print r.text
        except requests.exceptions.RequestException as e:
            print e

    def deleteSensor(self, nodeID, sensorType, sensorQuantity):
        try:
            sensor_id = str(nodeID) + "-" + sensorType + "-" + sensorQuantity
            r = requests.get(self.api_url + self.sensors_url + "?id=" + sensor_id, headers=self.headers)
            if "No sensors found" in r.text:
                print r.text
            else:
                data = r.json()
                node_id = data[0]['_id']
                r = requests.delete(self.api_url + self.sensors_url + "/" + str(node_id), headers=self.headers)
                print r.text
        except requests.exceptions.RequestException as e:
            print e

    def serverOn(self):
        try:
            response = urllib2.urlopen(server_url, timeout=1)
            return True
        except urllib2.URLError as err: pass
        return False
