#!/usr/bin/python
import os
import sys
path = os.getcwd()
if path not in sys.path:
        sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'webui.settings'
os.environ["CELERY_LOADER"] = "django"
