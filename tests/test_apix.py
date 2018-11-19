import os
from subprocess import check_output
import pytest

# subset of ~20 example invokations from the API-explorer page  (all GET)
# http://www.mg-rast.org/mgmain.html?mgpage=api 
# mangled by hand into 

def test_apix_annotation_similarity():
    CALL = '''curl 'http://api-ui.mg-rast.org/annotation/similarity/mgm4447943.3?id=mgm4447943.3&identity=80&no_cutoffs=0&source=KO&type=function' | head  '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a

#def test_apix_compute_alpha2():
#    CALL = '''curl 'http://api-ui.mg-rast.org/compute/alphadiversity/mgm4447943.3?id=mgm4447943.3&asynchronous=0&level=order' '''
#    a = check_output(CALL, shell=True)
#    assert not b"ERROR" in a
def test_apix3():
    CALL = '''curl 'http://api-ui.mg-rast.org/compute/blast/mgm4447943.3?id=mgm4447943.3&asynchronous=0&md5=0001c08aa276d154b7696f9758839786&rna=0' | head '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a
def test_apix_darkmatter_id():
    CALL = '''curl 'http://api-ui.mg-rast.org/darkmatter/mgm4447943.3?id=mgm4447943.3' | head '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a
def test_apix_download_id_350():
    CALL = '''curl 'http://api-ui.mg-rast.org/download/mgm4447943.3?id=mgm4447943.3&file=350.1&link=0' | head '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a

def test_apix_download_history():
    CALL = '''curl 'http://api-ui.mg-rast.org/download/history/mgm4447943.3?id=mgm4447943.3&delete=0&force=0' | head '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a
def test_apix_download():
    CALL = '''curl 'http://api-ui.mg-rast.org/download/mgm4447943.3?id=mgm4447943.3&stage=650' | head '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a
def test_apix_m5nr_accession():
    CALL = '''curl 'http://api-ui.mg-rast.org/m5nr/accession/YP_003268079.1?id=YP_003268079.1' | head '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a
def test_apix_m5nr_md5():
    CALL = '''curl 'http://api-ui.mg-rast.org/m5nr/md5/000821a2e2f63df1a3873e4b280002a8?id=000821a2e2f63df1a3873e4b280002a8&format=fasta&sequence=0&source=RefSeq' | head '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a
def test_apix_m5nr_function():
    CALL = '''curl 'http://api-ui.mg-rast.org/m5nr/function/sulfatase?text=sulfatase&exact=0&id_only=0&inverse=0&source=GenBank' '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a
def test_apix_m5nr_organism():
    CALL = '''curl 'http://api-ui.mg-rast.org/m5nr/organism/akkermansia?text=akkermansia&exact=0&inverse=0&source=KEGG&tax_level=strain' '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a
def test_apix12():
    CALL = '''curl 'http://api-ui.mg-rast.org/m5nr/sequence/MSTAITRQIVLDTETTGMNQIGAHYEGHKIIEIGAVEVVNRRLTGNNFHVYLKPDRLVDPEAFGVHGIADEFLLDKPTFAEVADEFMDYIRGAELVIHNAAFDIGFMDYEFSLLKRDIPKTNTFCKVTDSLAVARKMFPGKRNSLDALCARYEIDNSKRTLHGALLDAQILAEVYLAMTGGQTSMAFAMEGETQQQQGEATIQRIVRQASKLRVVFATDEEIAAHEARLDLVQKKGGSCLWRA?text=MSTAITRQIVLDTETTGMNQIGAHYEGHKIIEIGAVEVVNRRLTGNNFHVYLKPDRLVDPEAFGVHGIADEFLLDKPTFAEVADEFMDYIRGAELVIHNAAFDIGFMDYEFSLLKRDIPKTNTFCKVTDSLAVARKMFPGKRNSLDALCARYEIDNSKRTLHGALLDAQILAEVYLAMTGGQTSMAFAMEGETQQQQGEATIQRIVRQASKLRVVFATDEEIAAHEARLDLVQKKGGSCLWRA&source=TrEMBL' '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a
def test_apix_m5nr_function_id_POST():
    CALL = '''curl -d '{"compress":0,"data":["2442,5432"]}' 'http://api-ui.mg-rast.org/m5nr/function_id' '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a
def test_apix_m5nr_organism_POST():
    CALL = '''curl -d '{"data":["akkermansia,yersinia"],"exact":0,"inverse":0,"order":"accession","source":"KEGG","tax_level":"strain"}' 'http://api-ui.mg-rast.org/m5nr/organism' '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a
def test_apix_m5nr_sequence_POST():
    CALL = '''curl 'http://api-ui.mg-rast.org/m5nr/sequence' -d '{"data": ["MAGENHQWQGSIL","MAGENHQWQGSIL"]}' '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a
def test_apix_matrix_organism():
    CALL = '''curl 'http://api-ui.mg-rast.org/matrix/organism?id=mgm4447943.3&id=mgm4447192.3&id=mgm4447102.3&evalue=15&filter_level=function&filter_source=Subsystems&group_level=family&hide_metadata=0&hit_type=all&result_type=abundance&source=RefSeq' '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a
def test_apix_matrix_function():
    CALL = '''curl 'http://api-ui.mg-rast.org/matrix/function?id=mgm4447943.3&id=mgm4447192.3&id=mgm4447102.3&filter_level=strain&filter_source=RefSeq&group_level=level3&hide_metadata=0&identity=80&result_type=abundance&source=Subsystems' '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a
def test_apix_export_project():
    CALL = '''curl 'http://api-ui.mg-rast.org/metadata/export/mgp128?id=mgp128' '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a
def test_apix_metagenome_search():
    CALL = '''curl 'http://api-ui.mg-rast.org/metagenome?direction=asc&limit=20&match=all&order=name&status=both&verbosity=minimal' '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a
def test_apix_metagenome():
    CALL = '''curl 'http://api-ui.mg-rast.org/metagenome/mgm4447943.3?id=mgm4447943.3&nocache=0&verbosity=metadata' '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a
def test_apix_project_search():
    CALL = '''curl 'http://api-ui.mg-rast.org/project?limit=20&order=name&verbosity=minimal' '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a
def test_apix_project_mgp128():
    CALL = '''curl 'http://api-ui.mg-rast.org/project/mgp128?id=mgp128&verbosity=full' '''
    a = check_output(CALL, shell=True)
    assert not b"ERROR" in a

