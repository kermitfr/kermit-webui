'''
Created on Sep 19, 2011

@author: mmornati
'''
import saml2
from os import path
import ConfigParser
from webui.utils import CONF

BASE_URL=CONF.get('webui', 'base_url')

LOGIN_URL=BASE_URL+"/auth/saml2/login/"
LOGIN_REDIRECT_URL = BASE_URL
LOGOUT_LINK = ""
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

BASEDIR = path.dirname(path.abspath(__file__))
SAML_CONFIG = {
    # full path to the xmlsec1 binary programm
    'xmlsec_binary': '/usr/bin/xmlsec1',

    # your entity id, usually your subdomain plus the url to the metadata view
    'entityid': 'KermitIDP',
    
    #Added to prevent time not synchro between webui-server and IDP server
    'timeslack': '5000' ,

    # directory with attribute mapping
    'attribute_map_dir': path.join(BASEDIR, 'attribute-maps'),

    # this block states what services we provide
    'service': {
        # we are just a lonely SP
        'sp' : {
            'name': 'Example Service Provider',
            'endpoints': {
                # url and binding to the assetion consumer service view
                # do not change the binding or service name
                'assertion_consumer_service': [
                    ('http://saml.kermit.fr/saml2/login/',
                     saml2.BINDING_HTTP_POST),
                    ],
                # url and binding to the single logout service view
                # do not change the binding or service name
                'single_logout_service': [
                    ('http://saml.kermit.fr/auth/saml2/logout/',
                     saml2.BINDING_HTTP_REDIRECT),
                    ],
                },

             # attributes that this project need to identify a user
            'required_attributes': ['uid'],

             # attributes that may be useful to have but not required
            'optional_attributes': ['eduPersonAffiliation'],

            # in this section the list of IdPs we talk to are defined
            'idp': {
                # we do not need a WAYF service since there is
                # only an IdP defined here. This IdP should be
                # present in our metadata

                # the keys of this dictionary are entity ids
                #'https://localhost/simplesaml/saml2/idp/metadata.php': {
                'identity.kermit.fr': {
                    'single_sign_on_service': {
                        saml2.BINDING_HTTP_REDIRECT: 'https://saml.kremit.fr/login/',
                        },
                    'single_logout_service': {
                        saml2.BINDING_HTTP_REDIRECT: 'https://saml.kermit.fr/logout/',
                        },
                    },
                },
            },
        },

    # where the remote metadata is stored
    'metadata': {
        'local': ['/etc/kermit/webui/metadata_example.xml'],
        },

    # set to 1 to output debugging information
    'debug': 1,

    # certificate
    'key_file': '/etc/kermit/webui/mykey.pem',  # private part
    'cert_file': '/etc/kermit/webui/mycert.pem',  # public part

    # own metadata settings
    'contact_person': [
        {'given_name': 'Test',
         'sur_name': 'Test',
         'company': 'Think',
         'email_address': 'test@kermit.fr',
         'contact_type': 'technical'},
        {'given_name': 'Test2',
         'sur_name': 'Test2',
         'company': 'Think',
         'email_address': 'test2@kermit.fr',
         'contact_type': 'administrative'},
        ],
    # you can set multilanguage information here
    'organization': {
        'name': [('Kermit', 'fr'), ('Kermit', 'en')],
        'display_name': [('Kermit', 'fr'), ('Kermit', 'en')],
        'url': [('http://www.kermit.fr', 'fr'), ('http://www.kermit.fr', 'en')],
        },
    'valid_for': 1,  # how long is our metadata valid
    }
