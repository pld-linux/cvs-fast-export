#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	Tool to export CVS history into a fast-import stream
Summary(pl.UTF-8):	Narzędzie eksportujące historię CVS w postaci strumienia fast-import
Name:		cvs-fast-export
Version:	1.62
Release:	1
License:	GPL v2
Group:		Development/Version Control
Source0:	http://www.catb.org/~esr/cvs-fast-export/%{name}-%{version}.tar.gz
# Source0-md5:	8ed2dac4c7c1763d8351650d0bb2630c
Patch0:		hack-disable-cvsignore.patch
URL:		http://www.catb.org/~esr/cvs-fast-export/
BuildRequires:	asciidoc
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	cvs
%endif
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

%description -l pl.UTF-8
To narzędzie eksportuje historię RCS lub CVS w postaci strumienia
fast-import. Program analizuje zbiór plików RCS w repozytorium CVS
(lub na zewnątrz) i, w miarę możliwości, wypuszcza odpowiadającą mu
historię w postaci strumienia fast-import. Nie wszystkie historie
można w ten sposób przedstawić - w razie problemów program próbuje
wypisać przydatne ostrzeżenia. Program potrafi także utworzyć
wizualizację wynikowego skierowanego grafu acyklicznego (DAG) zmian
(commitów) w formacie DOT, obsługiwanym przez narzędzia graphviz.
Pakiet zawiera także narzędzie cvssync do tworzenia kopii lustrzanych
ze zdalnych serwerów CVS.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e '1s,/usr/bin/env python3$,%{__python3},' cvsconvert cvsstrip

%build
%{__make} cvs-fast-export man \
	CC="%{__cc}" \
	EXTRA_CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%if %{with tests}
# tests are racy, use -j1
%{__make} -C tests -j1
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS.adoc README.adoc TODO.adoc
%attr(755,root,root) %{_bindir}/cvs-fast-export
%attr(755,root,root) %{_bindir}/cvsconvert
%attr(755,root,root) %{_bindir}/cvssync
%{_mandir}/man1/cvs-fast-export.1*
%{_mandir}/man1/cvsconvert.1*
%{_mandir}/man1/cvssync.1*
