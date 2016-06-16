#!/usr/bin/env python

import sys
import time
import json
from datetime import datetime
from videk_rest_client import Videk
from random import randint

x = Videk('secret')
x.api_url = "http://localhost/api"

cluster = "example";
node = "example.com"
sensor_t = "test"
sensor_q = "test_value"
sensor_u = "t"

cluster_id = x.getClusterID(cluster)
if cluster_id == None:
    x.createCluster(cluster)
    cluster_id = x.getClusterID(cluster)

node_id = x.getNodeID(node)
if node_id == None:
    x.createNode(node, cluster_id)
    node_id = x.getNodeID(node)

sensor_id = x.getSensorID(node, sensor_t, sensor_q)
if sensor_id == None:
    x.createSensor(node_id, sensor_t, sensor_q, sensor_u)
    sensor_id = x.getSensorID(node, sensor_t, sensor_q)

measurement = '''{"latitude":"","longitude":"","ts":"","value":""}'''

while True:
    try:
        v = randint(1, 10)

        preparedData = []
        data = json.loads(measurement)
        data['value'] = v
        data['ts'] = datetime.utcnow().isoformat()
        data['latitude'] = 11.111111
        data['longitude'] = 11.111111
        preparedData.append(data)

        x.uploadMesurements(preparedData, node_id, sensor_id)

        time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
         sys.exit(0)
    except:
         time.sleep(10)
