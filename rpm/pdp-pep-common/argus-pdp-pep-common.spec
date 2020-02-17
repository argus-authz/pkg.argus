## Turn off meaningless jar repackaging on SL6
%define __jar_repack 0

%global jar_version 1.5.2
%global base_version 1.5.2
%global base_release 1

%define jdk_version 1.8.0

%if 0%{?rhel} >= 7 || 0%{?fedora} >= 21
%define maven maven
%else
%define maven apache-maven
%endif

%if %{?build_number:1}%{!?build_number:0}
%define release_version 0.build.%{build_number}
%else
%define release_version %{base_release}
%endif

Name: argus-pdp-pep-common

Version: %{base_version}
Release: %{release_version}%{?dist}
Summary: Argus PDP and PEP Server shared library

Group: System Environment/Libraries
License: ASL 2.0
URL: https://twiki.cern.ch/twiki/bin/view/EGEE/AuthorizationFramework

Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires: java-%{jdk_version}-openjdk-devel
BuildRequires: %{maven}

Requires: java-%{jdk_version}-openjdk
Requires: canl-java

%description 
Argus PDP and PEP Server shared library.
The Argus Authorization Service renders consistent authorization 
decisions for distributed services (e.g., user interfaces, 
portals, computing elements, storage elements). The service is 
based on the XACML standard, and uses authorization policies to 
determine if a user is allowed or denied to perform a certain 
action on a particular service.

%prep
%setup -q

%build
make package

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{_datadir}/java
%{_datadir}/java/%{name}.jar
%{_datadir}/java/%{name}-%{jar_version}.jar
%{_datadir}/doc/%{name}-%{jar_version}/RELEASE-NOTES
%{_datadir}/doc/%{name}-%{jar_version}/COPYRIGHT
%{_datadir}/doc/%{name}-%{jar_version}/LICENSE


%changelog
* Mon Feb 3 2020 Enrico Vianello <enrico.vianello@cnaf.infn.it> 1.5.2-1
- Moved to 1.5.2-1

* Tue Sep 10 2019 Enrico Vianello <enrico.vianello@cnaf.infn.it> 1.5.2-0
- Packaging for 1.5.2-0

* Mon Sep 7 2015 Andrea Ceccanti <andrea.ceccanti@cnaf.infn.it> 1.5.1-1
- Packaging for 1.5.1-1

* Mon Sep 7 2015 Andrea Ceccanti <andrea.ceccanti@cnaf.infn.it> 1.5.0-0
- Pre-release packaging for 1.5.0-0

* Mon Mar 16 2015 Andrea Ceccanti <andrea.ceccanti@cnaf.infn.it> 1.4.1-1
- Official packaging for upstream 1.4.1 release

* Wed May 28 2014 Valery Tschopp <valery.tschopp@switch.ch> 1.4.1-0
- Upstream version 1.4.1 for EMI-3 (RC1)

* Tue Jan 29 2013 Valery Tschopp <valery.tschopp@switch.ch> 1.4.0-2 
- Upstream version 1.4.0 for EMI-3 (RC2)

* Sun Nov 18 2012 Valery Tschopp <valery.tschopp@switch.ch> 1.4.0-1 
- Upstream version 1.4.0 for EMI-3 (RC1).

* Tue Jul 31 2012 Valery Tschopp <valery.tschopp@switch.ch> 1.3.2-1
- Self managed packaging with spec file.

* Tue Apr 3 2012 Valery Tschopp <valery.tschopp@switch.ch> 1.3.1-1
- Initial PDP and PEP Server common library for EMI 2.
