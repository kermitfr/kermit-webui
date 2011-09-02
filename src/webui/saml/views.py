# Create your views here.
from webui.saml import saml
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

def SSO(request):
    print request.POST
    attrs = saml.login(request.POST)
    # attrs is a dict containing simplified SAML attributes.
    # Attribute values are returned in a list, even for single values.
    # attrs['NameID'] is the Subject/NameID.
    # The remaining values are from the AttributeStatement, e.g.
    # if attrs.get('eduPersonPrincipalName')[0] in valid_users:
    #     authenticated = True
    
    # An unsuccessful authentication will log errors and return
    # and empty dict.
        
    final_destination = request.forms.get('RelayState')
    print final_destination
    print attrs
    # continue

def logout(request):
    return ''

def test(request):
    # First, register metadata for both parties
    ## Service Provider metadata
    # entityID registered with the IdP
    saml.SP['entityID'] = 'AutomatixD1'
    # Assertion Consumer Server URL
    saml.SP['ACS'] = 'http://oxitz1atx02.dktetrix.net/saml/SSO'
    
    # Identity Provider metadata
    saml.IdP['entityID'] = 'IDPDecathlon'
    saml.IdP['SingleSignOnService'] = 'https://preprod.idpdecathlon.oxylane.com:9031/idp/SSO.saml2'
    # the X509 certificate must in PEM form, including BEGIN and END lines
    print "Reading pem file"
    pem = open('/tmp/idp.pem')
    saml.IdP['X509'] = pem.read()
    final_destination = 'http://oxitz1atx02.dktetrix.net/saml/SSO'
    return redirect(saml.request(relay_state=final_destination))
