#!/usr/bin/python

import sys
import time
import random
import zlib
import urllib
import M2Crypto
import logging
import uuid
from datetime import datetime
from dateutil import parser as dt_parser
from dateutil.tz import tzutc
from hashlib import sha1
from base64 import b64decode, b64encode
try:
    import xml.etree.ElementTree as ElementTree
except:
    from elementtree import ElementTree


logger = logging.getLogger(__name__)

# seconds to cache ID for replay
replay_cache_lifetime = 3600

# seconds from IssueInstant where the Response is valid
response_window = 300

# xml namespaces for xpath
ns = {'saml2p': '{urn:oasis:names:tc:SAML:2.0:protocol}',
      'saml2': '{urn:oasis:names:tc:SAML:2.0:assertion}',
      'ds': '{http://www.w3.org/2000/09/xmldsig#}',
      'xs' : '{http://www.w3.org/2001/XMLSchema}',
      'ec' : '{http://www.w3.org/2001/10/xml-exc-c14n#}',
      'xsi' : '{http://www.w3.org/2001/XMLSchema-instance}',
    }

# xpath strings
xp_subject_nameid = '{saml2}Assertion/{saml2}Subject/{saml2}NameID' #.format(**ns)
xp_attributestatement= '{saml2}Assertion/{saml2}AttributeStatement' #.format(**ns)

# we only support the HTTP-POST-SimpleSign binding
HTTP_POST_SimpleSign = 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST-SimpleSign'

# SAML2 AuthnRequest template
authnRequest = ('<?xml version="1.0" encoding="UTF-8"?>'
                '<samlp:AuthnRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol" '
                    'AssertionConsumerServiceURL="{ACS}" '
                    'Destination="{SingleSignOnService}" ' 
                    'ID="{RequestID}" '
                    'IssueInstant="{IssueInstant}" '
                    'ProtocolBinding="{Binding}" '
                    'Version="2.0">'
                '<saml:Issuer xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">'
                '{entityID}'
                '</saml:Issuer>'
                '<samlp:NameIDPolicy AllowCreate="1"/>'
                '{Signature}'
                '</samlp:AuthnRequest>')

