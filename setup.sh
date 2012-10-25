#!/bin/bash
PY=python
test -f /usr/bin/python26 && PY=python26


$PY src/webui/manage.py loaddata basedata
$PY src/webui/manage.py loaddata widget

