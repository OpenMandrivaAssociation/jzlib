Name:		jzlib
Version:	1.1.5
Release:	1
Summary:	Re-implementation of zlib in pure Java
Group:		Development/Java
License:	BSD-3-Clause
URL:		https://github.com/jruby/jzlib
# Tag jzlib-1.1.5 of the JRuby fork. JRuby 9.4.14 compiles against
# org.jruby:jzlib. The classes stay in com.jcraft.jzlib. The module
# name stays com.jcraft.jzlib so the previous jmod provide still
# matches. Cooker 1.1.3 was the ymnk archive and provided only
# com.jcraft:jzlib. This build keeps that coordinate as an alias.
# Upstream Maven asks for source 7 and optimize, which the current
# JDK rejects, so the sources are compiled with javac.
Source0:	jzlib-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	java-current-devel
BuildRequires:	sysjar
BuildRequires:	javapackages-filesystem

Obsoletes:	%{name}-javadoc < %{version}-%{release}
Obsoletes:	%{name}-demo < %{version}-%{release}

%description
JZlib is a pure Java reimplementation of zlib, including gzip
streams. This package is the JRuby 1.1.5 fork. ZStream deflates and
inflates a byte buffer. The Java module is com.jcraft.jzlib.

%prep
%autosetup -n jzlib-jzlib-%{version} -p1
find . -type f \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -print > binaries.list
find . -type d -name '*.jar' -print >> binaries.list
if [ -s binaries.list ]; then
	cat binaries.list
	exit 1
fi
find src/main/java -name '*.java' | sort > sources.list
test "$(wc -l < sources.list)" -eq 23

%build
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-openjdk
export PATH="$JAVA_HOME/bin:$PATH"
mkdir -p classes modsrc
javac --release 8 -Xlint:-options -encoding UTF-8 -d classes @sources.list
test "$(find classes -name '*.class' | wc -l)" -eq 26
javap -v -classpath classes com.jcraft.jzlib.ZStream | grep -F -q 'major version: 52'
cat > modsrc/module-info.java << 'EOF'
module com.jcraft.jzlib {
    exports com.jcraft.jzlib;
}
EOF
javac --release 9 \
	--patch-module com.jcraft.jzlib=classes \
	-d classes \
	modsrc/module-info.java
test -s classes/module-info.class
test "$(find classes -name '*.class' | wc -l)" -eq 27
printf '%s\n' 'Manifest-Version: 1.0' > manifest.mf
jar cfm jzlib.jar manifest.mf -C classes .
jar i jzlib.jar
if jar tf jzlib.jar | grep -q '\.java$'; then
	exit 1
fi
jar tf jzlib.jar | grep -F -q 'com/jcraft/jzlib/ZStream.class'
jar tf jzlib.jar | grep -F -q 'module-info.class'
desc=$(jar --describe-module --file jzlib.jar)
printf '%s\n' "$desc"
if printf '%s\n' "$desc" | grep -F -q 'Unable'; then
	exit 1
fi
printf '%s\n' "$desc" | grep -F -q 'com.jcraft.jzlib'

cat > jzlib.pom << 'END'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.jruby</groupId>
  <artifactId>jzlib</artifactId>
  <version>1.1.5</version>
  <name>JZlib</name>
  <description>JZlib is a re-implementation of zlib in pure Java.</description>
  <url>https://github.com/jruby/jzlib</url>
  <licenses>
    <license>
      <name>BSD-3-Clause</name>
      <url>https://opensource.org/licenses/BSD-3-Clause</url>
    </license>
  </licenses>
</project>
END

%install
set -eo pipefail
sysjar install --buildroot %{buildroot} \
	--artifact jzlib.pom:jzlib.jar \
	--file-name jzlib \
	--alias com.jcraft:jzlib \
	--filelist .mfiles
idx="%{buildroot}/usr/share/sysjar/index/org.jruby/jzlib.sysjar"
test -s "$idx"
grep -F -q '"version": "1.1.5"' "$idx"
grep -F -q '"groupId": "org.jruby"' "$idx"
grep -F -q '"groupId": "com.jcraft"' "$idx"
grep -F -q '"artifactId": "jzlib"' "$idx"
test -s %{buildroot}%{_javadir}/jzlib.jar

%check
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-openjdk
export PATH="$JAVA_HOME/bin:$PATH"
JAR=%{buildroot}%{_javadir}/jzlib.jar
test -s "$JAR"
mkdir -p check
cat > check/Smoke.java << 'EOF'
import com.jcraft.jzlib.JZlib;
import com.jcraft.jzlib.ZStream;
import java.nio.charset.StandardCharsets;

public class Smoke {
    public static void main(String[] args) {
        byte[] plain = "jzlib_ok".getBytes(StandardCharsets.UTF_8);
        ZStream def = new ZStream();
        int rc = def.deflateInit(JZlib.Z_BEST_COMPRESSION);
        if (rc != JZlib.Z_OK) {
            throw new AssertionError("deflateInit " + rc);
        }
        def.next_in = plain;
        def.next_in_index = 0;
        def.avail_in = plain.length;
        byte[] comp = new byte[128];
        def.next_out = comp;
        def.next_out_index = 0;
        def.avail_out = comp.length;
        rc = def.deflate(JZlib.Z_FINISH);
        if (rc != JZlib.Z_STREAM_END) {
            throw new AssertionError("deflate " + rc);
        }
        int compLen = def.next_out_index;
        rc = def.deflateEnd();
        if (rc != JZlib.Z_OK) {
            throw new AssertionError("deflateEnd " + rc);
        }
        byte[] produced = new byte[compLen];
        System.arraycopy(comp, 0, produced, 0, compLen);
        ZStream inf = new ZStream();
        rc = inf.inflateInit();
        if (rc != JZlib.Z_OK) {
            throw new AssertionError("inflateInit " + rc);
        }
        inf.next_in = produced;
        inf.next_in_index = 0;
        inf.avail_in = produced.length;
        byte[] out = new byte[128];
        inf.next_out = out;
        inf.next_out_index = 0;
        inf.avail_out = out.length;
        rc = inf.inflate(JZlib.Z_FINISH);
        if (rc != JZlib.Z_STREAM_END) {
            throw new AssertionError("inflate " + rc);
        }
        int outLen = inf.next_out_index;
        String text = new String(out, 0, outLen, StandardCharsets.UTF_8);
        if (!"jzlib_ok".equals(text)) {
            throw new AssertionError(text);
        }
        System.out.println("jzlib_ok " + outLen);
    }
}
EOF
javac --release 8 -Xlint:-options -cp "$JAR" -d check check/Smoke.java
"$JAVA_HOME/bin/java" -cp "check:$JAR" Smoke > check/out.txt
cat check/out.txt
grep -F -qx 'jzlib_ok 8' check/out.txt

%files -f .mfiles
%doc README ChangeLog example
%license LICENSE.txt