sigtmpl = ('<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">'
           '<ds:SignedInfo>'
           '<ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>'
           '<ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>'
           '<ds:Reference URI="#%s">'
           '<ds:Transforms>'
           '<ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>'
           '<ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>'
           '</ds:Transforms>'
           '<ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>'
           '<ds:DigestValue>a1BFjLwXF44t+Hr8qpUK5STGJ7s=</ds:DigestValue>'
           '</ds:Reference>'
           '</ds:SignedInfo>'
           '<ds:SignatureValue>'
           'VFoZqLOjlhf66EnlYsgNN+8JgSk525gKjBW+kIqL/RUT0o+GHOXsLmzESA5MkxGM5MNkzcWFnfQT'
           'FBxRJsPW+72crC1S2W7ddC4qE6pD9vZtrrZYM/E2jMOy0+ZAoUwtRxJiZ8ykwiENxLLKItjwJVqy'
           'KO9s/yet8LpqUgaqlIs='
           '</ds:SignatureValue>'
           '<ds:KeyInfo>'
           '<ds:X509Data>'
           '<ds:X509Certificate>'
           'MIIEPjCCAyagAwIBAgICAhcwDQYJKoZIhvcNAQEFBQAwSTELMAkGA1UEBhMCRlIxGDAWBgNVBAoM'
           'D094eWxhbmUgUFJFUFJPRDEgMB4GA1UEAwwXR3JvdXAgU2VydmVyIENBIFBSRVBST0QwHhcNMTAw'
           'MjA5MTQzMDM1WhcNMTMwMjA5MTQzMDM1WjBGMQswCQYDVQQGEwJGUjEQMA4GA1UECgwHT3h5bGFu'
           'ZTENMAsGA1UECwwET1hJVDEWMBQGA1UEAwwNKi5wcmVwcm9kLm9yZzCBnzANBgkqhkiG9w0BAQEF'
           'AAOBjQAwgYkCgYEAptuIQdNG/m8vgMD/gcI9LGMIKjNhePjlSyIhNWrPbsvAvizshZsOTqI/5bXh'
           'Elmz5wkqXRWd1CqqndD+j70Mak8aWXw7j29SurJP8DWVmnZAVyCkLcRiV2yPN0Y7Yvdc6mLEPYyd'
           'uZUGyDz6woeAsQ8cxhedM9KebfNvmzCG2tECAwEAAaOCAbUwggGxMB0GA1UdDgQWBBRPg7w9QmaP'
           'GlTmMC4geCN0UQSt0zAfBgNVHSMEGDAWgBSx8pNiLx7Jn6dkXuoKCvUCA9oXNDARBglghkgBhvhC'
           'AQEEBAMCBkAwEwYDVR0lBAwwCgYIKwYBBQUHAwEwDgYDVR0PAQH/BAQDAgWgMIHmBgNVHR8Egd4w'
           'gdswgZ6ggZuggZiGgZVsZGFwOi8vbGRhcHIucHJlcHJvZC5vcmcvQ049R3JvdXAlMjBTZXJ2ZXIl'
           'MjBDQSUyMFBSRVBST0QsT1U9Q1JMRFAsT1U9UEtJLE89RGVjYXRobG9uP2NlcnRpZmljYXRlUmV2'
           'b2NhdGlvbkxpc3Q/YmFzZT9vYmplY3RjbGFzcz1jUkxEaXN0cmlidXRpb25Qb2ludDA4oDagNIYy'
           'aHR0cDovL2NybC5wcmVwcm9kLm9yZy9Hcm91cF9TZXJ2ZXJfQ0FfUFJFUFJPRC5jcmwwTgYIKwYB'
           'BQUHAQEEQjBAMD4GCCsGAQUFBzAChjJodHRwOi8vYWlhLnByZXByb2Qub3JnL0dyb3VwX1NlcnZl'
           'cl9DQV9QUkVQUk9ELmNydDANBgkqhkiG9w0BAQUFAAOCAQEAr9iq8p0TVyrnjplbmZDzNyTYbMDM'
           'rL0OiXsQpicveCdKAPJoEKHdXv0pN/Bset8BpJxLe/b8CHh2k4d4SeJLsPg1a7gc6cuqy6qmzsEC'
           'IVqAPwh6h28sZuElfzykpRG8TP+isvhvuI9K66Fx/P6GJI3V1MjtQ1eUV9bhlwdhWdII4IaJZ3g/'
           'ZnxterQbZiM1vT4sk1gojTisF5NwPRlWeCjg1DnyRpOvppPc8FgKksDUVR0/YzXfIotuTOcRDIje'
           'PQWUVvWHVm31yXmhexpXEeSiKbGEgGx369KYZOPuwX/FOqToRGfN24RxDzbKlJYbICYiaVN5R/9G'
           'csmebnYDKw=='
           '</ds:X509Certificate>'
           '</ds:X509Data>'
           '<ds:KeyValue>'
           '<ds:RSAKeyValue>'
           '<ds:Modulus>'
           'ptuIQdNG/m8vgMD/gcI9LGMIKjNhePjlSyIhNWrPbsvAvizshZsOTqI/5bXhElmz5wkqXRWd1Cqq'
           'ndD+j70Mak8aWXw7j29SurJP8DWVmnZAVyCkLcRiV2yPN0Y7Yvdc6mLEPYyduZUGyDz6woeAsQ8c'
           'xhedM9KebfNvmzCG2tE='
           '</ds:Modulus>'
           '<ds:Exponent>AQAB</ds:Exponent>'
           '</ds:RSAKeyValue>'
           '</ds:KeyValue>'
           '</ds:KeyInfo>'
           '</ds:Signature>')


# Required Metadata
SP = {'entityID': None,
      'ACS': None,
      'Binding': HTTP_POST_SimpleSign,
     }

IdP = {'entityID': None,
       'SingleSignOnService': None,
       'X509': None,
      }

# cache of response IDs for replay detection
id_cache = {}

class SAML_Error(Exception):
    pass

# Python's zlib doesn't have a deflate method.
# Luckily, it's just a zlib string without the header and checksum
def b64_deflate(string_val):
    cmp_str = zlib.compress(string_val)[2:-4]
    return b64encode(cmp_str)

def expire_cache(max_age):
    expired = time.time() + max_age
    for k, v in id_cache.items():
        if v < expired:
            del(id_cache[k])

def cache_id(id_str):
    expire_cache(replay_cache_lifetime)
    id_cache[id_str] = time.time()

def gen_id():
    id = uuid.uuid1()
    return str(id)

