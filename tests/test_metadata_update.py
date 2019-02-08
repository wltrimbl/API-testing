#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
from os.path import dirname, abspath
import json
from subprocess import check_output
import pytest
import requests
from test_byhand import read_api_list

DATADIR = dirname(abspath(__file__)) + "/data/"

APIS = read_api_list("API.server.list")
if 'MGRKEY' in os.environ:
    MGRKEY = os.environ['MGRKEY']
else:
    assert False, "This test does not work without MGRKEY"

def metadata_update(proj, filename, API_URL):
    h = check_output('curl -s -X POST -F "upload=@{FILENAME}" "{API_URL}/metadata/update" -H "Authorization: mgrast {MGRKEY}" -F "metagenome={METAGENOME}" -F "project={PROJECT}"'.format(FILENAME=filename, MGRKEY=MGRKEY, PROJECT=proj, METAGENOME="mgm4450397.3", API_URL=API_URL), shell=True)
    assert "ERROR" not in h.decode("utf-8")
    print(h)
    return(h)
#curl -X POST -F "upload=@FIXTURE-mgp28785-unicode.xlsx" "http://api.metagenomics.anl.gov/metadata/update" -H "Authorization: mgrast $MGRKEY"  -F "metagenome=mgm4514697.3" -F "project=mgp28785"

def metadata_import(proj, filename,API_URL):
    h = check_output('curl -s -X POST -F "upload=@{FILENAME}" "{API_URL}/metadata/import" -H "Authorization: mgrast {MGRKEY}" -F "metagenome=mgm4514697.3" -F "project={PROJECT}"'.format(FILENAME=filename, API_URL=API_URL, MGRKEY=MGRKEY, PROJECT=proj), shell=True)
    assert "ERROR" not in h.decode("utf-8")
    return(h)

#curl -X POST -F "upload=@mgp87606.xls" "http://api.metagenomics.anl.gov/metadata/validate"
def validate_metadata(filename,API_URL):
    h = check_output('curl -X POST -F "upload=@{FILENAME}" "{API_URL}/metadata/validate"'.format(FILENAME=filename, API_URL=API_URL), shell=True)
    return h

def get_proj_metadata(proj, field, API_URL):
    TESTURL = "{API_URL}/project/{PROJ}".format(API_URL=API_URL, PROJ=proj)
    TESTDATA = {"verbosity":"full", "nocache":1}
    TESTHEADERS = {"Authorization": "mgrast {MGRKEY}".format(MGRKEY=MGRKEY)}
#    print(TESTURL, TESTDATA, TESTHEADERS)
    a = requests.get(TESTURL, headers=TESTHEADERS, params=TESTDATA)
    aa = json.loads(a.content.decode("utf-8"))
    return(field, aa["metadata"][field])

def set_proj_metadata(proj, terms, API_URL):
    SETURL = API_URL + "/project/mgp119/updatemetadata"
    TESTHEADERS = {"Authorization": "mgrast {MGRKEY}".format(MGRKEY=MGRKEY)}
    # Convert data into the pecuilar syntax needed for requests.post to send
    # multipart/form-data without files:
    SETDATA = {k : (None, v)  for k, v in terms.items()}
#    print(SETURL, SETHEADERS, SETDATA)
    b = requests.post(SETURL, headers=TESTHEADERS, files=SETDATA)
    print(b.content.decode("utf-8"))

@pytest.mark.parametrize("API_URL", APIS)
@pytest.mark.requires_auth
@pytest.mark.utf8
def test_metadata_update_xls_nounicode(API_URL):
    FIXTURE = DATADIR+"/FIXTURE-mgp28785-nounicode.xlsx"
    PROJECT = "mgp28785"
    FIELD = "PI_organization_address"
    h = metadata_update(PROJECT, FIXTURE, API_URL)
    f, v = get_proj_metadata(PROJECT, FIELD, API_URL)
    print(f, v)
    assert v == "No unicode here."
    FIXTURE = DATADIR+"/FIXTURE-mgp28785-nounicode2.xlsx"
    PROJECT = "mgp28785"
    FIELD = "PI_organization_address"
    h = metadata_update(PROJECT, FIXTURE, API_URL)
    assert b"ERROR" not in h
    f, v = get_proj_metadata(PROJECT, FIELD, API_URL)
    print(f, v)
    assert v == "No unicode2 here."

@pytest.mark.requires_auth
@pytest.mark.parametrize("API_URL", APIS)
@pytest.mark.editutf8
def test_metadata_update_xls_unicode(API_URL):
    FIXTURE = DATADIR+"/FIXTURE-mgp28785-unicode.xlsx"
    PROJECT = "mgp28785"
    FIELD = "PI_organization_address"
    h = metadata_update(PROJECT, FIXTURE, API_URL)
    assert b"ERROR" not in h
    f, v = get_proj_metadata(PROJECT, FIELD, API_URL)
    print(f, v)
    assert v == "Unicóde test.  10μm in size.   CJK unlikely to work here."

@pytest.mark.utf8
@pytest.mark.parametrize("API_URL", APIS)
def test_metadata_validate_xls_nounicode(API_URL):
    FIXTURE = DATADIR+"/FIXTURE-mgp28785-nounicode.xlsx"
    h = validate_metadata(FIXTURE, API_URL)
    print(h)
    assert b"authentication failed" not in h
    j = json.loads(h.decode("utf-8"))
    assert j["is_valid"] == 1

@pytest.mark.utf8
@pytest.mark.parametrize("API_URL", APIS)
def test_metadata_validate_xls_unicode(API_URL):
    FIXTURE = DATADIR +"/FIXTURE-mgp28785-unicode.xlsx"
    h = validate_metadata(FIXTURE, API_URL)
    print(h)
    assert b"authentication failed" not in h
    j = json.loads(h.decode("utf-8"))
    assert j["is_valid"] == 1
