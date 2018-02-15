#!/usr/bin/env python
'''This script retrieves example API invokations form MG-RAST and compares new results
against stored return values from the example API calls. '''

from __future__ import print_function
import json
import sys
import os
import codecs
from hashlib import md5
import argparse
from time import time
import subprocess

try:  # python3
    from urllib.parse import urlparse, urlencode, parse_qs
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
except ImportError:  # python2
    from urlparse import urlparse, parse_qs
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError

from mglib.mglib import obj_from_url, async_rest_api


API_URL = "https://api.mg-rast.org/1"

SKIP = ["48f15d5aae95892edb9bae03988573fa",
        '3bfa44d3dad4e2af12bab2601cfa8138',
        'a78c50dc4b81f0d02fc0391532cc61f4',
        'c0a6a295563e01e7c42628cfe81b7431',
        '19fe36c957ab88a6b5a567d885db445c',
        '084905a84b75b6860c877a5804453829',
        '23bd3abcc793f83d87e16913c99ef5ac',
        '376206640f1592ac9302e30d7cf8fabb',
        '7017b76a86eee625ec9d954a6149dd12'] # these take too long



def sanitize(c):
    '''Function to remove escaping from API example strings'''
    clist = c.split()
    for i, c in enumerate(clist):
        if c[0] == "'" and c[-1] == "'":  # remove items with single quotes
            clist[i] = c[1:-1]
        if c[0] == '"' and c[-1] == '"':  # remove items with double quotes
            clist[i] = c[1:-1]
    for i, c in enumerate(clist):  # remove spaces within '-escaped examples
        for j in range(len(clist)-1, i-1, -1):
            if c[0] == "'" and clist[j][-1] == "'":
                clist = clist[:i] + ["".join(clist[i:j+1])[1:-1]] + clist[j+1:]
    return " ".join(clist)

def print_tests(testlist):
    for test in testlist:
        callhash, call, name, name2, description = test
        print(callhash, call, description)

def check_ok(stem, dir1, blesseddir):
    '''Populates a file called WORKING + stem + ".test" with symbols
    indicating which tests for similarity of output passed'''
    try:
        f1 = codecs.open(dir1+"/"+stem+".out", encoding="utf8").read()
    except Exception as e:
        return False, "Exception: "+str(e)
    try:
        f2 = codecs.open(blesseddir+"/"+stem+".out", encoding="utf8").read()
    except Exception as e:
        return False, "Exception: "+str(e)
    md5A = md5(f1.encode('utf8')).hexdigest()
    md5B = md5(f2.encode('utf8')).hexdigest()
    if len(f1) == 0 and len(f2) == 0:
        return True, "matchempty"
    if md5A != md5B:
        if len(f1) == 0:
            return False, "emptyoutput"
        elif len(f2) == 0:
            return False, "emptyreference"
        elif len(f1) > 0 and len(f2) > 0 and f1[0] == "{" and f2[0] == "{":
            try:            #   in case API returns invalid unicode!
                j1 = json.loads(f1)
            except UnicodeDecodeError:
                j1 = json.loads(f1.decode('latin-1'))
            try:
                j2 = json.loads(f2)
            except UnicodeDecodeError:
                j2 = json.loads(f2.decode('latin-1'))
            if "date" in j1.keys():
                j1["date"] = ""
            if "date" in j2.keys():
                j2["date"] = ""
            if j1 == j2:
                return True, "JSONmatch"
            else:
                fj1 = open(dir1+"/"+stem+".out1", "w")
                fj2 = open(dir1+"/"+stem+".out2", "w")
                fj1.write(json.dumps(j1, sort_keys=True))
                fj2.write(json.dumps(j2, sort_keys=True))
                fj1.close()
                fj2.close()
                if len(f1) == len(f2):
                    return True, "samesizeJSON".format(len(f1), len(f2))
                else:
                    return False, "JSONdiff {:d}, {:d}".format(len(f1), len(f2))
        else:
            return False, "diffnotjson, {:d}, {:d}".format(len(f1), len(f2))
    else:
        return True, "MD5match"