def timestamp():
    dt = datetime.utcnow()
    dt_str = dt.strftime('%Y-%m-%dT%H:%M:%S.000')[:22] #cut down to millis
    return (dt_str + 'Z')

def parse_simplesign(response, sig, sigalg, relaystate=None):
    cert = M2Crypto.X509.load_cert_string(IdP['X509'])
    logger.debug('Loaded X509 with fingerprint: ' + cert.get_fingerprint())
    pk = cert.get_pubkey()
    pk.reset_context(md='sha1')
    pk.verify_init()
    if relaystate:
        sign_string = 'SAMLResponse=%s&RelayState=%s&SigAlg=%s' % (response, relaystate, sigalg)
    else:
        sign_string = 'SAMLResponse=%s&SigAlg=%s' % (response, sigalg)

    pk.verify_update(sign_string)

    if pk.verify_final(b64decode(sig)) == 0:
        raise SAML_Error('Invalid SAML signature')
    logger.debug('Verified Response signature')

    response_xml = ElementTree.fromstring(response)
    if response_xml.get('ID') in id_cache:
        raise SAML_Error('Replay detected')
    logger.debug('No replay detected within %d seconds' % replay_cache_lifetime)

    cache_id(response_xml.get('ID'))

    issue_inst = dt_parser.parse(response_xml.get('IssueInstant'))
    now = datetime.now(tz=tzutc())
    delta = now - issue_inst
    logger.debug('IssueInstant = %s; CurrentTime = %s' % (issue_inst.ctime(), now.ctime()))
    if delta.seconds > response_window:
        raise SAML_Error('Time delta too great. IssueInstant off by %d seconds'
                         % delta.seconds)

    return response_xml
    

def request(relay_state=None):
    """
    Generate a SAML2 AuthnRequest URL for HTTP-Redirect 
    """
    md = {}
    md.update(SP)
    request_id = gen_id()
    md['SingleSignOnService'] = IdP['SingleSignOnService']
    md['RequestID'] = request_id
    md['IssueInstant'] = timestamp()
    md['Signature'] = sigtmpl % request_id
    req = format_string(md, authnRequest)
    SAMLRequest = urllib.quote(b64_deflate(req))
    
    logger.debug('Generating AuthnRequest')
    logger.debug('SingleSignOnService: ' + md['SingleSignOnService'])
    logger.debug('RequestID: ' + md['RequestID'])
    logger.debug('IssueInstant: ' + md['IssueInstant'])
    logger.debug('AuthnRequest: ' + req)

    location = IdP['SingleSignOnService'] + '?SAMLRequest=' + SAMLRequest
    if relay_state:
        logger.debug('RelayState = ' + relay_state)
        location = location + '&RelayState=' + urllib.quote(relay_state)
    
    return location


def login(form):
    """
    Process the HTTP-POST-SimpleSign form data.
    """
    attrs = {}
    response = b64decode(form.get('SAMLResponse', ''))
    sig = form.get('Signature', '')
    sigalg = form.get('SigAlg', '')
    relaystate = form.get('RelayState', '')

    logger.info('Processing SAML Response')
    logger.info('SAMLResponse: ' + response)
    logger.info('Signature: ' + sig)
    logger.info('SigAlg: ' + sigalg)
    logger.info('relayState: ' + relaystate)

    try:
        response_xml = parse_simplesign(response, sig, sigalg, relaystate)
    except SAML_Error, e:
        logger.error('Authentication Error: ' + str(e))
        logger.debug('Returning no attributes')
        return {}
    xp_subject_nameid = format_string(ns, xp_subject_nameid)
    name_id = response_xml.find(xp_subject_nameid)
    if name_id != None:
        attrs['NameID'] = name_id.text
    xp_attributestatement = format_string(ns, xp_attributestatement)
    for el in response_xml.find(xp_attributestatement):
        name = el.get('FriendlyName') or el.get('Name') or el.tag
        attrs[name] = []
        for av in el.findall(format_string(ns, '{saml2}AttributeValue')):
            if av.text:
                attrs[name].append(av.text)
            else:
                logger.debug(('Parsing XML AttributeValues for %s. '
                          'Some information may not be returned') % name)
                attrs[name] = [child.text for child in av]
   
    return attrs

#Method for compatibility with Python 2.4
def format_string(dict, string):
    logger.debug('Formatting String (Python: 2.4')
    for key in dict:
        string = string.replace('{'+key+'}', dict[key]) 
    logger.debug('Formatted String: ' + str(string))
    return string
