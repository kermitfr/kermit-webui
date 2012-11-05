#!/bin/bash
PY=python
test -f /usr/bin/python26 && PY=python26

MANAGE_FILE=/usr/share/kermit-webui/webui/manage.py

echo "* Executing script using $PY"
echo "* Creating database with configuration found in kermit-webui.cfg"
$PY $MANAGE_FILE syncdb --noinput
if [ $? -ne 0 ]; then
	exit 1;
fi
echo "* Importing base data"
rpm -q Django | grep -q 1.4
if [ $? -eq 0 ]; then
    $PY $MANAGE_FILE loaddata basedata-django14
else
    $PY $MANAGE_FILE loaddata basedata
fi
if [ $? -ne 0 ]; then
	exit 1;
fi
echo "* Importing base Widgets configuration"
$PY $MANAGE_FILE loaddata widget
if [ $? -ne 0 ]; then
	exit 1;
fi
dbname=$(sed -n -e '/\[webui-database\]/,/\[/p' /etc/kermit/kermit-webui.cfg | sed -n -e 's/^name=\(.*\)$/\1/gp')
if [ -f $dbname ]; then
	echo "* Changing database file rights"
	chown apache:apache $dbname
fi
logfile=$(sed -n -e '/\[webui_logs\]/,/\[/p' /etc/kermit/kermit-webui.cfg | sed -n -e 's/^main\.file=\(.*\)$/\1/gp')
if [ -f $logfile ]; then
	echo "* Changing kermit log file rights"
	chown apache:apache $logfile 
fi
mcologfile=$(sed -n -e '/\[webui_logs\]/,/\[/p' /etc/kermit/kermit-webui.cfg | sed -n -e 's/^calls\.file=\(.*\)$/\1/gp')
if [ -f $mcologfile ]; then
	echo "* Changing kermit mco log file rights"
	chown apache:apache $mcologfile 
fi
echo "* Change admin password"
$PY $MANAGE_FILE changepassword admin
echo ""
