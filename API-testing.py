#!/usr/bin/env python
'''This script retrieves example API invokations form MG-RAST and compares new results
against stored return values from the example API calls. '''

import urllib2, json, sys, md5, os
from optparse import OptionParser
from time import time
import subprocess
API_URL = "http://api.metagenomics.anl.gov/1"

SKIP = ["48f15d5aae95892edb9bae03988573fa",
        '3bfa44d3dad4e2af12bab2601cfa8138',
        'a78c50dc4b81f0d02fc0391532cc61f4',
        'c0a6a295563e01e7c42628cfe81b7431',
        '19fe36c957ab88a6b5a567d885db445c'] # these take too long

def sanitize(c):
    '''Function to remove escaping from API example strings'''
    clist = c.split()
    for i, c in enumerate(clist):
        if c[0] == "'" and c[-1] == "'":
            clist[i] = c[1:-1]
        if c[0] == '"' and c[-1] == '"':
            clist[i] = c[1:-1]
    return " ".join(clist)

def getmeajsonobject(url):
    '''places HTTP request for url and parses the returned JSON object'''
    if VERBOSE:
        sys.stderr.write("Retrieving %s\n" % url)
    try:
        opener = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print "Error with HTTP request: %d %s\n%s" % (e.code, e.reason, e.read())
        return None
    opener.addheaders = [('User-agent', 'API-testing.py')]

    jsonobject = opener.read()
    jsonstructure = json.loads(jsonobject)
    return jsonstructure

def print_tests(testlist):
    for test in testlist:
        callhash, call, name, name2, description = test
        print callhash, call, description

def check_ok(stem, dir1, blesseddir):
    '''Populates a file called WORKING + stem + ".test" with symbols
    indicating which tests for similarity of output passed'''
    f1 = open(dir1+"/"+stem+".out").read()
    f2 = open(blesseddir+"/"+stem+".out").read()
    md5A = md5.new(f1).hexdigest()
    md5B = md5.new(f2).hexdigest()
    if len(f1) == 0 and len(f2) == 0:
        return True, "matchempty"
    if md5A != md5B:
        if len(f1) == 0:
            return False, "emptyoutput"
        if len(f1) > 0 and len(f2) > 0 and f1[0] == "{" and f2[0] == "{":
            j1 = json.loads(f1)
            j2 = json.loads(f2)
            if "date" in j1.keys():
                j1["date"] = ""
            if "date" in j2.keys():
                j2["date"] = ""
            if j1 == j2:
                return True, "JSONmatch"
            else:
                return False, "JSONdiff {:d}, {:d}".format(len(f1), len(f2))
        else:
            return False, "not json, {:d}, {:d}".format(len(f1), len(f2))
    else:
         return True, "MD5match"

def run_tests(testlist):
    for test in testlist:
        if test[0] not in SKIP or not FAST:
            callhash, call, name, name2, description = test
            fncall = WORKING + "/" + callhash + ".call"
            fcall = open(fncall, "w")
            fcall.write(call+"\n")
            fcall.close()
            fnout = WORKING+"/"+"{}.out".format(callhash)
            fout = open(fnout, "w")
            shell = False
            fnerr = WORKING + "/" + callhash
            if call[0:4] == "curl":
                command = "{} -s -D {}.err".format(call, fnerr)
                command = sanitize(command)
            else:
                command = "curl {} -s -D {}.err".format(call, fnerr)
            if VERBOSE or 1:
                print "trying", callhash, command
            start = time()
            subprocess.call(str(command).split(), stdout=fout, shell=shell)
            elapsed = time() - start
            fout.close()
            ok, mesg = check_ok(callhash, WORKING, BLESSED)
            if ok:
                os.remove(fnout)
            else:
                pass
            ftest = open(WORKING+"/"+callhash + ".test", "w")
            if VERBOSE:
                print repr(ok)+mesg
            ftest.write(repr(ok)+mesg+"\n")
            ftest.close()
            ftime = open(WORKING+"/"+callhash + ".time", "w")
            ftime.write(str(elapsed)+"\n")
            ftime.close()
        else:
            print "skipping", test[0]

def get_example_calls(base_url):
    topleveljsonobjects = {}
    requestlist = []
    json_api_calls = getmeajsonobject(base_url)
    listofapiurls = [resources["url"]  for resources in json_api_calls["resources"]]
    for resourceurl in listofapiurls:
        if VERBOSE:
            sys.stderr.write(resourceurl+"\n")
        topleveljsonobjects[resourceurl] = getmeajsonobject(resourceurl)
    if VERBOSE:
        print listofapiurls
    for resource in listofapiurls:
        name = resource.split("/")[-1]
        try:
            for request in topleveljsonobjects[resource]["requests"]:
                try:
                    n = request["name"]
                    example = request["example"][0].replace("auth_key", "")
                    callhash = md5.new(request["example"][0]).hexdigest()
                    requestlist.append((callhash, request["example"][0], name, request["name"], request["description"]))
                except KeyError:
                    pass
        except TypeError:
            pass
    return requestlist

if __name__ == '__main__':
    usage = "usage: %prog \n  Tests MG-RAST API calls with example invokations in API"
    parser = OptionParser(usage)
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                      default=False, help="Verbose")
    parser.add_option("-b", "--blesseddir", dest="blesseddir", type="str",
                      default="data", help="Location of stored (good) results")
    parser.add_option("-w", "--workdingdir", dest="workingdir", type="str",
                      default=".", help="Working dir--will be filled with output files")
    parser.add_option("-t", "--test", dest="tests", action="store_true",
                      default=False, help="don't do it, just print tests")
    parser.add_option("-f", "--fast", dest="fast", action="store_true",
                      default=False, help="fast-skip slow tests")

    (opts, args) = parser.parse_args()
    VERBOSE = opts.verbose
    BLESSED = opts.blesseddir
    WORKING = opts.workingdir
    TESTS = opts.tests
    FAST = opts.fast

    tests = get_example_calls(API_URL)
    if  TESTS:
        print_tests(tests)
    else:
        run_tests(tests)

