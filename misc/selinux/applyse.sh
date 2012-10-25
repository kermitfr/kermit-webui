/usr/sbin/setsebool -P httpd_tmp_exec on
/usr/sbin/setsebool -P httpd_can_network_connect on
/usr/sbin/setsebool -P httpd_can_network_connect_db on

cp /etc/kermit/webui/selinux/kermitweb.te /tmp
cd /tmp
make -f /usr/share/selinux/devel/Makefile
semodule -i kermitweb.pp
rm -f /tmp/kermitweb.*

/usr/sbin/semanage fcontext -a -t httpd_sys_content_t /usr/share/kermit-webui
/usr/sbin/semanage fcontext -a -t httpd_sys_content_t "/var/lib/kermit/webui/db(/.*)?"

/sbin/restorecon -R /usr/share/kermit-webui
/sbin/restorecon -R /var/lib/kermit
/sbin/restorecon -R /etc/kermit
