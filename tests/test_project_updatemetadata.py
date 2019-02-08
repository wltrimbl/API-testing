#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import json
import requests
import pytest

if 'MGRKEY' in os.environ:
    MGRKEY = os.environ['MGRKEY']
else:
    assert False, "This test does not work without MGRKEY"

API_URL = "https://api.mg-rast.org/"

def get_proj_metadata(proj, field):
    '''Connect to MG-RAST API, authorize, and read project metadata.'''
    TESTURL = API_URL + "/project/{PROJ}".format(PROJ=proj)
    TESTDATA = {"verbosity":"full", "nocache":1}
    TESTHEADERS = {"Authorization": "mgrast {MGRKEY}".format(MGRKEY=MGRKEY)}
#    print(TESTURL, TESTDATA, TESTHEADERS)
    a = requests.get(TESTURL, headers=TESTHEADERS, params=TESTDATA)
    aa = json.loads(a.content.decode("utf-8"))
    assert "ERROR" not in a.content.decode("utf-8")
    return(field, aa["metadata"][field])

@pytest.mark.requires_auth
def set_proj_metadata(proj, terms):
    '''Connect to MG-RAST API, authorize, and change one or more fields
    of project metadata.'''
    SETURL = API_URL + "/project/{PROJ}/updatemetadata".format(PROJ=proj)
    SETHEADERS = {"Authorization": "mgrast {MGRKEY}".format(MGRKEY=MGRKEY)}
    # Convert data into the pecuilar syntax needed for requests.post to send
    # multipart/form-data without files:
    SETDATA = {key : (None, val)  for key, val in terms.items()}
#    print(SETURL, SETHEADERS, SETDATA)
    b = requests.post(SETURL, headers=SETHEADERS, files=SETDATA)
    print(b.content.decode("utf-8"))

@pytest.mark.requires_auth
def test_project_updatemetadata():
    '''Update a field of project metadata, confirm its value,
    update it again (with utf-8) and confirm its value.'''
    PROJECT = "mgp34834"  # This is a garbage project
    FIELD = "organization_url"
    set_proj_metadata(PROJECT, {FIELD: "TESTING"})
    f, v = get_proj_metadata(PROJECT, FIELD)
    print(f, v)
    assert v == "TESTING"
    set_proj_metadata(PROJECT, {FIELD: "TESTING2"})
    f, v = get_proj_metadata(PROJECT, FIELD)
    print(f, v)
    assert v == "TESTING2"

@pytest.mark.requires_auth
@pytest.mark.editutf8
def test_project_updatemetadata_with_utf8():
    '''Update a field of project metadata, confirm its value,
    update it again (with utf-8) and confirm its value.'''
    PROJECT = "mgp34834"  # This is a garbage project
    FIELD = "organization_url"
    set_proj_metadata(PROJECT, {FIELD: "TESTING"})
    f, v = get_proj_metadata(PROJECT, FIELD)
    print(f, v)
    assert v == "TESTING"
    set_proj_metadata(PROJECT, {FIELD: "TESTING2"})
    f, v = get_proj_metadata(PROJECT, FIELD)
    print(f, v)
    assert v == "TESTING2"
    set_proj_metadata(PROJECT, {FIELD: "Tésting2"})
    f, v = get_proj_metadata(PROJECT, FIELD)
    print(f, v)
    assert v == "Tésting2"
