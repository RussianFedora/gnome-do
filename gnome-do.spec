%define			debug_package %{nil}
%define                 mainver 0.8.0

Name:			gnome-do
Version:		%{mainver}
Release:		4%{?dist}
Summary:		Quick launch and search

License:		GPLv3+
Group:			Applications/File	
URL:			http://do.davebsd.com/
Source0:		http://launchpad.net/do/trunk/%{mainver}/+download/gnome-do-0.8.0.tar.gz

BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Various Mono dependencies are not available for ppc64; see bug 241850.
ExcludeArch:		ppc64

BuildRequires:		mono-devel, mono-addins-devel
BuildRequires:		desktop-file-utils
BuildRequires:		ndesk-dbus-devel
BuildRequires:		ndesk-dbus-glib-devel
BuildRequires:		gtk-sharp2-devel, notify-sharp-devel
BuildRequires:		gnome-sharp-devel, gnome-desktop-sharp-devel
BuildRequires:		gnome-keyring-sharp-devel
BuildRequires:		gettext
BuildRequires:		perl-XML-Parser
BuildRequires:		intltool
BuildRequires:		gtk2-devel

Requires(pre):		GConf2
Requires(post): 	GConf2
Requires(preun): 	GConf2

Requires:		mono-core mono-addins
Requires:		ndesk-dbus
Requires:		ndesk-dbus-glib
Requires:		gnome-keyring-sharp
Requires:		pkgconfig

%description
GNOME Do (Do) is an intelligent launcher tool that makes performing
common tasks on your computer simple and efficient. Do not only allows
you to search for items in your desktop environment
(e.g. applications, contacts, bookmarks, files, music), it also allows
you to specify actions to perform on search results (e.g. run, open,
email, chat, play).

%package devel
Summary:		Development files for GNOME Do
Group:			Development/Libraries
Requires:		%{name} = %{version}-%{release}
Requires:		pkgconfig

%description devel
Development files for GNOME Do

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor gnome --delete-original		\
	--dir $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart	\
	--add-only-show-in=GNOME				\
	$RPM_BUILD_ROOT%{_datadir}/applications/gnome-do.desktop

#own this dir:
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}

%find_lang %{name}

%pre
if [ "$1" -gt 1 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/%{name}.schemas >/dev/null || :
fi

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
  %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :

touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%preun
if [ "$1" -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYRIGHT
%{_bindir}/gnome-do/
%{_libdir}/gnome-do/
%dir %{_datadir}/gnome-do/
%config(noreplace) %{_sysconfdir}/xdg/autostart/gnome-do.desktop
%config(noreplace) %{_sysconfdir}/gconf/schemas/*
%{_datadir}/icons/hicolor/*/apps/gnome-do.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*

%changelog
* Tue Mar 3 2009 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.8.0-4
- Own _datadir/gnome-do
* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  7 2009 Michel Salim <salimma@fedoraproject.org> - 0.8.0-2
- Rebuild against new mono-addins

* Fri Jan 30 2009 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.8.0-1
- New upstream release

* Thu Jan 29 2009 Michel Salim <salimma@fedoraproject.org> - 0.6.1.0-3
- Remove Tomboy dependency (bz #481183)
- Updated description, from Do 

* Mon Oct 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.6.1.0-2
- rebuild against new gnome-sharp

* Wed Oct 08 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.6.1.0-1
- New Upstream Release

* Fri Oct 03 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.6.0.1-1
- New upstream release

* Wed Jun 11 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.6.0.0-1
- New upstream release

* Wed Jun 11 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.5.0.1-4
- New upstream release
- Add gnome-desktop-sharp dependency

* Wed Jun 04 2008 Caolán McNamara <caolanm@redhat.com> - 0.4.2.0-2
- rebuild for dependancies

* Tue Apr 22 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.4.2.0-1
- New upstream release

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
