import json
import logging
import sys
import time
import urllib.request

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
def get_SDF_by_cid (domain="compound", namespace= "cid", cid_key = 1, ):
    if isinstance(cid_key, int) == False:
        ValueError('please input CID (positive integer)')
        return
    cid_key_str = str(cid_key)
    # Make request
    symbol = "/"
    
    apiurl = symbol.join((API_BASE,domain,namespace,cid_key_str,"SDF"))
    print(apiurl)
    try:
        log.debug('Request URL: %s', apiurl)
        with urllib.request.urlopen(apiurl) as response:
            data = response.read().decode()
        return data
    except HTTPError as e:
        ValueError("HTTPError")
    
    
get_SDF_by_cid(cid_key=2244)