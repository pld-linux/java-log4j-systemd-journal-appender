# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_without	source		# don't build source jar
%bcond_with	tests		# build and run tests

%define		srcname		log4j-systemd-journal-appender
%define		commit		60bc8eccbc031616504f812ec0d3c8902d3ce79f
%include	/usr/lib/rpm/macros.java
Summary:	Log4j appender for systemd-journal
Summary(pl.UTF-8):	Appended log4j dla journala systemd
Name:		java-%{srcname}
Version:	1.3.1
Release:	1
License:	BSD
Group:		Libraries/Java
Source0:	https://github.com/bwaldvogel/log4j-systemd-journal-appender/archive/%{commit}/%{srcname}.tar.gz
# Source0-md5:	d1cc409f362f86f2691f90e759dd0957
Patch0:		local_deps_only.patch
Patch1:		no_nexus.patch
URL:		https://github.com/bwaldvogel/log4j-systemd-journal-appender
BuildRequires:	gradle
BuildRequires:	java-jna >= 4.2.0
BuildRequires:	java-log4j
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
%if %{with source}
BuildRequires:	rpmbuild(macros) >= 1.555
%endif
BuildRequires:	sed >= 4.0
Requires:	java-jna >= 4.2.0
Requires:	java-log4j
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Log4j appender that logs event meta data such as the timestamp, the
logger name, the exception stacktrace, mapped diagnostic contexts
(MDC) or the Java thread name to fields in systemd journal (aka "the
Journal").

%package javadoc
Summary:	Online manual for %{srcname}
Summary(pl.UTF-8):	Dokumentacja online do %{srcname}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for %{srcname}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{srcname}.

%description javadoc -l fr.UTF-8
Javadoc pour %{srcname}.

%package demo
Summary:	Demo for %{srcname}
Summary(pl.UTF-8):	Pliki demonstracyjne dla pakietu %{srcname}
Group:		Documentation
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{srcname}.

%description demo -l pl.UTF-8
Pliki demonstracyjne i przykłady dla pakietu %{srcname}.

%package manual
Summary:	Tutorial for %{srcname}
Group:		Documentation

%description manual
Manual for %{srcname}.

%package source
Summary:	Source code of %{srcname}
Summary(pl.UTF-8):	Kod źródłowy %{srcname}
Group:		Documentation
Requires:	jpackage-utils >= 1.7.5-2

%description source
Source code of %{srcname}.

%description source -l pl.UTF-8
Kod źródłowy %{srcname}.

%prep
%setup -q -n %{srcname}-%{commit}
%patch0 -p1
%patch1 -p1

%build
export JAVA_HOME="%{java_home}"

gradle jar %{?with_javadoc:javadoc} %{?with_source:sourcesJar} %{?with_tests:test}

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p build/libs/%{srcname}-%{commit}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a build/docs/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

# source
%if %{with source}
install -d $RPM_BUILD_ROOT%{_javasrcdir}
cp -a build/libs/%{srcname}-%{commit}-%{version}-sources.jar $RPM_BUILD_ROOT%{_javasrcdir}/%{srcname}.src.jar
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/%{srcname}-%{version}.jar
%{_javadir}/%{srcname}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif

%if %{with source}
%files source
%defattr(644,root,root,755)
%{_javasrcdir}/%{srcname}.src.jar
%endif
