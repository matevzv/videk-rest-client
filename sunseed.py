#!/usr/bin/env python

import sys
import json
import time
import os.path
from datetime import datetime
from videk_rest_client import Videk

videk = Videk("http://localhost:3000", "dEjdS28qKZ4exzjzxSdaHI6tzlfuAzFE")
node = "node-name"
cluster = "cluster-name"
lat = 46.042767
lon = 14.487632
machine_id = open('/etc/machine-id').readline().strip()
mac = open('/sys/class/net/enx847beb5aad2a/address').read().strip()
sw_version = "v1.0"

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

node_id_by_node_name = videk.getNode(node)
node_id_by_node_machine_id = videk.getNodeByHardwareId(machine_id);
node_model_update = {}

if node_id_by_node_name == None and node_id_by_node_machine_id == None:
    videk.createNode(node, cluster_id)
    node_id = videk.getNodeID(node)
    videk.updateSingleNodeParam(node_id, "machine_id", machine_id)
    videk.addNodeExtraField(node, "MAC", mac)
    #videk.addNodeExtraField(node, "Software", sw_version)
    node_model = videk.getNode(node)
elif node_id_by_node_name == None and node_id_by_node_machine_id != None:
    node_model = videk.getNodeByHardwareId(machine_id)
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
    node_model = node_id_by_node_name
    if node_model['machine_id'] != machine_id:
        node_model['machine_id'] = machine_id
        node_model_update['machine_id'] = machine_id
        print "updated node machine_id"
else:
    node_model = node_id_by_node_name

extra_fields = {}
update = False
extra_fields['extra_fields'] = []

if type(node_model['extra_fields']) != list:
    node_model['extra_fields'] = [node_model['extra_fields']]
    update = True

for extra_field in node_model['extra_fields']:
    if 'Software' in extra_field:
        if extra_field['Software'] != sw_version:
            extra_fields['extra_fields'].append({'Software':sw_version})
            update = True
            continue
    elif 'MAC' in extra_field:
        if extra_field['MAC'] != mac:
            extra_fields['extra_fields'].append({'MAC':mac})
            update = True
            continue
    extra_fields['extra_fields'].append(extra_field)

if update:
    node_model_update['extra_fields'] = extra_fields['extra_fields']

if len(node_model_update) != 0:
    videk.updateNode(node_model['id'], node_model_update)
    print "updated node model"

if lat != float(node_model['loc_lat']) or lon != float(node_model['loc_lon']):
    lat = node_model['loc_lat']
    lon = node_model['loc_lon']
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
