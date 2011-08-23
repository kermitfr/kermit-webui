import os
import sys
path = '/usr/share/kermit-webui/'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'webui.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()