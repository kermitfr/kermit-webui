Summary: Mcollective WebUI
Name: kermit-webui
Version: 0.4.1
Release: 1
License: GPL
Group: Applications/System
URL: https://github.com/thinkfr/kermit-webui
Source: %{name}-%{version}.tar.gz
Requires: httpd, Django, django-grappelli, django-guardian, django-celery, django-kombu, uuid, redis
%if 0%{?fedora}
Requires: python(abi) >= 2.6, mod_wsgi, python-httplib2, python-redis >= 2.4.10
%else
Requires: python(abi) = 2.6, python26-mod_wsgi, python26-httplib2, ordereddict, python26-redis >= 2.4.10 
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
%if 0%{?fedora}
	python ./src/webui/manage.py syncdb --noinput
%else
	python26 ./src/webui/manage.py syncdb --noinput
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
%if 0%{?fedora}
#do nothing
echo "Fedora: Do nothing..."
%else
%{__cp} ./misc/fixes/manage.py $RPM_BUILD_ROOT/usr/share/%{name}/webui/manage.py
%endif


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
%attr(0755, root, root) /etc/rc.d/init.d/celeryd
%attr(0755, root, root) /etc/rc.d/init.d/celeryev
%attr(0755, root, root) /etc/rc.d/init.d/celerybeat
%pre

%post
if [ "$1" -le "1" ] ; then # First install
selinux_mode=`/usr/sbin/getenforce`
if [ "$selinux_mode" == "Enforcing" ]; then
/usr/sbin/semanage fcontext -a -t httpd_sys_content_t /usr/share/%{name}
/usr/sbin/semanage fcontext -a -t httpd_sys_content_t "/usr/share/%{name}/db(/.*)?"
/sbin/restorecon -R /usr/share/%{name}
fi
/sbin/service httpd restart > /dev/null 2>&1
fi

%preun

%postun

%changelog
* Tue Oct 25 2011 Marco Mornati <ilmorna@gmail.com> - 0.0.3-8 
	Fixed problem on redirect url after login
  	Changed widget default position and name
  	Autoexpanded Tree on Server details
	Renamed Admin Link
	Rename Search field for System Status Widget
  	Fixed problem with content menu position when widget is at the bottom of the page
  	Added Widget with appli information
  	Created settings for saml2 in prod settings file (need to create properties in py file)
  	Added Widget ServerStatus With Classes Information
	Renamed ServerStatus to SystemStatus (Classes and files)
* Thu Sep 20 2011 Marco Mornati <ilmorna@gmail.com> - 0.0.3-4
	Added server export CSV
	Added Authentication Module
	Refactored tables with Jquery Datatable
	
* Thu Sep 19 2011 Marco Mornati <ilmorna@gmail.com> - 0.0.3-3
	Fixed poblems deploying application on different path
	Added external properties file
	
* Thu Sep 1 2011 Marco Mornati <ilmorna@gmail.com> - 0.0.2-2
	Fixed problem on OC4J with apps without poollist
	Changed id for server: from hostname to fqdn

* Thu Sep 1 2011 Marco Mornati <ilmorna@gmail.com> - 0.0.2-1
	Fixed problems with Weblogic platform
	Fixed wrong HTML char
	Fixed wrong tree name for webloginc platform
	Added basic security     Created login/logout pages
	Version updated
	Fixed build problem changing version

* Thu Aug 18 2011 Marco Mornati <ilmorna@gmail.com>
    Added Server Details page

* Wed Aug 17 2011 Marco Mornati <ilmorna@gmail.com>
    Added Admin Operations
    Imported some django admin templates to extends
    Completed view part of PuppetClasses Widget
    Completed Widgets on Database
    Added missing admin area

* Wed Aug 17 2011 Marco Mornati <ilmorna@gmail.com>
    Added Cron App used to schedule tasks from others installed apps
    Completed Server Status apps and models
    Autoretrieved information from mcollective about server status, agents and puppet classes
    Added tree view to navigate puppet classes
    Added some necessary plugin to jquery

* Tue Aug 16 2011 Marco Mornati <ilmorna@gmail.com>
    Added python-simplejson dependency in spec file
    Added Dynamic Paths in Settings.py file

* Mon Aug 15 2011 Louis Coilliot <louis.coilliot@gmail.com>
    kermit.conf to kermit-webui.conf
    Refs to 'automatix' and 'kermit' changed to 'webui'

* Sun Aug 14 2011 Louis Coilliot <louis.coilliot@gmail.com>
    Minor changes

* Sun Aug 14 2011 Marco Mornati <ilmorna@gmail.com>
    Renamed project and project stuffs using OpenSource name and not the Customer Custom (automatix -> kermit)
    Added firt version of spec file to rpm generation
    Added Apache configuration

* Sat Aug 13 2011 Marco Mornati <ilmorna@gmail.com>
    Updated README file

* Fri Aug 12 2011 Marco Mornati <ilmorna@gmail.com>
    Added Django Widget Project (modified to get it working)
    Added initial_data to initialize database
    Created a first widget example (to complete fixing some problems)
    Updated README file
    Created puppetclass django app
    Fixed problem within Dynamic Widgets
    Removed unused files
    Added Server Status Apps
    Added Logging Stuffs to new classes (to be refactored all view classes)
    Renamed Django_Widgets to Widgets
    Creted Models for ServerClasses

* Thu Aug 11 2011 Marco Mornati <ilmorna@gmail.com> - 0.0.1-1
	Added Default Operation to database
	Enabled admin area
	Show default operations dynamically retrieving information from database
