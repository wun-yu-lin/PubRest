##test
from api_package import api_pubchem

cid_key = 2244
api_pubchem.get_SDF_by_cid(cid_key=2244)

for x in range(1,1000):
    api_pubchem.get_SDF_by_cid(cid_key=x)