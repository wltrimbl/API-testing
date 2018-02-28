#!/usr/bin/env python

import re
import sys
import json
import random
from subprocess import check_output

if len(sys.argv) == 1:
    sys.stderr.write("missing required etcd host name\n")
    sys.exit(1)

etcdhost = sys.argv[1]
hostregex = re.match(r'^(.*)\{(\d+)\.\.(\d+)\}(.*)$', etcdhost)
if hostregex:
    prefix = hostregex.group(1)
    first  = int(hostregex.group(2))
    last   = int(hostregex.group(3))
    suffix = hostregex.group(4)
    etcdhost = "%s%d%s"%(prefix, random.randint(first, last), suffix)
    print etcdhost

try:
    info = json.loads(check_output(["curl", "-s", "http://%s:2379/v2/keys/services/api-server/api/"%(etcdhost)]))
except:
    sys.stderr.write("unable to connect to etcd cluster using host=%s\n"%(etcdhost))
    sys.exit(1)

for entry in info["node"]["nodes"]:
    value = json.loads(entry["value"])
    ip = value["COREOS_PUBLIC_IPV4"]
    port = value["http"]
    print "http://%s:%d"%(ip, port)

sys.exit(0)

