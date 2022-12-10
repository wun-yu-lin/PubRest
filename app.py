##test
from api_package import api_pubchem




cid_key = 2244

path = "{cid_key_str}.sdf".format(cid_key_str = str(cid_key))
with open(path, 'w') as f:
    f.write(str(api_pubchem.get_SDF_by_cid(cid_key=2244)))