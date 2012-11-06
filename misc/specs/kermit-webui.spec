Summary: KermIT WebUI Framework
Name: kermit-webui
Version: 1.3
Release: 1%{dist}
License: GPLv3
Group: Applications/System
URL: https://github.com/kermitfr/kermit-webui
Source: %{name}-%{version}.tar.gz

%description
%{summary}.

%package main
Summary: KermIT WebUI Main Package
Requires: httpd, Django >= 1.4, django-grappelli = 2.4.2, django-guardian = 1.0.4, django-celery, django-kombu, uuid, redis, django-picklefield
Requires: policycoreutils-python
%if "%dist" == ".el5"
Requires: python(abi) = 2.6, python26-mod_wsgi, python26-httplib2, ordereddict, python26-redis, python26-docutils, selinux-policy-devel 
BuildRequires: ordereddict 
%else
Requires: python(abi) >= 2.6, mod_wsgi, python-httplib2, python-redis, python-ordereddict, python-docutils, selinux-policy
%endif
%if "%dist" == ".el6"
Requires: python-dateutil15
%endif 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
#BuildRequires: Django >= 1.4
#BuildRequires: django-picklefield
#BuildRequires: django-grappelli = 2.4.2
#BuildRequires: django-guardian = 1.0.4
#BuildRequires: django-celery
#BuildRequires: django-kombu

%description main
%{summary}.

#SubPackages Definition
%package platform-bar
Summary: BatchARchive KermIT Platform
Group: Applications/System
Requires: kermit-webui-main = %{version}

%description platform-bar
%{summary}.

%package platform-jboss
Summary: JBoss KermIT Platform
Group: Applications/System
Requires: kermit-webui-main = %{version}

%description platform-jboss
%{summary}.

%package platform-oc4j
Summary: OC4J KermIT Platform
Group: Applications/System
Requires: kermit-webui-main = %{version}

%description platform-oc4j
%{summary}.

%package platform-oracledb
Summary: Oracle Database KermIT Platform
Group: Applications/System
Requires: kermit-webui-main = %{version}

%description platform-oracledb
%{summary}.

%package platform-postgresql
Summary: PostgreSQL KermIT Platform
Group: Applications/System
Requires: kermit-webui-main = %{version}

%description platform-postgresql
%{summary}.

%package platform-virtualization
Summary: Virtualization KermIT Platform
Group: Applications/System
Requires: kermit-webui-main = %{version}

%description platform-virtualization
%{summary}.

%package platform-weblogic
Summary: JBoss KermIT Platform
Group: Applications/System
Requires: kermit-webui-main = %{version}

%description platform-weblogic
%{summary}.


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
%{__mkdir} -p $RPM_BUILD_ROOT/var/lib/kermit/webui/db

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
%{__cp} ./misc/selinux/kermitweb.te $RPM_BUILD_ROOT/usr/share/%{name}/selinux/kermitweb.te
%{__cp} ./misc/selinux/applyse.sh $RPM_BUILD_ROOT/usr/share/%{name}/selinux/applyse.sh
%{__cp} ./setup.sh $RPM_BUILD_ROOT/usr/share/%{name}/setup.sh
%if "%dist" == ".el5"
%{__cp} ./misc/fixes/manage.py $RPM_BUILD_ROOT/usr/share/%{name}/webui/manage.py
%{__cp} ./misc/httpd.conf/kermit-webui.conf.el5 $RPM_BUILD_ROOT/etc/httpd/conf.d/kermit-webui.conf
%{__cp} ./misc/scripts/django.wsgi.el5 $RPM_BUILD_ROOT/etc/kermit/webui/scripts/django.wsgi
%endif
#create version file
echo %{version} > $RPM_BUILD_ROOT/etc/kermit/webui/version.txt


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files main
%defattr(-,root,root,-) 
/*/*

#Exclude all platforms sources
%exclude /usr/share/%{name}/webui/platforms/bar
%exclude /usr/share/%{name}/webui/platforms/jboss
%exclude /usr/share/%{name}/webui/platforms/oc4j
%exclude /usr/share/%{name}/webui/platforms/oracledb
%exclude /usr/share/%{name}/webui/platforms/postgresql
%exclude /usr/share/%{name}/webui/platforms/virtualization
%exclude /usr/share/%{name}/webui/platforms/weblogic
#Exclude all platforms templates
%exclude /usr/share/%{name}/templates/platforms/bar
%exclude /usr/share/%{name}/templates/platforms/jboss
%exclude /usr/share/%{name}/templates/platforms/oc4j
%exclude /usr/share/%{name}/templates/platforms/oracledb
%exclude /usr/share/%{name}/templates/platforms/postgresql
%exclude /usr/share/%{name}/templates/platforms/virtualization
%exclude /usr/share/%{name}/templates/platforms/weblogic

#Exclude Custom Stuffs
%exclude /usr/share/%{name}/webui/chain
%exclude /usr/share/%{name}/templates/chain

%doc /usr/share/doc/*

%config /etc/httpd/conf.d/*
%config(noreplace) %attr(0644,apache,apache) /etc/kermit/kermit-webui.cfg
%attr(0777,apache,apache) %dir /var/lib/kermit/webui/db
%attr(0750,apache,apache) %dir /var/www/%{name}/uploads
%attr(0755,apache,apache) %dir /var/log/kermit
%attr(0755,apache,apache) %dir /var/log/celery
%attr(0755,apache,apache) %dir /var/run/celery
%attr(0755,apache,apache) /usr/share/kermit-webui/webui/manage.py
%attr(0755,apache,apache) /etc/httpd/conf.d/kermit-webui.conf
%attr(0755,root,root) /usr/share/kermit-webui/selinux/applyse.sh
%attr(0755,root,root) /usr/share/kermit-webui/setup.sh
%attr(0755,root,root) /etc/rc.d/init.d/celeryd
%attr(0755,root,root) /etc/rc.d/init.d/celeryev
%attr(0755,root,root) /etc/rc.d/init.d/celerybeat

%files platform-bar
%defattr(-,root,root)
/usr/share/%{name}/webui/platforms/bar
/usr/share/%{name}/templates/platforms/bar

%files platform-jboss
%defattr(-,root,root)
/usr/share/%{name}/webui/platforms/jboss
/usr/share/%{name}/templates/platforms/jboss

%files platform-oc4j
%defattr(-,root,root)
/usr/share/%{name}/webui/platforms/oc4j
/usr/share/%{name}/templates/platforms/oc4j

%files platform-oracledb
%defattr(-,root,root)
/usr/share/%{name}/webui/platforms/oracledb
/usr/share/%{name}/templates/platforms/oracledb

%files platform-postgresql
%defattr(-,root,root)
/usr/share/%{name}/webui/platforms/postgresql
/usr/share/%{name}/templates/platforms/postgresql

%files platform-virtualization
%defattr(-,root,root)
/usr/share/%{name}/webui/platforms/virtualization
/usr/share/%{name}/templates/platforms/virtualization

%files platform-weblogic
%defattr(-,root,root)
/usr/share/%{name}/webui/platforms/weblogic
/usr/share/%{name}/templates/platforms/weblogic

%pre

%post

%preun

%postun

%changelog
