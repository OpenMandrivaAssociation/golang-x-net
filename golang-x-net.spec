%global debug_package %{nil}

# Run tests in check section
%bcond_without check

# https://github.com/golang/net
%global goipath		golang.org/x//net
%global forgeurl	https://github.com/golang/net
Version:		0.30.0

%gometa

Summary:	Go supplementary network libraries
Name:		golang-x-net

Release:	1
Source0:	https://github.com/golang/net/archive/v%{version}/net-%{version}.tar.gz
URL:		https://github.com/golang/net
License:	BSD with advertising
Group:		Development/Other
BuildRequires:	compiler(go-compiler)
BuildRequires:	golang(golang.org/x/crypto/chacha20)
BuildRequires:	golang(golang.org/x/crypto/chacha20poly1305)
BuildRequires:	golang(golang.org/x/crypto/cryptobyte)
BuildRequires:	golang(golang.org/x/crypto/hkdf)
BuildRequires:	golang(golang.org/x/sys/unix)
BuildRequires:	golang(golang.org/x/term)
BuildRequires:	golang(golang.org/x/text/encoding)
BuildRequires:	golang(golang.org/x/text/encoding/charmap)
BuildRequires:	golang(golang.org/x/text/encoding/htmlindex)
BuildRequires:	golang(golang.org/x/text/secure/bidirule)
BuildRequires:	golang(golang.org/x/text/transform)
BuildRequires:	golang(golang.org/x/text/unicode/bidi)
BuildRequires:	golang(golang.org/x/text/unicode/norm)

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

