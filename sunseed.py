#!/usr/bin/env python

import sys
import socket
from videk_rest_client import Videk

videk = Videk("address", "secret")

if videk.serverOn:
    echo "Videk server is online ..."
else:
    echo "Videk server is offline ..."
    sys.exit(1)

node = "node-name"
cluster = "cluster-name"
lat = 46.042767
lon = 14.487632

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
