%define			debug_package %{nil}

Name:			gnome-do
Version:		0.5.99
Release:		1%{?dist}
Summary:		Quick launch and search

License:		GPLv3+
Group:			Applications/File	
URL:			http://do.davebsd.com/
Source0:		http://launchpad.net/do/trunk/0.5/+download/%{name}-%{version}.tar.gz
# keyring's .pc file has been renamed in latest CVS
Patch0:			%{name}-0.5.0.1-keyring.patch
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Various Mono dependencies are not available for ppc64; see bug 241850.
ExcludeArch:		ppc64

BuildRequires:		mono-devel, mono-addins-devel
BuildRequires:		desktop-file-utils
BuildRequires:		ndesk-dbus-devel
BuildRequires:		ndesk-dbus-glib-devel
BuildRequires:		gtk-sharp2-devel
BuildRequires:		gnome-sharp-devel, gnome-desktop-sharp-devel
BuildRequires:		gnome-keyring-sharp-devel
BuildRequires:		gettext
BuildRequires:		perl-XML-Parser
BuildRequires:		intltool
BuildRequires:		gtk2-devel

Requires:		mono-core, mono-addins
Requires:		tomboy
Requires:		mono-core
Requires:		ndesk-dbus
Requires:		ndesk-dbus-glib
Requires:		gnome-keyring-sharp
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
%patch0 -p1 -b .keyring
#%patch1 -p1 -b .launcher


%build
%configure
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
%doc AUTHORS COPYING COPYRIGHT
%{_bindir}/gnome-do/
%{_libdir}/gnome-do/
%config(noreplace) %{_sysconfdir}/xdg/autostart/gnome-do.desktop

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*

%changelog
* Wed Jun 11 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.5.99-1
- New upstream release

* Wed Jun 11 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.5.0.1-4
- New upstrean release
- Add gnome-desktop-sharp dependency

* Wed Jun 04 2008 Caolán McNamara <caolanm@redhat.com> - 0.4.2.0-2
- rebuild for dependancies

* Tue Apr 22 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.4.2.0-1
- New upstrean release

* Tue Apr 01 2008 David Nielsen <gnomeuser@gmail.com> - 0.4.0.1-2
- #439793 - correct URL

* Sat Mar 29 2008 David Nielsen <gnomeuser@gmail.com> - 0.4.0.1-1
- Bump to 0.4.0.1
- Hopefully bring an end to the endless dups of 432201

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
