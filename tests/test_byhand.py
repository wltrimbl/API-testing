from subprocess import check_output

# These tests should be quick

def test_utf8_project():
    a = check_output('''curl -s  'https://api.mg-rast.org/project/mgp128?verbosity=full' |file -''', shell=True)
    assert ("UTF-8" in a)

def test_utf8_metagenome_export():
    a = check_output('''curl -s 'https://api.mg-rast.org/metagenome/mgm4447943.3?verbosity=metadata' | file -''', shell=True)
    assert ("UTF-8" in a)

def test_utf8_metadata_export():
    a = check_output('''curl -s 'https://api.mg-rast.org/metadata/export/mgp128' | file -''', shell=True)
    assert ("UTF-8" in a)


def test_utf8_project_https():
    a = check_output('''curl -s  'https://api.mg-rast.org/project/mgp128?verbosity=full' |file -''', shell=True)
    assert ("UTF-8" in a)

def test_utf8_metagenome_export_https():
    a = check_output('''curl -s 'https://api.mg-rast.org/metagenome/mgm4447943.3?verbosity=metadata' | file -''', shell=True)
    assert ("UTF-8" in a)

def test_utf8_metadata_export_https():
    a = check_output('''curl -s 'https://api.mg-rast.org/metadata/export/mgp128' | file -''', shell=True)
    assert ("UTF-8" in a)

def test_download_partial():
    a = check_output('''curl -s 'https://api.mg-rast.org/download/mgm4447943.3?file=350.1' | head -n 100 ''', shell=True)
    assert "ERROR" not in a
    assert "GF8803K01A00MJ" in a

def test_annotation_similarity():
    URL = "https://api.metagenomics.anl.gov/annotation/similarity/mgm4447943.3?identity=80&type=function&source=KO"
    a = check_output('''curl -s '{}' | head -n 10 '''.format(URL), shell=True)
    assert "ERROR" not in a
    assert "\t" in a

def test_annotation_sequence():
    URL = "https://api.metagenomics.anl.gov/annotation/sequence/mgm4447943.3?evalue=10&type=organism&source=SwissProt"
    a = check_output('''curl -s '{}' | head -n 10 '''.format(URL), shell=True)
    assert "ERROR" not in a
    assert "\t" in a

def test_blast_result():
    URL = "https://api.metagenomics.anl.gov/compute/blast/mgm4447943.3?md5=0001c08aa276d154b7696f9758839786"
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert "ERROR" not in a
    assert "alignment" in a

#def test_post1(): 
#    CMD = '''curl -X POST -d '{"source":"KO","type":"function","md5s":["000821a2e2f63df1a3873e4b280002a8","15bf1950bd9867099e72ea6516e3d602"]}' "https://api.mg-rast.org/annotation/sequence/mgm4447943.3"'''     # EMPTY RETURN DATA 

def test_post2():
    CMD = '''curl -X POST -d '{"source":"SwissProt","type":"organism","md5s":["000821a2e2f63df1a3873e4b280002a8","15bf1950bd9867099e72ea6516e3d602"]}' "https://api.mg-rast.org/annotation/sequence/mgm4447943.3"'''
    a = check_output(CMD, shell=True)
    assert "ERROR" not in a

def test_errs_matrix_function():
    URL = "http://api.metagenomics.anl.gov/matrix/function?id=mgm4447943.3&id=mgm4447192.3&id=mgm4447102.3&group_level=level3&source=Subsystems&identity=80"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert "ERROR" not in a
def test_errs_profile():
    URL = "http://api.metagenomics.anl.gov/profile/mgm4447943.3?source=RefSeq&format=biom"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert "ERROR" not in a
def test_errs_matrix_organism():
    URL = "http://api.metagenomics.anl.gov/matrix/organism?id=mgm4447943.3&id=mgm4447192.3&id=mgm4447102.3&group_level=family&source=RefSeq&evalue=15"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert "ERROR" not in a
def test_errs_library():
    URL = "http://api.metagenomics.anl.gov/library/mgl52924?verbosity=full"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert "ERROR" not in a
def test_errs_metadata():
    URL = "http://api.metagenomics.anl.gov/metadata/ontology?name=biome&version=2017-04-15"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert "ERROR" not in a
def test_errs_darkmatter():
    URL = "http://api.metagenomics.anl.gov/darkmatter/mgm4447943.3?"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert "ERROR" not in a
def test_errs_download_history():
    URL = "http://api.metagenomics.anl.gov/download/history/mgm4447943.3"
    print(URL)
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert "ERROR" not in a

