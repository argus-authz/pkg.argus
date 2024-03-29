# Copyright (c) Istituto Nazionale di Fisica Nucleare (INFN). 2006-2010.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global base_version 1.6.1
%global base_release 1

%if %{?build_number:1}%{!?build_number:0}
%define release_version %{base_release}.build.%{build_number}
%else
%define release_version %{base_release}
%endif

%define default_user root
%define default_prefix /opt/glite

Name: yaim-argus_server
Version: %{base_version}
Release: %{release_version}%{?dist}
Summary: Yaim ARGUS_server configuration

License: ASL 2.0
Group: System Environment/Libraries
URL: https://twiki.cern.ch/twiki/bin/view/EGEE/AuthorizationFramework

Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires: glite-yaim-core
Requires: glite-info-provider-service
Requires: glite-yaim-bdii

%description
yaim configuration for the ARGUS_server node-type (EMI)


%prep
%setup -q -n %{name}-%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir /opt/glite/yaim/etc/versions/
/opt/glite/yaim/etc/versions/glite-yaim-argus-server
%dir /opt/glite/yaim/examples/siteinfo/services/
/opt/glite/yaim/examples/siteinfo/services/glite-argus_server
%dir /opt/glite/yaim/node-info.d/
/opt/glite/yaim/node-info.d/glite-argus_server
%dir /opt/glite/yaim/functions/
/opt/glite/yaim/functions/config_info_glue2_service_argus
/opt/glite/yaim/functions/config_pep_service
/opt/glite/yaim/functions/config_pdp_service
/opt/glite/yaim/functions/config_pap_service
%dir /opt/glite/yaim/defaults/
/opt/glite/yaim/defaults/glite-argus_server.post
/opt/glite/yaim/defaults/glite-argus_server.pre
%doc COPYRIGHT LICENSE README.md

%changelog
* Mon Feb 17 2020 Enrico Vianello <enrico.vianello@cnaf.infn.it> 1.6.1-1
- Moved to version 1.6.1-1

* Mon Dec 3 2012 Valery Tschopp <valery.tschopp@switch.ch> 1.6.0-1
- Upstream version 1.6.0 for EMI-3.

* Fri Aug 3 2012 Valery Tschopp <valery.tschopp@switch.ch> 1.5.2-1
- Self managed packaging with spec file.

* Tue Apr 3 2012 Valery Tschopp <valery.tschopp@switch.ch> 1.5.1-1
- Initial yaim ARGUS_server config for EMI 2.
