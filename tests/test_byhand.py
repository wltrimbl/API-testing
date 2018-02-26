from subprocess import check_output
def test_utf8_project():
    a = check_output('''curl -s  'http://api.mg-rast.org/project/mgp128?verbosity=full' |file -''', shell=True)
    assert ("UTF-8" in a)

def test_utf8_metagenome_export():
    a = check_output('''curl -s 'http://api.mg-rast.org/metagenome/mgm4447943.3?verbosity=metadata' | file -''', shell=True)
    assert ("UTF-8" in a)

def test_utf8_metadata_export():
    a = check_output('''curl -s 'http://api.mg-rast.org/metadata/export/mgp128' | file -''', shell=True)
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

