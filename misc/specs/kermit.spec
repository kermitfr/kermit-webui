Summary: Mcollective WebUI
Name: kermit
Version: 0.0.1
Release: 1
License: GPL
Group: Applications/System
URL: https://github.com/thinkfr/automatix
Source: %{name}-%{version}.tar.gz
Requires: httpd, Django, python, mod_python, python-httplib2
#, python-json, python-simplejson
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

%description
Mcollective WebUI

%prep
%setup -n %{name}

%build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT/etc/httpd/conf.d
%{__mkdir} -p $RPM_BUILD_ROOT/etc/%{name}
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/%{name}
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}
%{__mkdir} -p $RPM_BUILD_ROOT/var/www/%{name}
%{__mkdir} -p $RPM_BUILD_ROOT/var/www/%{name}/uploads

%{__cp} -R ./src/* $RPM_BUILD_ROOT/usr/share/%{name}
%{__cp} -R ./templates $RPM_BUILD_ROOT/usr/share/%{name}
%{__cp} -R ./static $RPM_BUILD_ROOT/var/www/%{name}
%{__cp} -R ./fixtures $RPM_BUILD_ROOT/etc/%{name}
%{__cp} -R ./README $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}
%{__cp} ./misc/httpd.conf/%{name}.conf $RPM_BUILD_ROOT/etc/httpd/conf.d
#%{__cp} -R ./misc/sql $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}
#%{__cp} -R ./misc/sql/sqlite.dat $RPM_BUILD_ROOT/var/www/%{name}
#%{__ln_s} -f ../../usr/share/%{name}/settings.py $RPM_BUILD_ROOT/etc/%{name}/


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-) 
/*/*

%doc /usr/share/doc/*

%config /etc/httpd/conf.d/*
#%config /usr/share/%{name}/settings.py
%config /var/www/%{name}/sqlite.dat
%attr(0750,apache,apache) %dir /var/www/%{name}/uploads

%pre

%post

%postun

%changelog
* Sun Aug 14 2011 Marco Mornati <ilmorna@gmail.com> - 1.0
- Project startup
