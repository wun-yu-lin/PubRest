
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

import functools
import json
import logging
import os
import sys
import time
import warnings
import binascii

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


def request(identifier, namespace='cid', domain='compound', operation=None, output='JSON', searchtype=None, **kwargs):
    """
    Construct API request from parameters and return the response.

    Full specification at http://pubchem.ncbi.nlm.nih.gov/pug_rest/PUG_REST.html
    """
    if sys.version_info[0] == 3:
        text_types = str, bytes
    else:
        text_types = basestring
        
    try:
        if isinstance(identifier, int):
            identifier = str(identifier)
        if not isinstance(identifier, text_types):
            identifier = ','.join(str(x) for x in identifier)
    except:
        ValueError('please check your parameter is current')
        
    #Filter None Values from kwargs
    kwargs = dict((i,j) for i, j in kwargs.items() if i is not None)
    
    #construct API Url endpoint
    urlid = None
    postData = None
    try:
        if namespace == 'sourceid':
            identifier = identifier.replace('/', '.')
        if namespace in ['listkey', 'formula', 'sourceid'] or searchtype == 'xref' or (searchtype and namespace == 'cid') or domain == 'sources':
            urlid = quote(identifier.encode('utf8'))
        else:
            postdata = urlencode([(namespace, identifier)]).encode('utf8')
        
        ##create url from parameter
        comps = filter(None, [API_BASE, domain, searchtype, namespace, urlid, operation, output])
        apiurl = '/'.join(comps)
    except:
        ValueError('please check your parameter is current')
       
    #if have parameter in kwargs, join to apiurl
    if kwargs:
        apiurl += '?%s' % urlencode(kwargs)
        
    # Make request
    try:
        log.debug('Request URL: %s', apiurl)
        log.debug('Request data: %s', postdata)
        response = urlopen(apiurl, postdata)
        return response
    except HTTPError as e:
        raise PubRestHTTPError(e)
    
def get(identifier, namespace='cid', domain='compound', operation=None, output='JSON', searchtype=None, **kwargs):
    """Request wrapper that automatically handles async requests."""
    if (searchtype and searchtype != 'xref') or namespace in ['formula']:
        response = request(identifier, namespace, domain, None, 'JSON', searchtype, **kwargs).read()
        status = json.loads(response.decode())
        if 'Waiting' in status and 'ListKey' in status['Waiting']:
            identifier = status['Waiting']['ListKey']
            namespace = 'listkey'
            while 'Waiting' in status and 'ListKey' in status['Waiting']:
                time.sleep(2)
                response = request(identifier, namespace, domain, operation, 'JSON', **kwargs).read()
                status = json.loads(response.decode())
            if not output == 'JSON':
                response = request(identifier, namespace, domain, operation, output, searchtype, **kwargs).read()
    else:
        response = request(identifier, namespace, domain, operation, output, searchtype, **kwargs).read()
    return response
        
    
def get_json(identifier, namespace='cid', domain='compound', operation=None, searchtype=None, **kwargs):
    """Request wrapper that automatically parses JSON response and supresses NotFoundError."""
    try:
        return json.loads(get(identifier, namespace, domain, operation, 'JSON', searchtype, **kwargs).decode())
    except NotFoundError as e:
        log.info(e)
        return None

def get_sdf(identifier, namespace='cid', domain='compound',operation=None, searchtype=None, **kwargs):
    """Request wrapper that automatically parses SDF response and supresses NotFoundError."""
    try:
        return get(identifier, namespace, domain, operation, 'SDF', searchtype, **kwargs).decode()
    except NotFoundError as e:
        log.info(e)
        return None    
    
    
    
class PubRestDeprecationWarning(Warning):
    """Warning category for deprecated features."""
    pass


class PubRestError(Exception):
    """Base class for all PubRest exceptions."""
    pass


class ResponseParseError(PubRestError):
    """PubRest response is uninterpretable."""
    pass


class PubRestHTTPError(PubRestError):
    """Generic error class to handle all HTTP error codes."""
    def __init__(self, e):
        self.code = e.code
        self.msg = e.reason
        try:
            self.msg += ': %s' % json.loads(e.read().decode())['Fault']['Details'][0]
        except (ValueError, IndexError, KeyError):
            pass
        if self.code == 400:
            raise BadRequestError(self.msg)
        elif self.code == 404:
            raise NotFoundError(self.msg)
        elif self.code == 405:
            raise MethodNotAllowedError(self.msg)
        elif self.code == 504:
            raise TimeoutError(self.msg)
        elif self.code == 501:
            raise UnimplementedError(self.msg)
        elif self.code == 500:
            raise ServerError(self.msg)

    def __str__(self):
        return repr(self.msg)


class BadRequestError(PubRestHTTPError):
    """Request is improperly formed (syntax error in the URL, POST body, etc.)."""
    def __init__(self, msg='Request is improperly formed'):
        self.msg = msg


class NotFoundError(PubRestHTTPError):
    """The input record was not found (e.g. invalid CID)."""
    def __init__(self, msg='The input record was not found'):
        self.msg = msg


class MethodNotAllowedError(PubRestHTTPError):
    """Request not allowed (such as invalid MIME type in the HTTP Accept header)."""
    def __init__(self, msg='Request not allowed'):
        self.msg = msg


class TimeoutError(PubRestHTTPError):
    """The request timed out, from server overload or too broad a request.

    See :ref:`Avoiding TimeoutError <avoiding_timeouterror>` for more information.
    """
    def __init__(self, msg='The request timed out'):
        self.msg = msg


class UnimplementedError(PubRestHTTPError):
    """The requested operation has not (yet) been implemented by the server."""
    def __init__(self, msg='The requested operation has not been implemented'):
        self.msg = msg


class ServerError(PubRestHTTPError):
    """Some problem on the server side (such as a database server down, etc.)."""
    def __init__(self, msg='Some problem on the server side'):
        self.msg = msg

