#!/usr/bin/env python

import sys
import json
import time
import socket
import os.path
from datetime import datetime
from videk_rest_client import Videk

videk = Videk("address", "secret")
node = "node-name"
cluster = "cluster-name"
lat = 46.042767
lon = 14.487632
hw_id = open("/etc/machine-id", "r").readline().strip()

def uploadSensors(sensor_type, sensors):
    for sensor in sensors:
        sensor_id = videk.getSensorID(node, sensor_type, sensor['name'])
        if sensor_id == None:
            videk.createSensor(node_id, sensor_type, sensor['name'],
                sensor['unit'])
            sensor_id = videk.getSensorID(node, sensor_type, sensor['name'])

            print sensor['name']
        print sensor_id
        measurement = '''{"latitude":"","longitude":"","ts":"","value":""}'''
        v = sensor['value']
        preparedData = []
        data = json.loads(measurement)
        data['value'] = v
        data['ts'] = datetime.utcnow().isoformat()
        data['latitude'] = lat
        data['longitude'] = lon
        preparedData.append(data)

        videk.uploadMesurements(preparedData, node_id, sensor_id)

if videk.serverOnline():
    print "Videk server is online ..."
else:
    print "Videk server is offline ..."
    sys.exit(1)

pmc_file_name = "/tmp/pmc-data"
spm_file_name = "/tmp/spm-data"

videk.latitude = lat
videk.longitude = lon

cluster_id = videk.getClusterID(cluster)
if cluster_id == None:
    videk.createCluster(cluster)
    cluster_id = videk.getClusterID(cluster)

node_id = videk.getNodeID(node)

if node_id == None:
    videk.createNode(node, cluster_id)
    node_id = videk.getNodeID(node)
    videk.addNodeExtraField(node_id, "HW_ID", hw_id)
else:
    lat_lon = videk.getNodeLocation(node)
    print lat_lon
    if lat != lat_lon['latitude'] or lon != lat_lon['longitude']:
        lat = lat_lon['latitude']
        lon = lat_lon['longitude']

if os.path.isfile(pmc_file_name):
    pmc = open(pmc_file_name, "r").readline().strip()
    pmc = json.loads(pmc)
    uploadSensors("pmc", pmc)
elif os.path.isfile(spm_file_name):
    spm = open(spm_file_name, "r").readline().strip()
    spm = json.loads(spm)
    uploadSensors("spm", spm)
else:
    sys.exit(1)
