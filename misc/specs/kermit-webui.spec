Summary: Mcollective WebUI
Name: kermit-webui
Version: 1.0.2
Release: 1%{dist}
License: GPL
Group: Applications/System
URL: https://github.com/thinkfr/kermit-webui
Source: %{name}-%{version}.tar.gz
Requires: httpd, Django, django-grappelli, django-guardian, django-celery, django-kombu, uuid, redis, django-picklefield
%if "%dist" == ".el5"
Requires: python(abi) = 2.6, python26-mod_wsgi, python26-httplib2, ordereddict, python26-redis, python26-docutils 
%else
Requires: python(abi) >= 2.6, mod_wsgi, python-httplib2, python-redis, python-ordereddict, python-docutils
%endif

%if "%dist" == ".el6"
Requires: python-dateutil15
%endif 

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
BuildRequires: django-grappelli
BuildRequires: django-guardian
BuildRequires: django-celery
BuildRequires: django-kombu

%description
Mcollective WebUI
Quick start :
cd /usr/share/kermit-webui
python webui/manage.py syncdb --noinput
/etc/init.d/httpd restart

%prep
%setup -n %{name}

%build
%if "%dist" == ".el5"
	python26 ./src/webui/manage.py syncdb --noinput
%else
	python ./src/webui/manage.py syncdb --noinput
%endif

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT/etc/httpd/conf.d
%{__mkdir} -p $RPM_BUILD_ROOT/etc/kermit/webui
%{__mkdir} -p $RPM_BUILD_ROOT/etc/sysconfig
%{__mkdir} -p $RPM_BUILD_ROOT/etc/rc.d/init.d
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/%{name}
%{__mkdir} -p $RPM_BUILD_ROOT/var/lib/kermit/webui/db
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}
%{__mkdir} -p $RPM_BUILD_ROOT/var/www/%{name}
%{__mkdir} -p $RPM_BUILD_ROOT/var/www/%{name}/uploads
%{__mkdir} -p $RPM_BUILD_ROOT/var/log/kermit
%{__mkdir} -p $RPM_BUILD_ROOT/var/log/celery
%{__mkdir} -p $RPM_BUILD_ROOT/var/run/celery

%{__cp} -R ./src/* $RPM_BUILD_ROOT/usr/share/%{name}
%{__cp} -R /tmp/sqlite.db $RPM_BUILD_ROOT/var/lib/kermit/webui/db
%{__cp} -R ./misc/config/kermit-webui.cfg.prod $RPM_BUILD_ROOT/etc/kermit/kermit-webui.cfg
#%{__rm} -Rf $RPM_BUILD_ROOT/var/lib/kermit/webui/db/sqlite.db
%{__rm} -Rf $RPM_BUILD_ROOT/usr/share/%{name}/webui/kermit-webui.cfg

%{__cp} -R ./misc/saml2/* $RPM_BUILD_ROOT/etc/kermit/webui
%{__cp} -R ./templates $RPM_BUILD_ROOT/usr/share/%{name}
%{__cp} -R ./static $RPM_BUILD_ROOT/var/www/%{name}
%{__cp} -R ./fixtures $RPM_BUILD_ROOT/etc/kermit/webui
%{__cp} -R ./misc/scripts $RPM_BUILD_ROOT/etc/kermit/webui
%{__cp} -R ./README $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}
%{__cp} ./misc/httpd.conf/kermit-webui.conf $RPM_BUILD_ROOT/etc/httpd/conf.d
%{__cp} -R README $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}
#%{__cp} -R ./misc/sql $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}
#%{__ln_s} -f ../../usr/share/%{name}/settings.py $RPM_BUILD_ROOT/etc/%{name}/
install -m 755 ./misc/init/init.d/celeryd $RPM_BUILD_ROOT/etc/rc.d/init.d/celeryd
install -m 755 ./misc/init/init.d/celeryev $RPM_BUILD_ROOT/etc/rc.d/init.d/celeryev
install -m 755 ./misc/init/init.d/celerybeat $RPM_BUILD_ROOT/etc/rc.d/init.d/celerybeat
%{__cp} ./misc/init/sysconfig/celeryd $RPM_BUILD_ROOT/etc/sysconfig/celeryd
%{__cp} ./misc/init/sysconfig/celeryev $RPM_BUILD_ROOT/etc/sysconfig/celeryev
%{__cp} ./misc/init/sysconfig/celerybeat $RPM_BUILD_ROOT/etc/sysconfig/celerybeat
%if "%dist" == ".el5"
%{__cp} ./misc/fixes/manage.py $RPM_BUILD_ROOT/usr/share/%{name}/webui/manage.py
%{__cp} ./misc/httpd.conf/kermit-webui.conf.el5 $RPM_BUILD_ROOT/etc/httpd/conf.d/kermit-webui.conf
%{__cp} ./misc/scripts/django.wsgi.el5 $RPM_BUILD_ROOT/etc/kermit/webui/scripts/django.wsgi
%endif
#create version file
echo %{version} > $RPM_BUILD_ROOT/etc/kermit/webui/version.txt


%clean
%{__rm} -rf $RPM_BUILD_ROOT
%{__rm} -rf /tmp/sqlite.db

%files
%defattr(-,root,root,-) 
/*/*

%doc /usr/share/doc/*

%config /etc/httpd/conf.d/*
#%config /usr/share/%{name}/settings.py
%config /var/lib/kermit/webui/db/sqlite.db
%config /etc/kermit/kermit-webui.cfg
%attr(0777,apache,apache) %dir /var/lib/kermit/webui/db
%attr(0777,apache,apache) %dir /var/lib/kermit/webui/db/sqlite.db
%attr(0750,apache,apache) %dir /var/www/%{name}/uploads
%attr(0755,apache,apache) %dir /var/log/kermit
%attr(0755,apache,apache) %dir /var/log/celery
%attr(0755,apache,apache) %dir /var/run/celery
%attr(0644,apache,apache) %dir /etc/kermit/kermit-webui.cfg
%attr(0755,apache,apache) /usr/share/kermit-webui/webui/manage.py
%attr(0755, root, root) /etc/rc.d/init.d/celeryd
%attr(0755, root, root) /etc/rc.d/init.d/celeryev
%attr(0755, root, root) /etc/rc.d/init.d/celerybeat
%pre

%post
#if [ "$1" -le "1" ] ; then # First install
#selinux_mode=`/usr/sbin/getenforce`
#if [ "$selinux_mode" == "Enforcing" ]; then
#/usr/sbin/semanage fcontext -a -t httpd_sys_content_t /usr/share/%{name}
#/usr/sbin/semanage fcontext -a -t httpd_sys_content_t "/usr/share/%{name}/db(/.*)?"
#/sbin/restorecon -R /usr/share/%{name}
#fi
#/sbin/service httpd restart > /dev/null 2>&1
#fi

%preun

%postun

%changelog
