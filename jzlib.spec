%define section   free
%define gcj_support 1

Name:           jzlib
Version:        1.0.7
Release:        %mkrel 8
Epoch:          0
Summary:        JZlib re-implementation of zlib in pure Java

Group:          Development/Java
License:        BSD-style
URL:            http://www.jcraft.com/jzlib/
Source0:        http://www.jcraft.com/jzlib/jzlib-%{version}.tar.bz2
Source1:        %{name}_build.xml
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
#Distribution:   JPackage
#Vendor:         JPackage Project

%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRequires:  java-rpmbuild >= 0:1.5.31, ant >= 0:1.5.4

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
cp %{SOURCE1} build.xml
mkdir src
mv com src

%build
%ant dist javadoc 

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


%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

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
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%doc %{_datadir}/%{name}-%{version}
%ghost %doc %{_datadir}/%{name}


