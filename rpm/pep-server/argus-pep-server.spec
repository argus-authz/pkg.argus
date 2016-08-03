# Turn off the brp-java-repack-jars script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-java-repack-jars[[:space:]].*$!!g')

%global base_version 1.7.2
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

Name: argus-pep-server

Version: %{base_version}
Release: %{release_version}%{?dist}
Summary: Argus PEP Server

Group: System Environment/Daemons
License: ASL 2.0
URL: https://twiki.cern.ch/twiki/bin/view/EGEE/AuthorizationFramework

Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires: java-%{jdk_version}-openjdk-devel
BuildRequires: %{maven}
BuildRequires: jpackage-utils

Requires: java-%{jdk_version}-openjdk
Requires: jpackage-utils
Requires: redhat-lsb
Requires: argus-pep-common >= 2.3
Requires: argus-pdp-pep-common >= 1.5
Requires: voms-api-java

%description
Argus PEP (Policy Enforcement Point) Server.
The Argus Authorization Service renders consistent authorization
decisions for distributed services (e.g., user interfaces,
portals, computing elements, storage elements). The service is
based on the XACML standard, and uses authorization policies to
determine if a user is allowed or denied to perform a certain
action on a particular service.
.
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
%setup -q

%build
make package

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT


%pre
# on install (1): nothing
# on upgrade (2): stop the service, and clean up the lib directory
if [ $1 -eq 2 ] ; then
    /sbin/service argus-pepd stop > /dev/null 2>&1 || :
    # delete old jar
    find /var/lib/argus/pepd/lib -name "*.jar" -exec rm {} \;
fi


%post
# on install (1): register the service in init.d
# on upgrade (2): nothing
if [ $1 -eq 1 ] && [ -z `pidof systemd` ] ; then
    /sbin/chkconfig --add argus-pepd
fi
# correct files/dirs permission
chmod -f 640 %{_sysconfdir}/argus/pepd/pepd.ini
chmod -f 750 %{_datadir}/argus/pepd/sbin/pepdctl
chmod -f 750 %{_localstatedir}/log/argus/pepd
if [ `pidof systemd` ]; then
	/usr/bin/systemctl daemon-reload
fi



%preun
# on uninstall (0): stop and deregister the service
# on upgrade (1): nothing
if [ $1 -eq 0 ] ; then
    /sbin/service argus-pepd stop > /dev/null 2>&1 || :
	if [ ! `pidof systemd` ]; then
    	/sbin/chkconfig --del argus-pepd
	fi
fi

%postun
# on uninstall (0): nothing
# on upgrade (1): restart the service
if [ $1 -eq 1 ] ; then
    /sbin/service argus-pepd start
fi


