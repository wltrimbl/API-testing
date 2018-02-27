#!/usr/bin/env python

import sys
import json
from subprocess import check_output

if len(sys.argv) == 1:
    sys.stderr.write("missing required etcd host IP\n")
    sys.exit(1)

etcdip = sys.argv[1]

try:
    info = json.loads(check_output(["curl", "-s", "http://%s:2379/v2/keys/services/api-server/api/"%(etcdip)]))
except:
    sys.stderr.write("unable to connect to etcd cluster using IP=%s\n"%(etcdip))
    sys.exit(1)

for entry in info["node"]["nodes"]:
    value = json.loads(entry["value"])
    ip = value["COREOS_PUBLIC_IPV4"]
    port = value["http"]
    print "http://%s:%d"%(ip, port)

sys.exit(0)

