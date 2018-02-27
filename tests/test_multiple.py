import pytest 
from subprocess import check_output

#  This test was noted failing for some backend API servers but not others
#  Rotate through list of backend server hosts:ports in API.server.list
#  with paramterized tests

def read_api_list(filename):
    server_list = []
    for l in open(filename).readlines():
        server_list.append(l.strip())
    return(server_list)


APIS = read_api_list("API.server.list")
print(APIS)

@pytest.mark.parametrize("API_URL", APIS)
def test_blast_result_http(API_URL):
    URL = API_URL + "/compute/blast/mgm4447943.3?md5=0001c08aa276d154b7696f9758839786"
    a = check_output('''curl -s '{}' '''.format(URL), shell=True)
    assert "ERROR" not in a
    assert "alignment" in a