%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/argus/pepd
%config(noreplace) %{_sysconfdir}/argus/pepd/logging.xml
%config(noreplace) %{_sysconfdir}/argus/pepd/pepd.ini
%config(noreplace) %{_sysconfdir}/sysconfig/argus-pepd
%{_sbindir}/pepdctl
%dir %{_datadir}/argus/pepd
%dir %{_datadir}/argus/pepd/sbin
%{_datadir}/argus/pepd/logs
%{_datadir}/argus/pepd/conf
%{_datadir}/argus/pepd/doc
%{_datadir}/argus/pepd/lib
%{_datadir}/argus/pepd/sbin/pepdctl
%{_sysconfdir}/grid-security/certificates/policy-aspen-birch-cedar.info
%{_sysconfdir}/grid-security/certificates/policy-aspen-birch-cedar-dogwood.info
%dir %{_defaultdocdir}/argus/pepd
%{_defaultdocdir}/argus/pepd/COPYRIGHT
%{_defaultdocdir}/argus/pepd/LICENSE
%{_defaultdocdir}/argus/pepd/RELEASE-NOTES
%dir %{_localstatedir}/lib/argus/pepd/lib
%{_localstatedir}/lib/argus/pepd/lib/argus-pepd-%{version}.jar
%{_localstatedir}/lib/argus/pepd/lib/commons-codec-*.jar
%{_localstatedir}/lib/argus/pepd/lib/commons-collections-*.jar
%{_localstatedir}/lib/argus/pepd/lib/commons-httpclient-*.jar
%{_localstatedir}/lib/argus/pepd/lib/commons-io-*.jar
%{_localstatedir}/lib/argus/pepd/lib/commons-lang-*.jar
%{_localstatedir}/lib/argus/pepd/lib/ehcache-*.jar
%{_localstatedir}/lib/argus/pepd/lib/esapi-*.jar
%{_localstatedir}/lib/argus/pepd/lib/ini4j-*.jar
%{_localstatedir}/lib/argus/pepd/lib/jcl-over-slf4j-*.jar
%{_localstatedir}/lib/argus/pepd/lib/jetty-*.jar
%{_localstatedir}/lib/argus/pepd/lib/javax.*.jar
%{_localstatedir}/lib/argus/pepd/lib/jna-*.jar
%{_localstatedir}/lib/argus/pepd/lib/joda-time-*.jar
%{_localstatedir}/lib/argus/pepd/lib/jul-to-slf4j-*.jar
%{_localstatedir}/lib/argus/pepd/lib/log4j-over-slf4j-*.jar
%{_localstatedir}/lib/argus/pepd/lib/logback-classic-*.jar
%{_localstatedir}/lib/argus/pepd/lib/logback-core-*.jar
%{_localstatedir}/lib/argus/pepd/lib/not-yet-commons-ssl-*.jar
%{_localstatedir}/lib/argus/pepd/lib/opensaml-*.jar
%{_localstatedir}/lib/argus/pepd/lib/openws-*.jar
%{_localstatedir}/lib/argus/pepd/lib/slf4j-api-*.jar
%{_localstatedir}/lib/argus/pepd/lib/velocity-*.jar
%{_localstatedir}/lib/argus/pepd/lib/xmlsec-*.jar
%{_localstatedir}/lib/argus/pepd/lib/xmltooling-*.jar
%dir %{_localstatedir}/lib/argus/pepd/lib/endorsed
%{_localstatedir}/lib/argus/pepd/lib/endorsed/serializer-*.jar
%{_localstatedir}/lib/argus/pepd/lib/endorsed/xalan-*.jar
%{_localstatedir}/lib/argus/pepd/lib/endorsed/xercesImpl-*.jar
%{_localstatedir}/lib/argus/pepd/lib/endorsed/xml-apis-*.jar
%{_localstatedir}/lib/argus/pepd/lib/endorsed/xml-resolver-*.jar
%dir %{_localstatedir}/lib/argus/pepd/lib/provided
%{_localstatedir}/lib/argus/pepd/lib/provided/bcpkix-*.jar
%{_localstatedir}/lib/argus/pepd/lib/provided/bcprov-*.jar
%{_localstatedir}/lib/argus/pepd/lib/provided/canl-*.jar
%{_localstatedir}/lib/argus/pepd/lib/provided/voms-api-java-*.jar
%dir %{_localstatedir}/log/argus/pepd

%if 0%{?rhel} >= 7 || 0%{?fedora} >= 21
%exclude %{_sysconfdir}/init.d/argus-pepd
/lib/systemd/system/argus-pepd.service
%else
%exclude /lib/systemd/system/argus-pepd.service
%{_sysconfdir}/init.d/argus-pepd
%endif

%changelog
* Wed Aug  3 2016 Mischa Salle <msalle@nikhef.nl> 1.7.2-1
- Add two Argus-specific policy info files.

* Thu May 5 2016 Andrea Ceccanti <andrea.ceccanti@cnaf.infn.it> 1.7.2-0
- Pre-release packaging for 1.7.2

* Mon Apr 11 2016 Marco Caberletti <marco.caberletti@cnaf.infn.it> 1.7.0-2
- Exclude sysV init script for EL7.

* Tue Nov 17 2015 Marco Caberletti <marco.caberletti@cnaf.infn.it> 1.7.0-1
- Add systemd unit file.

* Tue Sep 8 2015 Andrea Ceccanti <andrea.ceccanti@cnaf.infn.it> 1.7.0-0
- Pre-release packaging for 1.7.0

* Thu Oct  2 2014 Mischa Salle <msalle@nikhef.nl> 1.6.2-1
- Replace exact versions, except argus-pepd, in filelist with wildcard.
- Upstream version 1.6.2 for EMI-3.

* Thu Feb 20 2014 Valery Tschopp <valery.tschopp@switch.ch> 1.6.2-0
- Version 1.6.2 (RC1) for EMI-3 update.

* Fri Apr 5 2013 Valery Tschopp <valery.tschopp@switch.ch> 1.6.1-1
- Upstream version 1.6.1 for EMI-3 update.

* Wed Jan 30 2013 Valery Tschopp <valery.tschopp@switch.ch> 1.6.0-3
- Upstream version 1.6.0 for EMI-3 release.

* Tue Jan 29 2013 Valery Tschopp <valery.tschopp@switch.ch> 1.6.0-2
- Upstream version 1.6.0 for EMI-3 (RC2).

* Sun Nov 18 2012 Valery Tschopp <valery.tschopp@switch.ch> 1.6.0-1
- Upstream version 1.6.0 for EMI-3 (RC1).

* Mon Jul 30 2012 Valery Tschopp <valery.tschopp@switch.ch> 1.5.2-1
- Self managed packaging with spec file.

* Tue Apr 3 2012 Valery Tschopp <valery.tschopp@switch.ch> 1.5.1-1
- Initial Argus PDP for EMI 2.

