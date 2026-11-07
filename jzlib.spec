Name:		jzlib
Version:	1.1.3
Release:	2
Summary:	Re-implementation of zlib in pure Java
Group:		Development/Java
License:	BSD
URL:		https://github.com/ymnk/jzlib
Source0:	https://github.com/ymnk/jzlib/archive/refs/tags/%{version}.tar.gz#/%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name jzlib

Obsoletes:	%{name}-javadoc < %{version}-%{release}
Obsoletes:	%{name}-demo < %{version}-%{release}

%description
JZlib is a pure Java reimplementation of zlib, including gzip
streams. 1.1.3 is the last upstream release. The 0.0 releases were
LGPL. This release is the BSD license. The Java module is
com.jcraft.jzlib. The examples are shipped as documentation and are
not run as tests.

%prep
%autosetup -n jzlib-%{version}
# Compiler plugin 2.0 asks for source and target 1.5 and for optimize.
# The current JDK rejects source 1.5. Compiler plugin 3.x rejects
# optimize. The version stays, so the plugin and this configuration
# are kept and the version is rewritten to the installed plugin.
python - <<'PY'
import xml.etree.ElementTree as ET
from pathlib import Path

ET.register_namespace("", "http://maven.apache.org/POM/4.0.0")
ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")

def local(tag):
    return tag.rsplit("}", 1)[-1]

path = Path("pom.xml")
tree = ET.parse(path)
root = tree.getroot()
compiler = None
for parent in root.iter():
    for child in list(parent):
        if local(child.tag) != "plugin":
            continue
        artifact = ""
        for item in child:
            if local(item.tag) == "artifactId":
                artifact = (item.text or "").strip()
        if artifact == "maven-compiler-plugin":
            compiler = child
if compiler is None:
    raise SystemExit("compiler plugin missing")
plugin_version = ""
for item in compiler:
    if local(item.tag) == "version":
        plugin_version = (item.text or "").strip()
optimize = source = target = None
for item in compiler.iter():
    name = local(item.tag)
    if name == "optimize":
        optimize = item
    elif name == "source":
        source = item
    elif name == "target":
        target = item
    elif name == "release":
        raise SystemExit("compiler release present")
if optimize is None or source is None or target is None:
    raise SystemExit("compiler fields missing")
if plugin_version != "2.0" or (source.text or "").strip() != "1.5":
    raise SystemExit("unexpected compiler pin")
removed = False
for parent in compiler.iter():
    if optimize in list(parent):
        parent.remove(optimize)
        removed = True
        break
if not removed:
    raise SystemExit("optimize parent missing")
source.text = "1.8"
target.text = "1.8"
tree.write(path, encoding="UTF-8", xml_declaration=True)
text = path.read_text(encoding="utf-8")
if "<optimize>" in text or ">1.5<" in text or ">1.8<" not in text:
    raise SystemExit("rewrite failed")
if "<release>" in text:
    raise SystemExit("release was added")
PY

%build -a
cat > target/module-info.java << 'EOF'
module com.jcraft.jzlib {
    exports com.jcraft.jzlib;
}
EOF
javac --release 9 \
	--patch-module com.jcraft.jzlib=target/classes \
	-d target/classes \
	target/module-info.java
test -s target/classes/module-info.class
jar uf target/jzlib-%{version}.jar -C target/classes module-info.class
java --module-path target/jzlib-%{version}.jar --describe-module com.jcraft.jzlib | grep -q '^com.jcraft.jzlib'

%files -f .mfiles
%doc LICENSE.txt README ChangeLog example
