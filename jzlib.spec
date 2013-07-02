Summary:        Re-implementation of zlib in pure Java
Name:           jzlib
Version:        1.1.1
Release:        2
Group:          Development/Java
License:        BSD-style
Url:            http://www.jcraft.com/jzlib/
Source0:        http://www.jcraft.com/jzlib/jzlib-%{version}.zip
BuildArch:      noarch

BuildRequires:	ant >= 0:1.5.4
BuildRequires:	java-1.6.0-openjdk-devel
BuildRequires:  java-rpmbuild >= 0:1.5.31

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
%setup -q
mkdir -p dist/lib javadoc

%build
export JAVA_HOME=%{_prefix}/lib/jvm/java-1.6.0
cd src/main
find . -name "*.java" |xargs $JAVA_HOME/bin/javac
jar cf ../../dist/lib/%name.jar `find . -name "*.class"`
$JAVA_HOME/bin/javadoc -d ../../javadoc java.com.jcraft.jzlib java/com/jcraft/jzlib/*.java

%install
# jars
install -Dpm 644 dist/lib/%{name}.jar \
  %{buildroot}%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} # ghost symlink

# examples
install -dm 755 %{buildroot}%{_datadir}/%{name}-%{version}
cp -pr example/* %{buildroot}%{_datadir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_datadir}/%{name} # ghost symlink

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%post demo
rm -f %{_datadir}/%{name}
ln -s %{name}-%{version} %{_datadir}/%{name}

%files
%doc LICENSE.txt
%{_javadir}/*.jar

%files javadoc
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files demo
%doc %{_datadir}/%{name}-%{version}
%ghost %doc %{_datadir}/%{name}

