#!/bin/bash
PY=python
test -f /usr/bin/python26 && PY=python26

echo "* Executing script using $PY"
echo "* Creating database with configuration found in kermit.cfg"
$PY src/webui/manage.py syncdb --noinput
echo "* Importing base data"
rpm -q Django | grep -q 1.4
if [ $? -eq 0 ]; then
    $PY src/webui/manage.py loaddata basedata-django1.4.1
else
    $PY src/webui/manage.py loaddata basedata
fi
echo "* Importing base Widgets configuration"
$PY src/webui/manage.py loaddata widget
echo "* Change admin password"
$PY src/webui/manage.py changepassword admin
echo ""
