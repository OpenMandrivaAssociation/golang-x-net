%global debug_package %{nil}

%bcond_without bootstrap2

# Run tests in check section
%bcond_without check

# https://github.com/golang/net
%global goipath		golang.org/x//net
%global forgeurl	https://github.com/golang/net
Version:		0.22.0

%gometa

%if %{with bootstrap2}
%global __requires_exclude ^golang\\\(golang\\\.org\\\/x\\\/text.*\\\)$|^golang\\\(golang\\.org\\\/x\\\/crypto.*\\\)$
%endif
#\
#	|^golang\\\(golang.org/x/text.*\\\)$ \
#	|^golang\\\(golang\\.org\\\/x\\\/crypto.*\\\)$
Summary:	Go supplementary network libraries
Name:		golang-x-net

Release:	1
Source0:	https://github.com/golang/net/archive/v%{version}/net-%{version}.tar.gz
%if %{with bootstrap2}
# Generated from Source100
Source3:	vendor.tar.zst
Source100:	golang-package-dependencies.sh
%endif
URL:		https://github.com/golang/net
License:	BSD with advertising
Group:		Development/Other
BuildRequires:	compiler(go-compiler)
%if ! %{with bootstrap2}
BuildRequires:	compiler(golang.org/x/crypto)
BuildRequires:	compiler(golang.org/x/text)
%endif

%description
This package provides supplementary Go networking libraries.

#-----------------------------------------------------------------------

%package devel
Summary:	%{summary}
Group:		Development/Other
BuildArch:	noarch

%description devel
%{description}

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.

%files devel -f devel.file-list
%license LICENSE
%doc README.md

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n net-%{version}

rm -rf vendor

%if %{with bootstrap2}
tar xf %{S:3}
%endif

%build
%gobuildroot
for cmd in $(ls -1 cmd) ; do
	%gobuild -o _bin/$cmd %{goipath}/cmd/$cmd
done

%install
%goinstall
for cmd in $(ls -1 _bin) ; do
	install -Dpm 0755 _bin/$cmd %{buildroot}%{_bindir}/$cmd
done

%check
%if %{with check}
%gochecks
%endif