def run_tests(testlist):
    '''run tests for list of URIs in testlist'''

    result_hash = {}
    if JSON_FILE:
        result_hash["tests"] = {}
        result_hash["epoch_utc_start"] = time()
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
            if VERBOSE:
                print("trying", callhash, command)
            start = time()
            subprocess.call(str(command).split(), stdout=fout, shell=shell)
            elapsed = time() - start
            fout.close()
            ok, mesg = check_ok(callhash, WORKING, BLESSED)
            if JSON_FILE:
                result_hash["tests"][callhash] = {}
                result_hash["tests"][callhash]["status"] = ok
                result_hash["tests"][callhash]["call"] = call
                result_hash["tests"][callhash]["mesg"] = mesg
                result_hash["tests"][callhash]["time"] = elapsed
            else:
                if ok:
                    os.remove(fnout)
                else:
                    print("TESTFAIL", callhash, call, mesg)
            ftest = open(WORKING+"/"+callhash + ".test", "w")
            if VERBOSE:
                print("result: "+repr(ok)+mesg)
            ftest.write(repr(ok)+mesg+"\n")
            ftest.close()
            ftime = open(WORKING+"/"+callhash + ".time", "w")
            ftime.write(str(elapsed)+"\n")
            ftime.close()
        else:
            if VERBOSE:
                print("skipping", test[0])
    if JSON_FILE:
        result_hash["epoch_utc_end"] = time()
        with open(JSON_FILE, 'w') as outfile:
            json.dump(result_hash, outfile)

def get_example_calls(base_url):
    topleveljsonobjects = {}
    requestlist = []
    json_api_calls = obj_from_url(base_url)
    listofapiurls = [resources["url"]  for resources in json_api_calls["resources"]]
    for resourceurl in listofapiurls:
        if VERBOSE:
            sys.stderr.write("resourceurl: "+resourceurl+"\n")
        topleveljsonobjects[resourceurl] = obj_from_url(resourceurl)
    if VERBOSE:
        print "listofapiurls: ", listofapiurls
    for resource in listofapiurls:
        name = resource.split("/")[-1]
        for request in topleveljsonobjects[resource]["requests"]:
            if "example" in request.keys():
                n = request["name"]
                example = request["example"][0].replace("auth_key", "")
                callhash = md5(request["example"][0].encode('utf8')).hexdigest()
                requestlist.append((callhash, request["example"][0], name,
                                    request["name"], request["description"]))
    return requestlist

if __name__ == '__main__':
    usage = "usage: %prog \n  Tests MG-RAST API calls with example invokations in API"
    parser = argparse.ArgumentParser(usage)
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true",
                        default=False, help="Verbose")
    parser.add_argument("-j", "--jsonfile", dest="json_file", type=str,
                        default="", help="use output format JSON")
    parser.add_argument("-b", "--blesseddir", dest="blesseddir", type=str,
                        default="data", help="Location of stored (good) results")
    parser.add_argument("-w", "--workdingdir", dest="workingdir", type=str,
                        default=".", help="Working dir--will be filled with output files")
    parser.add_argument("-t", "--test", dest="tests", action="store_true",
                        default=False, help="don't do it, just print tests")
    parser.add_argument("-f", "--fast", dest="fast", action="store_true",
                        default=False, help="skip slow tests")

    opts = parser.parse_args()
    VERBOSE = opts.verbose
    BLESSED = opts.blesseddir
    WORKING = opts.workingdir
    TESTS = opts.tests
    FAST = opts.fast
    JSON_FILE = opts.json_file
    # create working dir if it does not exist
    if not os.path.isdir(WORKING):
        os.makedirs(WORKING)
    # get list of example API calls from API
    if VERBOSE:
        print("Fetching examples")
    tests = get_example_calls(API_URL)
    if  TESTS:
        print_tests(tests)
    else:
        run_tests(tests)
