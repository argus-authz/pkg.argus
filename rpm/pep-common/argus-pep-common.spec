## Turn off meaningless jar repackaging on SL6
%define __jar_repack 0

%global base_version 2.3.1
%global base_release 1

%if 0%{?rhel} == 5
%define jdk_version 1.7.0
%else
%define jdk_version 1.8.0
%endif

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

Name: argus-pep-common

Version: %{base_version}
Release: %{release_version}%{?dist}
Summary: Argus PEP client and server shared library

Group: System Environment/Libraries
License: ASL 2.0
URL: https://twiki.cern.ch/twiki/bin/view/EGEE/AuthorizationFramework

##Source: https://github.com/downloads/argus-authz/%{name}/%{name}-%{version}.tar.gz
Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires: java-%{jdk_version}-openjdk-devel
BuildRequires: %{maven}

Requires: java-%{jdk_version}-openjdk

%description
Argus PEP client and PEP Server shared library.
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
%{_datadir}/java/%{name}-%{version}.jar
%doc README.md doc/RELEASE-NOTES doc/COPYRIGHT doc/Hessian.LICENSE doc/LICENSE

%changelog
* Sun Feb 7 2016 Andrea Ceccanti <andrea.ceccanti@cnaf.infn.it> 2.3.1-0
- Upstream version 2.3.1

* Wed Nov 14 2012 Valery Tschopp <valery.tschopp@switch.ch> 2.3.0-1
- Upstream version 2.3.0 for EMI-3.

* Tue Jul 31 2012 Valery Tschopp <valery.tschopp@switch.ch> 2.2.1-1
- Self managed packaging with spec file.

* Tue Apr 3 2012 Valery Tschopp <valery.tschopp@switch.ch> 2.2.0-1
- Initial PEP Server and client library for EMI 2.
