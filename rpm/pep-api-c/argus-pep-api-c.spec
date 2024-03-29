%global base_version 2.3.1
%global base_release 1

%if %{?build_number:1}%{!?build_number:0}
%define release_version 0.build.%{build_number}
%else
%define release_version %{base_release}
%endif

Name: argus-pep-api-c

Version: %{base_version}
Release: %{release_version}%{?dist}
Summary: Argus PEP client library

License: ASL 2.0
Group: System Environment/Libraries
URL: https://twiki.cern.ch/twiki/bin/view/EGEE/AuthorizationFramework

Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libcurl-devel

%description
The Argus PEP client API for C is a multi-thread friendly client library used
to communicate with the Argus PEP Server. It authorizes request and receives
authorization response back from Argus.

%package devel
Group: Development/Libraries
Summary: Argus PEP client development libraries
# SL5 doesn't correctly find the pkgconfig(libcurl) dependency
%if 0%{?rhel} == 5
Requires: %{name} = %{version}-%{release}, curl-devel
%else
Requires: %{name} = %{version}-%{release}
%endif


%description devel
The Argus PEP client API for C is a multi-thread friendly client library used
to communicate with the Argus PEP Server. It authorizes request and receives
authorization response back from Argus.

This package contains the development libraries.

%prep
echo "XXX:macros: dist=%{?dist} el5=%{?el5} rhel=%{?rhel}"
%setup -q
./autotools.sh

%build
%configure

# The following two lines were suggested by
# https://fedoraproject.org/wiki/Packaging/Guidelines to prevent any
# RPATHs creeping in.
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
strip -s -v %{buildroot}%{_libdir}/*.so

# clean up installed documentation, will be done using doc macro
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libargus-pep.so.2.1.0
%{_libdir}/libargus-pep.so.2

%doc AUTHORS COPYING LICENSE README ChangeLog

%files devel
%defattr(-,root,root,-)
%{_libdir}/libargus-pep.so
%{_libdir}/pkgconfig/libargus-pep.pc
%dir %{_includedir}/argus
%{_includedir}/argus/error.h
%{_includedir}/argus/xacml.h
%{_includedir}/argus/pep.h
%{_includedir}/argus/pip.h
%{_includedir}/argus/oh.h
%{_includedir}/argus/profiles.h

%doc src/example

%changelog
* Mon Feb 3 2020 Enrico Vianello <enrico.vianello@cnaf.infn.it> 2.3.1-1
- Moved to 2.3.1-1

* Fri Jan 24 2020 Enrico Vianello <enrico.vianello@cnaf.infn.it> 2.3.1-0
- Prepare for 2.3.1 release

* Mon Feb 8 2016 Andrea Ceccanti <andrea.ceccanti@cnaf.infn.it> 2.3.0-2
- Repackaged against new packaging tools

* Mon Apr 28 2014 Valery Tschopp <valery.tschopp@switch.ch> 2.3.0-1
- Package for upstream version 2.3.0

* Fri Jul 12 2013 Valery Tschopp <valery.tschopp@switch.ch> 2.2.0-2 
- Source in spec file corrected.

* Thu Nov 8 2012 Valery Tschopp <valery.tschopp@switch.ch> 2.2.0-1 
- Package for upstream version 2.2.0
- Corrects rpmlint errors and warnings.

* Fri Aug 3 2012 Valery Tschopp <valery.tschopp@switch.ch> 2.1.1-1
- Self managed packaging with spec file.

* Tue Dec 6 2011 Valery Tschopp <valery.tschopp@switch.ch> 2.1.0-1
- New package for version 2.1.0

* Tue Oct 4 2011 Mischa Salle <msalle@nikhef.nl> 2.0.3-2
- Initial build.


