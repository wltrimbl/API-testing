import os
from subprocess import check_output
import pytest

# These tests should be quick

# Rotate through API servers listed in API.server.list

def read_api_list(filename):
    server_list = []
    if not os.path.isfile(filename):
        return ["http://api.mg-rast.org", "https://api.mg-rast.org"]
    for l in open(filename).readlines():
        server_list.append(l.strip())
    return server_list

APIS = read_api_list("API.server.list")

@pytest.mark.parametrize("API_URL", APIS)
def test_utf8_project(API_URL):
    URL = API_URL + '/project/mgp128?verbosity=full'
    a = check_output('''curl -s '{}' |file -'''.format(URL), shell=True)
    assert b"UTF-8" in a

@pytest.mark.parametrize("API_URL", APIS)
def test_utf8_metagenome_export(API_URL):
    URL = API_URL + "/metagenome/mgm4447943.3?verbosity=metadata"
    a = check_output('''curl -s '{}' | file -'''.format(URL), shell=True)
    assert b"UTF-8" in a

@pytest.mark.parametrize("API_URL", APIS)
def test_utf8_metadata_export(API_URL):
    URL = API_URL + "/metadata/export/mgp128"
    a = check_output('''curl -s '{}' | file -'''.format(URL), shell=True)
    assert b"UTF-8" in a

@pytest.mark.parametrize("API_URL", APIS)
def test_download_partial(API_URL):
    URL = API_URL + "/download/mgm4447943.3?file=350.1"
    a = check_output('''curl -s '{}' | head -n 100 '''.format(URL), shell=True)
    assert b"ERROR" not in a
    assert b"GF8803K01A00MJ" in a

@pytest.mark.parametrize("API_URL", APIS)
def test_annotation_similarity(API_URL):
    URL = API_URL + "/annotation/similarity/mgm4447943.3?identity=80&type=function&source=KO"
    a = check_output('''curl -s '{}' | head -n 10 '''.format(URL), shell=True)
    assert b"ERROR" not in a
    assert b"\t" in a

@pytest.mark.parametrize("API_URL", APIS)
def test_annotation_sequence(API_URL):
    URL = API_URL + "/annotation/sequence/mgm4447943.3?evalue=10&type=organism&source=SwissProt"
    a = check_output('''curl -s '{}' | head -n 10 '''.format(URL), shell=True)
    assert b"ERROR" not in a
    assert b"\t" in a

@pytest.mark.parametrize("API_URL", APIS)
def test_blast_result_http(API_URL):
    URL = API_URL + "/compute/blast/mgm4447943.3?md5=0001c08aa276d154b7696f9758839786"
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert b"ERROR" not in a
    assert b"alignment" in a

@pytest.mark.parametrize("API_URL", APIS)
def test_blast_result_https(API_URL):
    URL = API_URL + "/compute/blast/mgm4447943.3?md5=0001c08aa276d154b7696f9758839786"
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert b"ERROR" not in a
    assert b"alignment" in a

#def test_post1(API_URL):
#    CMD = '''curl -X POST -d '{"source":"KO","type":"function","md5s":["000821a2e2f63df1a3873e4b280002a8","15bf1950bd9867099e72ea6516e3d602"]}' "https://api.mg-rast.org/annotation/sequence/mgm4447943.3"'''     # EMPTY RETURN DATA

@pytest.mark.parametrize("API_URL", APIS)
def test_post2(API_URL):
    URL = API_URL + "/annotation/sequence/mgm4447943.3"
    CMD = '''curl -s -X POST -d '{"source":"SwissProt","type":"organism","md5s":["000821a2e2f63df1a3873e4b280002a8","15bf1950bd9867099e72ea6516e3d602"]}' "''' + API_URL + '''"'''
    a = check_output(CMD, shell=True)
    assert b"ERROR" not in a

@pytest.mark.parametrize("API_URL", APIS)
def test_errs_matrix_function(API_URL):
    URL = API_URL + "/matrix/function?id=mgm4447943.3&id=mgm4447192.3&id=mgm4447102.3&group_level=level3&source=Subsystems&identity=80"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert b"ERROR" not in a
@pytest.mark.parametrize("API_URL", APIS)
def test_errs_profile(API_URL):
    URL = API_URL + "/profile/mgm4447943.3?source=RefSeq&format=biom"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert b"ERROR" not in a
@pytest.mark.parametrize("API_URL", APIS)
def test_errs_matrix_organism(API_URL):
    URL = API_URL + "/matrix/organism?id=mgm4447943.3&id=mgm4447192.3&id=mgm4447102.3&group_level=family&source=RefSeq&evalue=15"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert b"ERROR" not in a
@pytest.mark.parametrize("API_URL", APIS)
def test_errs_library(API_URL):
    URL = API_URL + "/library/mgl52924?verbosity=full"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert b"ERROR" not in a
@pytest.mark.parametrize("API_URL", APIS)
def test_errs_metadata(API_URL):
    URL = API_URL + "/metadata/ontology?name=biome&version=2017-04-15"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert b"ERROR" not in a
@pytest.mark.parametrize("API_URL", APIS)
def test_errs_darkmatter(API_URL):
    URL = API_URL + "/darkmatter/mgm4447943.3?"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert b"ERROR" not in a
@pytest.mark.parametrize("API_URL", APIS)
def test_errs_download_history(API_URL):
    URL = API_URL + "/download/history/mgm4447943.3"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert b"ERROR" not in a

