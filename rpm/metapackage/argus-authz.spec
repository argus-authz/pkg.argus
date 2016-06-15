%global base_version 1.7.0
%global base_release 1

%if %{?build_number:1}%{!?build_number:0}
%define release_version 0.build.%{build_number}
%else
%define release_version %{base_release}
%endif

Name: argus-authz

Version: %{base_version}
Release: %{release_version}%{?dist}
Summary: Argus Authorization Service meta-package (PAP, PDP and PEP Server)

Group: System Environment/Daemons
License: ASL 2.0
URL: http://argus-authz.github.io/

BuildArch: noarch

Requires: argus-pap
Requires: argus-pdp
Requires: argus-pep-server
Requires: argus-pepcli
Requires: bdii
Requires: lcg-expiregridmapdir
Requires: fetch-crl

%description
Argus meta-package (PAP, PDP and PEP Server).
The Argus Authorization Service is composed of three main
components:
- The Policy Administration Point (PAP) provides the tools to
author authorization policies, organize them in the local
repository and configure policy distribution among remote PAPs.
- The Policy Decision Point (PDP) implements the authorization
engine, and is responsible for the evaluation of the authorization
requests against the XACML policies retrieved from the PAP.
- The Policy Enforcement Point Server (PEP Server) ensures the
integrity and consistency of the authorization requests received
from the PEP clients. Lightweight PEP client libraries are also
provided to ease the integration and interoperability with other
EMI services or components.

%prep

%build

%install

%clean

%files

%changelog
* Fri Apr 15 2016 Marco Caberletti <marco.caberletti@cnaf.infn.it> 1.7.0
- Argus metapackage for EL7.

* Wed Nov 14 2012 Valery Tschopp <valery.tschopp@switch.ch> 1.6.0-1
- Argus metapackage for EMI-3.

