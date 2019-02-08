import os
import json
from subprocess import check_output
import pytest

from test_byhand import read_api_list

if 'MGRKEY' in os.environ:
    MGRKEY = os.environ['MGRKEY']
else:
    assert False, "This test does not work without MGRKEY"

APIS = read_api_list("API.server.list")

@pytest.mark.requires_auth
@pytest.mark.editutf8
@pytest.mark.parametrize("API_URL", APIS)
def test_setusername(API_URL):
    CMD = '''curl -s -X PUT '{API_URL}/user/wltrimbl3' -d "firstname=Fool" -d "lastname=Trimble dépr" -d "email2=" -d email="effectivewindow@hotmail.com"  -H "Authorization: mgrast {MGRKEY}"  | jq .'''.format(API_URL=API_URL, MGRKEY=MGRKEY)
    print(CMD)
    o = check_output(CMD, shell=True)
    print(o)
    assert b"ERROR" not in o
    j = json.loads(o)
    assert j["lastname"] == "Trimble dépr"  # unicode in json response
    CMD = '''curl -s -X GET '{API_URL}/user/wltrimbl3' -H "Authorization: mgrast {MGRKEY}"  | jq .'''.format(API_URL=API_URL, MGRKEY=MGRKEY)
    o = check_output(CMD, shell=True)
    print(o)
    assert b"ERROR" not in o
    j = json.loads(o)
    assert j["lastname"] == "Trimble dépr"  # unicode in follow-up query for user data
