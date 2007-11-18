%define			debug_package %{nil}

Name:			gnome-do
Version:		0.0.2
Release:		2%{?dist}
Summary:		Quick launch and search

License:		GPLv3+
Group:			Applications/File	
URL:			https://edge.launchpad.net/gc/
Source0:		http://do.davebsd.com/src/%{name}_%{version}.orig.tar.gz
Patch0:			%{name}-libdir.patch
Patch1:			%{name}-desktopfile.patch
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Various Mono dependencies are not available for ppc64; see bug 241850.
ExcludeArch:		ppc64

BuildRequires:		mono-devel
BuildRequires:		desktop-file-utils
BuildRequires:		ndesk-dbus-devel
BuildRequires:		ndesk-dbus-glib-devel
BuildRequires:		gtk-sharp2-devel
BuildRequires:		gnome-sharp-devel

Requires:		mono-core

%description
Allows you to quickly search for many objects present in your
GNOME desktop environment and perform commonly used commands 
on those objects

%package devel
Summary:		Develpment files for GNOME Do
Group:			Development/Libraries
Requires:		%{name} = %{version}-%{release}
Requires:		pkgconfig

%description devel
Development files for GNOME Do

%prep
%setup -q -n do-0.1

# fix libdir, https://bugs.edge.launchpad.net/gc/+bug/162255
%patch0 -p1 -b .libdir
# adjust .desktop to have non-localized GenericName
%patch1 -p1 -b .desktopfile

%configure

%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor gnome --delete-original		\
	--dir $RPM_BUILD_ROOT%{_datadir}/applications		\
	--add-only-show-in=GNOME				\
	$RPM_BUILD_ROOT%{_datadir}/applications/gnome-do.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/gnome-do
%{_libdir}/do/*
%{_datadir}/applications/gnome-do.desktop

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*

%changelog
* Sat Nov 17 2007 David Nielsen <david@lovesunix.net> - 0.0.2-2
- updated libdir patch
- cleaned up desktop-file-install invocation
- correct BuildRequires

* Mon Nov 12 2007 David Nielsen <david@lovesunix.net> - 0.0.2-1
- Initial package
