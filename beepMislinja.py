#!/usr/bin/env python

import sys
import time
import json
from datetime import datetime
from videk_rest_client import Videk
from beep import Beep

x = Videk('nRmU1rIiTETP4brIPkKr+SO/uumG5kzR')

cluster = "beep";
node = "beepMislinja"
sensor_t = "beep"
sensor_q1 = "voltage"
sensor_u1 = "mV"
sensor_q2 = "signal"
sensor_u2 = "dBm"
sensor_q3 = "weight"
sensor_u3 = "g"

cluster_id = x.getClusterID(cluster)
if cluster_id == None:
    x.createCluster(cluster)
    cluster_id = x.getClusterID(cluster)

node_id = x.getNodeID(node)
if node_id == None:
    x.createNode(node, cluster_id)
    node_id = x.getNodeID(node)

sensor_id_v = x.getSensorID(node, sensor_t, sensor_q1)
if sensor_id_v == None:
    x.createSensor(node_id, sensor_t, sensor_q1, sensor_u1)
    sensor_id_v = x.getSensorID(node, sensor_t, sensor_q1)

sensor_id_s = x.getSensorID(node, sensor_t, sensor_q2)
if sensor_id_s == None:
    x.createSensor(node_id, sensor_t, sensor_q2, sensor_u2)
    sensor_id_s = x.getSensorID(node, sensor_t, sensor_q2)

sensor_id_w = x.getSensorID(node, sensor_t, sensor_q3)
if sensor_id_w == None:
    x.createSensor(node_id, sensor_t, sensor_q3, sensor_u3)
    sensor_id_w = x.getSensorID(node, sensor_t, sensor_q3)

nodeName = "1401003"
beep = Beep(nodeName)
measurement = '''{"latitude":"","longitude":"","ts":"","value":""}'''

while True:
    try:
        v = beep.getBatteryVoltage()
        s = beep.getSignalStrength()
        w = beep.getWeight()

        preparedData = []
        data = json.loads(measurement)
        data['value'] = v
        data['ts'] = datetime.utcnow().isoformat()
        data['latitude'] = 11.111111
        data['longitude'] = 11.111111
        preparedData.append(data)

        x.uploadMesurements(preparedData, node_id, sensor_id_v)

        preparedData = []
        data = json.loads(measurement)
        data['value'] = s
        data['ts'] = datetime.utcnow().isoformat()
        data['latitude'] = 11.111111
        data['longitude'] = 11.111111
        preparedData.append(data)

        x.uploadMesurements(preparedData, node_id, sensor_id_s)

        preparedData = []
        data = json.loads(measurement)
        data['value'] = w
        data['ts'] = datetime.utcnow().isoformat()
        data['latitude'] = 11.111111
        data['longitude'] = 11.111111
        preparedData.append(data)

        x.uploadMesurements(preparedData, node_id, sensor_id_w)

        time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
    except:
        time.sleep(10)
        pass
