'''
Created on Nov 13, 2012

@author: mmornati
'''
import logging
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from guardian.decorators import permission_required
from webui.messages.models import Message, IgnoredMessage
from django.utils import simplejson as json

logger = logging.getLogger(__name__)

@login_required()
@permission_required('messages.modify_messages', return_403=True)
def delete_message(request, message_id):
    logger.debug("Delete message with id %s" % message_id)
    try:
        m = Message.objects.get(id=message_id)
        m.delete()
    except Exception, e:
        return HttpResponse(json.dumps({"result":"ERROR", "message":str(e)}), mimetype="application/json")
    return HttpResponse(json.dumps({"result":"OK"}), mimetype="application/json")
    
@login_required()
@permission_required('messages.modify_messages', return_403=True)
def ignore_message(request, message_id):
    logger.debug("Ignore message with id %s" % message_id)
    try:
        m = Message.objects.get(id=message_id)
        IgnoredMessage.objects.create(server=m.server, message=m.message)
        m.delete()
    except Exception, e:
        return HttpResponse(json.dumps({"result":"ERROR", "message":str(e)}), mimetype="application/json")
    return HttpResponse(json.dumps({"result":"OK"}), mimetype="application/json")