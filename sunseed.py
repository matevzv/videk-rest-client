#!/usr/bin/env python

import sys
import socket
from videk_rest_client import Videk

videk = Videk("address", "secret")

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
