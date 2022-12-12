import logging
import urllib.request
import os
from pathlib import Path

try:
    from urllib.error import HTTPError
    from urllib.parse import quote, urlencode
    
except ImportError:
    from urllib import urlencode
    from urllib import quote, urlopen, HTTPError
    
__author__ = 'Wunyu'
__email__ = 'secret'
__version__ = '1.0.0'
__license__ = 'NCHU'

API_BASE = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug'
log = logging.getLogger('pubRest')
log.addHandler(logging.NullHandler())

    
##https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/SDF

def get_SDF_by_cid (domain="compound", namespace= "cid", cid_key = 1,path="./sdf" ):
    if isinstance(cid_key, int) == False:
        ValueError('please input CID (positive integer)')
        return
    cid_key_str = str(cid_key)
    # Make request
    symbol = "/"
    
    apiurl = symbol.join((API_BASE,domain,namespace,cid_key_str,"SDF"))
    
    
    ##if folder not exist, create folder
    p = Path(path)
    if(p.exists()==False):
        os.mkdir(path)
        
    
    
    ##print(apiurl)
    try:
        log.debug('Request URL: %s', apiurl)
        with urllib.request.urlopen(apiurl) as response:
            data_undecode = response.read()
            data = data_undecode.decode()
            #get compound name
            index = 0
            for x in data_undecode.splitlines():
                index+=1

                if (str(x)=="b'> <PUBCHEM_IUPAC_CAS_NAME>'"):
                   compoundName = str(data_undecode.splitlines()[index]).split("'")[1]
            
        
        
        data_path = "{path}/{cid_key_str}_{compoundName}.sdf".format(path=str(path),cid_key_str = str(cid_key), compoundName =str(compoundName))
        with open(data_path, 'w') as f:
            f.write(str(data))
        
        
        
        
        
        return data
    except HTTPError as e:
        ValueError("HTTPError")
    
    




##test function
get_SDF_by_cid(cid_key=2244)