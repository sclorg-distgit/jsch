%{?scl:%scl_package jsch}
%{!?scl:%global pkg_name %{name}}

Name:           %{?scl_prefix}jsch
Version:        0.1.54
Release:        4.2%{?dist}
Summary:        Pure Java implementation of SSH2
Group:          Development/Libraries
License:        BSD
URL:            http://www.jcraft.com/jsch/
BuildArch:      noarch

Source0:        http://download.sourceforge.net/sourceforge/jsch/jsch-%{version}.zip
# wget \
# http://download.eclipse.org/tools/orbit/downloads/drops/R20090825191606/bundles/com.jcraft.jsch_0.1.41.v200903070017.jar
# unzip com.jcraft.jsch_*.jar META-INF/MANIFEST.MF
# mv META-INF/MANIFEST.MF .
# sed -i "/^Name/d" MANIFEST.MF
# sed -i "/^SHA1/d" MANIFEST.MF
# dos2unix MANIFEST.MF
# sed -i "/^$/d" MANIFEST.MF
# unix2dos MANIFEST.MF
Source1:        MANIFEST.MF
Source2:        plugin.properties

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}mvn(com.jcraft:jzlib)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.sonatype.oss:oss-parent:pom:)
BuildRequires:  zip

Requires:       %{?scl_prefix}jzlib >= 0:1.0.5

%description
JSch allows you to connect to an sshd server and use port forwarding, 
X11 forwarding, file transfer, etc., and you can integrate its 
functionality into your own Java programs.

%package        javadoc
Summary:        Javadoc for %{pkg_name}

%description    javadoc
%{summary}.

%prep
%setup -n %{pkg_name}-%{version} -q
%mvn_file : jsch

%pom_remove_plugin :maven-javadoc-plugin

%pom_xpath_remove pom:project/pom:build/pom:extensions
%pom_xpath_set pom:project/pom:version %{version}

%build
%mvn_build

# inject the OSGi Manifest
mkdir META-INF
cp %{SOURCE1} META-INF
cp %{SOURCE2} plugin.properties
touch META-INF/MANIFEST.MF
touch plugin.properties
zip target/%{pkg_name}-%{version}.jar META-INF/MANIFEST.MF
zip target/%{pkg_name}-%{version}.jar plugin.properties

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Thu Jun 22 2017 Michael Simacek <msimacek@redhat.com> - 0.1.54-4.2
- Mass rebuild 2017-06-22

* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 0.1.54-4.1
- Automated package import and SCL-ization

* Thu Feb 23 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.1.54-4
- Remove unneeded maven-javadoc-plugin invocation

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.54-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 31 2016 Alexander Kurtakov <akurtako@redhat.com> 0.1.54-2
- Fix version in pom.xml.

* Wed Aug 31 2016 Alexander Kurtakov <akurtako@redhat.com> - 0.1.54-1
- New upstream release 0.1.54

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.1.53-5
- Add missing build-requires

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.53-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.53-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 5 2015 Alexander Kurtakov <akurtako@redhat.com> 0.1.53-2
- Revert jsch.jar to not be in javadir subdir.

* Fri Jun 5 2015 Alexander Kurtakov <akurtako@redhat.com> 0.1.53-1
- Update to 0.1.53
- Build with xmvn.
