#!/usr/bin/env python
# encoding: utf-8
import subprocess
import re
import time
import json
import datetime
from videk_rest_client import Videk

x = Videk('TOKEN')

x.createCluster('clusterName')
cluster_id = x.getClusterID('clusterName')

x.createNode('nodeName', cluster_id)
node_id = x.getNodeID('nodeName')

x.createSensor(node_id, 'sensorType', 'sensorQuantity', 'sensorUnit')
sensor_id = x.getSensorID('nodeName', 'sensorType', 'sensorQuantity')

measurement = '''{"latitude": 99.999999 , "longitude": 99.999999 ,"ts": "2014-07-24T15:14:30.850Z","value": 0 }'''
while True:
    #Get CPU temperature
    sensors = subprocess.check_output("sensors")
    temperatures = {match[0]: float(match[1]) for match in re.findall("^(.*?)\:\s+\+?(.*?)°C", sensors, re.MULTILINE)}

    preparedData = []
    data = json.loads(measurement)
    data['value'] = temperatures['Core 0']
    data['ts'] = datetime.utcnow().isoformat()
    data['latitude'] = 11.111111
    data['longitude'] = 11.111111
    preparedData.append(data)

    x.uploadMesurements(preparedData, node_id, sensor_id)
    time.sleep(10)
