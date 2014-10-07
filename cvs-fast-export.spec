#
# Conditional build:
%bcond_with	tests		# build without tests

Summary:	Tool to export CVS history into a fast-import stream
Name:		cvs-fast-export
Version:	1.14
Release:	1
License:	GPL v2
Group:		Applications
Source0:	http://www.catb.org/~esr/cvs-fast-export/%{name}-%{version}.tar.gz
# Source0-md5:	2ae209bc8a37609c717cf957320b1f35
URL:		http://www.catb.org/~esr/cvs-fast-export/
BuildRequires:	asciidoc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Export an RCS or CVS history as a fast-import stream. This program
analyzes a collection of RCS files in a CVS repository (or outside of
one) and, when possible, emits an equivalent history in the form of a
fast-import stream. Not all possible histories can be rendered this
way; the program tries to emit useful warnings when it can't. The
program can also produce a visualization of the resulting commit DAG
in the DOT format handled by the graphviz suite. The package also
includes cvssync, a tool for mirroring masters from remote CVS hosts.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	EXTRA_CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	prefix=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO
%attr(755,root,root) %{_bindir}/cvs-fast-export
%attr(755,root,root) %{_bindir}/cvssync
%{_mandir}/man1/cvs-fast-export.1*
%{_mandir}/man1/cvssync.1*
