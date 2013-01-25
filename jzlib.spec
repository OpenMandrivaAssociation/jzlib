Name:           jzlib
Version:        1.1.1
Release:        1
Epoch:          0
Summary:        JZlib re-implementation of zlib in pure Java

Group:          Development/Java
License:        BSD-style
URL:            http://www.jcraft.com/jzlib/
Source0:        http://www.jcraft.com/jzlib/jzlib-%{version}.zip

BuildArch:      noarch
BuildRequires:	java-1.6.0-openjdk-devel
BuildRequires:  java-rpmbuild >= 0:1.5.31, ant >= 0:1.5.4

%track
prog %name = {
	url = http://www.jcraft.com/jzlib/
	version = %version
	regex = jzlib-(__VER__)\.zip
}

%description
The zlib is designed to be a free, general-purpose, legally unencumbered 
-- that is, not covered by any patents -- lossless data-compression 
library for use on virtually any computer hardware and operating system. 
The zlib was written by Jean-loup Gailly (compression) and Mark Adler 
(decompression). 

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
%{summary}.

%package        demo
Summary:        Examples for %{name}
Group:          Development/Java

%description    demo
%{summary}.


%prep
%setup -q -n %{name}-%{version}
mkdir -p dist/lib javadoc

%build
export JAVA_HOME=%_prefix/lib/jvm/java-1.6.0
cd src/main
find . -name "*.java" |xargs $JAVA_HOME/bin/javac
jar cf ../../dist/lib/%name.jar `find . -name "*.class"`
$JAVA_HOME/bin/javadoc -d ../../javadoc java.com.jcraft.jzlib java/com/jcraft/jzlib/*.java

%install
# jars
rm -rf $RPM_BUILD_ROOT
install -Dpm 644 dist/lib/%{name}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# examples
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
cp -pr example/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_datadir}/%{name} # ghost symlink

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%post demo
rm -f %{_datadir}/%{name}
ln -s %{name}-%{version} %{_datadir}/%{name}


%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt
%{_javadir}/*.jar

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%doc %{_datadir}/%{name}-%{version}
%ghost %doc %{_datadir}/%{name}

%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0:1.0.7-12mdv2011.0
+ Revision: 665842
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.0.7-11mdv2011.0
+ Revision: 606120
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.0.7-10mdv2010.1
+ Revision: 523153
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.0.7-9mdv2010.0
+ Revision: 425478
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:1.0.7-8mdv2009.1
+ Revision: 351330
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0:1.0.7-7mdv2009.0
+ Revision: 221763
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.0.7-6mdv2008.1
+ Revision: 120959
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.0.7-5mdv2008.0
+ Revision: 87189
- rebuild to filter out autorequires on GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sat Sep 08 2007 Pascal Terjan <pterjan@mandriva.org> 0:1.0.7-4mdv2008.0
+ Revision: 82637
- update to new version


* Wed Mar 14 2007 Christiaan Welvaart <spturtle@mandriva.org> 1.0.7-3mdv2007.1
+ Revision: 143750
- rebuild for 2007.1
- Import jzlib

* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 0:1.0.7-2mdv2007.0
- rebuild for libgcj.so.7
- aot-compile

* Sat Jan 14 2006 David Walluck <walluck@mandriva.org> 0:1.0.7-1mdk
- 1.0.7

* Sun May 08 2005 David Walluck <walluck@mandriva.org> 0:1.0.5-2.1mdk
- release

* Wed Oct 20 2004 David Walluck <david@jpackage.org> 0:1.0.5-2jpp
- rebuild with jdk 1.4.2

* Wed Oct 20 2004 David Walluck <david@jpackage.org> 0:1.0.5-1jpp
- 0.1.5

* Tue Aug 24 2004 Randy Watler <rwatler at finali.com> - 0:1.0.3-2jpp
- Rebuild with ant-1.6.2

