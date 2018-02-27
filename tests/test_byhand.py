from subprocess import check_output

# These tests should be quick

API_URL = "http://api.mg-rast.org/"
API_URL_NOHTTPS = "https://api.mg-rast.org/"

def test_utf8_project():
    URL = API_URL_NOHTTPS + '/project/mgp128?verbosity=full'
    a = check_output('''curl -s  '{}' |file -'''.format(URL), shell=True)
    assert ("UTF-8" in a)

def test_utf8_metagenome_export():
    URL = API_URL_NOHTTPS + "/metagenome/mgm4447943.3?verbosity=metadata" 
    a = check_output('''curl -s '{}' | file -'''.format(URL), shell=True)
    assert ("UTF-8" in a)

def test_utf8_metadata_export():
    URL = API_URL_NOHTTPS + "/metadata/export/mgp128"
    a = check_output('''curl -s '{}' | file -'''.format(URL), shell=True)
    assert ("UTF-8" in a)

def test_utf8_project_https():
    URL = API_URL + "/project/mgp128?verbosity=full"
    a = check_output('''curl -s  '{}' |file -'''.format(URL), shell=True)
    assert ("UTF-8" in a)

def test_utf8_metagenome_export_https():
    URL = API_URL + "/metagenome/mgm4447943.3?verbosity=metadata"
    a = check_output('''curl -s '{}' | file -'''.format(URL), shell=True)
    assert ("UTF-8" in a)

def test_utf8_metadata_export_https():
    URL = API_URL + "/metadata/export/mgp128"
    a = check_output('''curl -s '{}' | file -'''.format(URL), shell=True)
    assert ("UTF-8" in a)

def test_download_partial():
    URL = API_URL + "/download/mgm4447943.3?file=350.1"
    a = check_output('''curl -s '{}' | head -n 100 '''.format(URL), shell=True)
    assert "ERROR" not in a
    assert "GF8803K01A00MJ" in a

def test_annotation_similarity():
    URL = API_URL + "/annotation/similarity/mgm4447943.3?identity=80&type=function&source=KO"
    a = check_output('''curl -s '{}' | head -n 10 '''.format(URL), shell=True)
    assert "ERROR" not in a
    assert "\t" in a

def test_annotation_sequence():
    URL = API_URL + "/annotation/sequence/mgm4447943.3?evalue=10&type=organism&source=SwissProt"
    a = check_output('''curl -s '{}' | head -n 10 '''.format(URL), shell=True)
    assert "ERROR" not in a
    assert "\t" in a

def test_blast_result_http():
    URL = API_URL + "/compute/blast/mgm4447943.3?md5=0001c08aa276d154b7696f9758839786"
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert "ERROR" not in a
    assert "alignment" in a

def test_blast_result_https():
    URL = API_URL + "/compute/blast/mgm4447943.3?md5=0001c08aa276d154b7696f9758839786"
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert "ERROR" not in a
    assert "alignment" in a

#def test_post1(): 
#    CMD = '''curl -X POST -d '{"source":"KO","type":"function","md5s":["000821a2e2f63df1a3873e4b280002a8","15bf1950bd9867099e72ea6516e3d602"]}' "https://api.mg-rast.org/annotation/sequence/mgm4447943.3"'''     # EMPTY RETURN DATA 

def test_post2():
    URL = API_URL + "/annotation/sequence/mgm4447943.3"
    CMD = '''curl -X POST -d '{"source":"SwissProt","type":"organism","md5s":["000821a2e2f63df1a3873e4b280002a8","15bf1950bd9867099e72ea6516e3d602"]}' "''' + API_URL + '''"'''
    a = check_output(CMD, shell=True)
    assert "ERROR" not in a

def test_errs_matrix_function():
    URL = API_URL + "/matrix/function?id=mgm4447943.3&id=mgm4447192.3&id=mgm4447102.3&group_level=level3&source=Subsystems&identity=80"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert "ERROR" not in a
def test_errs_profile():
    URL = API_URL + "/profile/mgm4447943.3?source=RefSeq&format=biom"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert "ERROR" not in a
def test_errs_matrix_organism():
    URL = API_URL + "/matrix/organism?id=mgm4447943.3&id=mgm4447192.3&id=mgm4447102.3&group_level=family&source=RefSeq&evalue=15"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert "ERROR" not in a
def test_errs_library():
    URL = API_URL + "/library/mgl52924?verbosity=full"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert "ERROR" not in a
def test_errs_metadata():
    URL = API_URL + "/metadata/ontology?name=biome&version=2017-04-15"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert "ERROR" not in a
def test_errs_darkmatter():
    URL = API_URL + "/darkmatter/mgm4447943.3?"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert "ERROR" not in a
def test_errs_download_history():
    URL = API_URL + "/download/history/mgm4447943.3"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert "ERROR" not in a

