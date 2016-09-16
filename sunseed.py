#!/usr/bin/env python

import sys
import socket
import os.path
from videk_rest_client import Videk

videk = Videk("http://localhost:3000", "vMrr4jELLU1vxL9SdY63qJtlEZq42ykz")

if videk.serverOnline():
    print "Videk server is online ..."
else:
    print "Videk server is offline ..."
    sys.exit(1)

node = "node-name"
cluster = "cluster-name"
lat = 46.042767
lon = 14.487632
hw_id = open("/etc/machine-id", "r").readline().strip()

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

if os.path.isfile(pmc_file_name):
    pmc = open(pmc_file_name, "r").readline().strip()
    pmc = json.loads(pmc)
    # TODO register each sensor and upload data
elif os.path.isfile(spm_file_name):
    print "read spm data"
else:
    sys.exit(1)
