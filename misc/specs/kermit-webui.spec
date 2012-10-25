Summary: Mcollective WebUI
Name: kermit-webui
Version: 1.1
Release: 3%{dist}
License: GPL
Group: Applications/System
URL: https://github.com/thinkfr/kermit-webui
Source: %{name}-%{version}.tar.gz

Requires: httpd, Django, django-grappelli, django-guardian, django-celery, django-kombu, uuid, redis, django-picklefield

%if "%dist" == ".el5"
Requires: python(abi) = 2.6, python26-mod_wsgi, python26-httplib2, ordereddict, python26-redis, python26-docutils 
BuildRequires: ordereddict 
%else
Requires: python(abi) >= 2.6, mod_wsgi, python-httplib2, python-redis, python-ordereddict, python-docutils
#BuildRequires: python-ordereddict 
%endif

%if "%dist" == ".el6"
Requires: python-dateutil15
%endif 

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
BuildRequires: django-picklefield
BuildRequires: django-grappelli
BuildRequires: django-guardian
BuildRequires: django-celery
BuildRequires: django-kombu

%description
Mcollective WebUI

%prep
%setup -n %{name}

%build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT/etc/httpd/conf.d
%{__mkdir} -p $RPM_BUILD_ROOT/etc/kermit/webui
%{__mkdir} -p $RPM_BUILD_ROOT/etc/sysconfig
%{__mkdir} -p $RPM_BUILD_ROOT/etc/rc.d/init.d
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/%{name}
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/%{name}/selinux
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}
%{__mkdir} -p $RPM_BUILD_ROOT/var/www/%{name}
%{__mkdir} -p $RPM_BUILD_ROOT/var/www/%{name}/uploads
%{__mkdir} -p $RPM_BUILD_ROOT/var/log/kermit
%{__mkdir} -p $RPM_BUILD_ROOT/var/log/celery
%{__mkdir} -p $RPM_BUILD_ROOT/var/run/celery

%{__cp} -R ./src/* $RPM_BUILD_ROOT/usr/share/%{name}
%{__cp} -R ./misc/config/kermit-webui.cfg.prod $RPM_BUILD_ROOT/etc/kermit/kermit-webui.cfg
%{__rm} -Rf $RPM_BUILD_ROOT/usr/share/%{name}/webui/kermit-webui.cfg

%{__cp} -R ./misc/saml2/* $RPM_BUILD_ROOT/etc/kermit/webui
%{__cp} -R ./templates $RPM_BUILD_ROOT/usr/share/%{name}
%{__cp} -R ./static $RPM_BUILD_ROOT/var/www/%{name}
%{__cp} -R ./fixtures $RPM_BUILD_ROOT/etc/kermit/webui
%{__cp} -R ./misc/scripts $RPM_BUILD_ROOT/etc/kermit/webui
%{__cp} -R ./README $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}
%{__cp} ./misc/httpd.conf/kermit-webui.conf $RPM_BUILD_ROOT/etc/httpd/conf.d
%{__cp} -R README $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}
install -m 755 ./misc/init/init.d/celeryd $RPM_BUILD_ROOT/etc/rc.d/init.d/celeryd
install -m 755 ./misc/init/init.d/celeryev $RPM_BUILD_ROOT/etc/rc.d/init.d/celeryev
install -m 755 ./misc/init/init.d/celerybeat $RPM_BUILD_ROOT/etc/rc.d/init.d/celerybeat
%{__cp} ./misc/init/sysconfig/celeryd $RPM_BUILD_ROOT/etc/sysconfig/celeryd
%{__cp} ./misc/init/sysconfig/celeryev $RPM_BUILD_ROOT/etc/sysconfig/celeryev
%{__cp} ./misc/init/sysconfig/celerybeat $RPM_BUILD_ROOT/etc/sysconfig/celerybeat
%{__cp} ./misc/selinux/kermitweb.te %$RPM_BUILD_ROOT/usr/share/%{name}/selinux/kermitweb.te
%{__cp} ./misc/selinux/applyse.sh %$RPM_BUILD_ROOT/usr/share/%{name}/selinux/applyse.sh
%if "%dist" == ".el5"
%{__cp} ./misc/fixes/manage.py $RPM_BUILD_ROOT/usr/share/%{name}/webui/manage.py
%{__cp} ./misc/httpd.conf/kermit-webui.conf.el5 $RPM_BUILD_ROOT/etc/httpd/conf.d/kermit-webui.conf
%{__cp} ./misc/scripts/django.wsgi.el5 $RPM_BUILD_ROOT/etc/kermit/webui/scripts/django.wsgi
%endif
#create version file
echo %{version} > $RPM_BUILD_ROOT/etc/kermit/webui/version.txt


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-) 
/*/*

%doc /usr/share/doc/*

%config /etc/httpd/conf.d/*
%config(noreplace) %attr(0644,apache,apache) /etc/kermit/kermit-webui.cfg
%attr(0750,apache,apache) %dir /var/www/%{name}/uploads
%attr(0755,apache,apache) %dir /var/log/kermit
%attr(0755,apache,apache) %dir /var/log/celery
%attr(0755,apache,apache) %dir /var/run/celery
%attr(0755,apache,apache) /usr/share/kermit-webui/webui/manage.py
%attr(0755,root,root) /usr/share/kermit-webui/selinux/applyse.sh
%attr(0755, root, root) /etc/rc.d/init.d/celeryd
%attr(0755, root, root) /etc/rc.d/init.d/celeryev
%attr(0755, root, root) /etc/rc.d/init.d/celerybeat
%pre

%post

%preun

%postun

%changelog
