from django.utils import simplejson as json
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.csrf import csrf_exempt
from webui.puppetclasses.utils import update_classes
from webui.acls_manager.utils import update_acls
import sys
import logging

logger = logging.getLogger(__name__)

def save_upload( uploaded, filename, raw_data ):
    ''' raw_data: if True, upfile is a HttpRequest object with raw post data
          as the file, rather than a Django UploadedFile from request.FILES '''
    try:
        from io import FileIO, BufferedWriter
        with BufferedWriter( FileIO( filename, "wb" ) ) as dest:
            # if the "advanced" upload, read directly from the HTTP request 
            # with the Django 1.3 functionality
            if raw_data:
                foo = uploaded.read( 1024 )
                while foo:
                    dest.write( foo )
                    foo = uploaded.read( 1024 ) 
            else:
                for c in uploaded.chunks( ):
                    dest.write( c )
    except IOError:
        return False

@csrf_exempt
def upload(request):
    success = ""
    if request.method == "POST":    
        if request.is_ajax( ):
            upload = request
            try:
                filename = request.GET[ 'qqfile' ]
                funcToCall = request.GET['funcToCall']
            except KeyError: 
                return HttpResponseBadRequest( "AJAX request not valid" )
            file_content = upload.read()
            rsp_message = execute_operation(funcToCall, file_content)
            success = "true"
        else:
            #Actually ignored this part.
            is_raw = False
            if len( request.FILES ) == 1:
                upload = request.FILES.values( )[ 0 ]
            else:
                raise Http404( "Bad Upload" )
            filename = upload.name
         
        
    ret_json = { 'success': success, 'message':rsp_message}
    return HttpResponse( json.dumps( ret_json ) )

def execute_operation(operation, file_content):
    if operation == 'importPuppetClass':
        try:
            json_classes = json.loads(file_content)
        except:
            logger.error("Error parsing JSON file %s" % sys.exc_info()[2])
        update_classes(json_classes)
        return "PuppetClasses Updated"
    elif operation == 'importAcls':
        try:
            json_acls = json.loads(file_content)
        except:
            logger.error("Error parsing JSON file %s" % sys.exc_info()[2])
        update_acls(json_acls)
        return "ACLs Permissions Updated"
        

@csrf_exempt
def get_upload_form(request, funcToCall):
    return render_to_response('upload/form.html', {'funcToCall':funcToCall}, RequestContext(request))