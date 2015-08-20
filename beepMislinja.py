#!/usr/bin/env python
import sys
import time
import json
from datetime import datetime
from videk_rest_client import Videk
from beep import Beep

x = Videk('nRmU1rIiTETP4brIPkKr+SO/uumG5kzR')

#x.createCluster('Beep')
cluster_id = x.getClusterID('Beep')

#x.createNode('BeepMislinja', cluster_id)
node_id = x.getNodeID('BeepMislinja')

#x.createSensor(node_id, 'beep', 'voltage', 'mV')
sensor_id_v = x.getSensorID('BeepMislinja', 'beep', 'voltage')

#x.createSensor(node_id, 'beep', 'signal', 'dBm')
sensor_id_s = x.getSensorID('BeepMislinja', 'beep', 'signal')

#x.createSensor(node_id, 'beep', 'weight', 'g')
sensor_id_w = x.getSensorID('BeepMislinja', 'beep', 'weight')

nodeName = "1401003"
beep = Beep(nodeName)
measurement = '''{"latitude": 99.999999 , "longitude": 99.999999 ,"ts": "2014-07-24T15:14:30.850Z","value": 0 }'''
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
