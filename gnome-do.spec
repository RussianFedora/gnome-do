%define			debug_package %{nil}

Name:			gnome-do
Version:		0.3.1
Release:		4%{?dist}
Summary:		Quick launch and search

License:		GPLv3+
Group:			Applications/File	
URL:			https://edge.launchpad.net/gc/
Source0:		http://do.davebsd.com/src/%{name}-%{version}.tar.gz
Patch0:			%{name}-libdir.patch
Patch1:			%{name}-desktopfile.patch
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# JIT only availible on these:
ExclusiveArch:		%ix86 x86_64 ppc ia64 armv4l sparc alpha

BuildRequires:		mono-devel
BuildRequires:		desktop-file-utils
BuildRequires:		ndesk-dbus-devel
BuildRequires:		ndesk-dbus-glib-devel
BuildRequires:		gtk-sharp2-devel
BuildRequires:		gnome-sharp-devel
BuildRequires:		gettext
BuildRequires:		perl-XML-Parser
BuildRequires:		intltool

Requires:		mono-core
Requires:		tomboy
Requires:		ndesk-dbus
Requires:		ndesk-dbus-glib
Requires:		pkgconfig

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
%setup -q

# fix libdir
%patch0 -p1 -b .libdir

# adjust .desktop, Version setting breaks spec.
%patch1 -p1 -b .desktopfile

%configure

%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor gnome --delete-original		\
	--dir $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart	\
	--add-only-show-in=GNOME				\
	$RPM_BUILD_ROOT%{_datadir}/applications/gnome-do.desktop

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/gnome-do/
%{_libdir}/gnome-do/
%{_sysconfdir}/xdg/autostart/gnome-do.desktop

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*

%changelog
* Fri Feb 29 2008 David Nielsen <gnomeuser@gmail.com> - 0.3.1-4
- Actually do the jit change

* Fri Feb 29 2008 David Nielsen <gnomeuser@gmail.com> - 0.3.1-3
- #432201 - try 2
- Better excluding of non mono JIT archs

* Thu Feb 21 2008 David Nielsen <david@lovesunix.net> - 0.3.1-2
- Fix 432201

* Thu Feb 21 2008 David Nielsen <david@lovesunix.net> - 0.3.1-1
- Bump to 0.3.1

* Wed Feb 06 2008 David Nielsen <david@lovesunix.net> - 0.3.0.1-5
- #431589 - Force runtime dependency on ndesk-dbus(-glib)

* Mon Feb 04 2008 David Nielsen <david@lovesunix.net> - 0.3.0.1-4
- #431462 - Correctly pull in Tomboy runtime dependency

* Fri Jan 25 2008 David Nielsen <david@lovesunix.net> - 0.3.0.1-3
- autostart gnome-do in quiet mode with the user session
- to invoke gnome-do use super+space

* Tue Jan 22 2008 David Nielsen <david@lovesunix.net> - 0.3.0.1-2
- Fix BuildRequires

* Tue Jan 22 2008 David Nielsen <david@lovesunix.net> - 0.3.0.1-1
- bump to 0.3.0.1
- update patches

* Sat Nov 17 2007 David Nielsen <david@lovesunix.net> - 0.0.2-2
- updated libdir patch
- cleaned up desktop-file-install invocation
- correct BuildRequires

* Mon Nov 12 2007 David Nielsen <david@lovesunix.net> - 0.0.2-1
- Initial package
