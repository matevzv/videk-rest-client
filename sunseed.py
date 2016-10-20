#!/usr/bin/env python

import sys
import json
import time
import socket
import os.path
from datetime import datetime
from videk_rest_client import Videk

videk = Videk("http://localhost:3000", "secret")
node = socket.gethostname()
cluster = node[:node.rfind("-")]
lat = 46.042767
lon = 14.487632
machine_id = open('/etc/machine-id').readline().strip()
mac = open('/sys/class/net/eth0/address').read().strip()

def uploadSensors(node_id, sensor_type, sensors):
    for sensor in sensors:
        sensor_id = videk.getSensorID(node, sensor_type, sensor['name'])
        if sensor_id == None:
            videk.createSensor(node_id, sensor_type, sensor['name'],
                sensor['unit'])
            sensor_id = videk.getSensorID(node, sensor_type, sensor['name'])

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

node_id_by_node_name = videk.getNodeID(node)
node_id_by_node_machine_id = videk.getNodeByHardwareId(machine_id);
node_model_update = None

if node_id_by_node_name == None and node_id_by_node_machine_id == None:
    videk.createNode(node, cluster_id)
    node_id = videk.getNodeID(node)
    videk.updateSingleNodeParam(node_id, "machine_id", machine_id)
    videk.addNodeExtraField(node_id, "MAC", mac)
    node_model = videk.getNode(node)
elif node_id_by_node_name == None and node_id_by_node_machine_id != None:
    node_model = videk.getNodeByHardwareId(machine_id)
    node_model_update = {}
    if node_model['name'] != node:
        node_model['name'] = node
        node_model_update['name'] = node
        print "updated node name"
    if node_model['cluster'] != cluster:
        node_model['cluster'] = cluster
        node_model['cluster_name'] = cluster
        node_model_update['cluster'] = cluster
        node_model_update['cluster_name'] = cluster
        print "updated node cluster"
elif node_id_by_node_name != None and node_id_by_node_machine_id == None:
    node_model = videk.getNode(node)
    node_model_update = {}
    if node_model['machine_id'] != machine_id:
        node_model['machine_id'] = machine_id
        node_model_update['machine_id'] = machine_id
        print "updated node machine_id"
else:
    node_model = videk.getNode(node)

if node_model_update != None:
    videk.updateNode(node_model['id'], node_model_update)
    print "updated node model"

if lat != node_model['latitude'] or lon != node_model['longitude']:
    lat = node_model['latitude']
    lon = node_model['longitude']
    print "updated node location"

if os.path.isfile(pmc_file_name):
    pmc = open(pmc_file_name, "r").readline().strip()
    pmc = json.loads(pmc)
    uploadSensors(node_model['id'], "pmc", pmc)
elif os.path.isfile(spm_file_name):
    spm = open(spm_file_name, "r").readline().strip()
    spm = json.loads(spm)
    uploadSensors(node_model['id'], "spm", spm)
else:
    print "No sensors found!"
