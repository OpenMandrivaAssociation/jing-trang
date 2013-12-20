%_javapackages_macros
# TODO:
# - Install dtdinst's schemas, XSL etc as non-doc and to system catalogs?
# - Drop isorelax and xerces license texts and references to them because
#   our package does not actually contain them?

%if 0%{?fedora} >= 20 || 0%{?rhel} >= 7
%global headless -headless
%endif

Name:           jing-trang
Version:        20091111
Release:        16.0%{?dist}
Summary:        Schema validation and conversion based on RELAX NG


License:        BSD
URL:            http://code.google.com/p/jing-trang/
# Source0 generated with Source99, upstream does not distribute archives
# containing the complete build system
Source0:        %{name}-%{version}.tar.xz
Source99:       %{name}-prepare-tarball.sh
# Applicable parts submitted upstream:
# http://code.google.com/p/jing-trang/issues/detail?id=129
# http://code.google.com/p/jing-trang/issues/detail?id=130
Patch0:         %{name}-20091111-build.patch
# Saxon "HE" doesn't work for this, no old Saxon available, details in #655601
Patch1:         %{name}-20091111-xalan.patch
Patch2:         %{name}-20091111-datatype-sample.patch
# http://code.google.com/p/jing-trang/source/detail?r=2356, #716177
Patch3:         %{name}-20091111-saxon93-716177.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%if 0%{?rhel} && 0%{?rhel} < 7
BuildRequires:  ant-trax
%else
BuildRequires:  ant >= 1.8.2
%endif
BuildRequires:  bsh
BuildRequires:  isorelax
BuildRequires:  java-devel-openjdk >= 1:1.6.0
BuildRequires:  java-javadoc
BuildRequires:  javacc
BuildRequires:  jpackage-utils
BuildRequires:  qdox
BuildRequires:  relaxngDatatype
BuildRequires:  relaxngDatatype-javadoc
BuildRequires:  saxon >= 9.3
BuildRequires:  testng
BuildRequires:  xalan-j2
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-resolver

%description
%{summary}.

%package     -n jing
Summary:        RELAX NG validator in Java

Requires:       jpackage-utils
Requires:       java%{?headless} >= 1.5.0
Requires:       relaxngDatatype
Requires:       xerces-j2
Requires:       xml-commons-resolver

%description -n jing
Jing is a RELAX NG validator written in Java.  It implements the RELAX
NG 1.0 Specification, RELAX NG Compact Syntax, and parts of RELAX NG
DTD Compatibility, specifically checking of ID/IDREF/IDREFS.  It also
has experimental support for schema languages other than RELAX NG;
specifically W3C XML Schema, Schematron 1.5, and Namespace Routing
Language.

%package     -n jing-javadoc
Summary:        Javadoc API documentation for Jing

Requires:       java-javadoc
Requires:       relaxngDatatype-javadoc

%description -n jing-javadoc
Javadoc API documentation for Jing.

%package     -n trang
Summary:        Multi-format schema converter based on RELAX NG

Requires:       jpackage-utils
Requires:       java%{?headless} >= 1.5.0
Requires:       relaxngDatatype
Requires:       xerces-j2
Requires:       xml-commons-resolver

%description -n trang
Trang converts between different schema languages for XML.  It
supports the following languages: RELAX NG (both XML and compact
syntax), XML 1.0 DTDs, W3C XML Schema.  A schema written in any of the
supported schema languages can be converted into any of the other
supported schema languages, except that W3C XML Schema is supported
for output only, not for input.

%package     -n dtdinst
Summary:        XML DTD to XML instance format converter

Requires:       jpackage-utils
Requires:       java%{?headless} >= 1.5.0

%description -n dtdinst
DTDinst is a program for converting XML DTDs into an XML instance
format.


%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1
sed -i -e 's/\r//g' lib/isorelax.copying.txt
find . -name "OldSaxon*.java" -delete # No "old" saxon available in Fedora


%build
CLASSPATH=$(build-classpath beust-jcommander xalan-j2 xalan-j2-serializer) \
%ant -Dlib.dir=%{_javadir} -Dbuild.sysclasspath=last dist


%install
rm -rf $RPM_BUILD_ROOT *-%{version}

install -dm 755 $RPM_BUILD_ROOT{%{_javadir},%{_javadocdir}}

%{__unzip} build/dist/jing-%{version}.zip
install -Dpm 644 jing-%{version}/bin/jing.jar $RPM_BUILD_ROOT%{_javadir}
mv jing-%{version}/doc/api $RPM_BUILD_ROOT%{_javadocdir}/jing
ln -s %{_javadocdir}/jing jing-%{version}/doc/api
rm -f jing-%{version}/sample/datatype/datatype-sample.jar
%jpackage_script com.thaiopensource.relaxng.util.Driver "" "" jing:relaxngDatatype:xml-commons-resolver:xerces-j2 jing true

%{__unzip} build/dist/trang-%{version}.zip
install -pm 644 trang-%{version}/trang.jar $RPM_BUILD_ROOT%{_javadir}
%jpackage_script com.thaiopensource.relaxng.translate.Driver "" "" trang:relaxngDatatype:xml-commons-resolver:xerces-j2 trang true

%{__unzip} build/dist/dtdinst-%{version}.zip
install -pm 644 dtdinst-%{version}/dtdinst.jar $RPM_BUILD_ROOT%{_javadir}
%jpackage_script com.thaiopensource.xml.dtd.app.Driver "" "" dtdinst dtdinst true


%clean
rm -rf $RPM_BUILD_ROOT


%files -n jing
%defattr(-,root,root,-)
%doc jing-%{version}/{readme.html,doc,sample}
%{_bindir}/jing
%{_javadir}/jing.jar

%files -n jing-javadoc
%defattr(-,root,root,-)
%doc jing-%{version}/doc/{copying.html,isorelax.copying.txt,xerces.copying.txt}
%{_javadocdir}/jing/

%files -n trang
%defattr(-,root,root,-)
%doc trang-%{version}/*.{txt,html}
%{_bindir}/trang
%{_javadir}/trang.jar

%files -n dtdinst
%defattr(-,root,root,-)
%doc dtdinst-%{version}/{*.{txt,html,rng,xsl},example}
%{_bindir}/dtdinst
%{_javadir}/dtdinst.jar