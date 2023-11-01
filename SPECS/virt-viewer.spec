# -*- rpm-spec -*-

%global _hardened_build 1

# Default to skipping autoreconf.  Distros can change just this one line
# (or provide a command-line override) if they backport any patches that
# touch configure.ac or Makefile.am.
%{!?enable_autotools:%global enable_autotools 1}

%define with_spice 0
%if 0%{?fedora} >= 17 || 0%{?rhel} >= 6
%define with_spice 1
%endif

%define with_govirt 0
%if 0%{?fedora} > 19 || 0%{?rhel} >= 7
%define with_govirt 1
%endif

Name: virt-viewer
Version: 9.0
Release: 12%{?dist}%{?extra_release}
Summary: Virtual Machine Viewer
Group: Applications/System
License: GPLv2+
URL: https://virt-manager.org/
Source0: http://virt-manager.org/download/sources/%{name}/%{name}-%{version}.tar.gz

Patch001: 0001-DOWNSTREAM-Workaround-inconsistency-with-REST-API.patch
Patch002: 0002-DOWNSTREAM-ovirt-foreign-menu-Bypass-errors-from-Hos.patch
Patch003: 0003-DOWNSTREAM-remote-viewer-Set-admin-privileges-when-c.patch
Patch004: 0004-ovirt-Do-not-filter-out-DATA-storage-domains.patch
Patch005: 0005-display-error-message-on-no-extension-for-screenshot.patch
Patch006: 0006-ovirt-foreign-menu-Use-proper-function-in-the-case-o.patch
Patch007: 0007-ovirt-foreign-menu-Take-into-account-StorageDomains-.patch

#rhbz#1548371
Patch008: 0008-More-specific-key-accelerator-description.patch

#rhbz#1753563
Patch009: 0009-virt-viewer-file-transfer-dialog-Reports-detailed-er.patch

# rhbz#1848267
# Patches 10 and 12 slightly modified to match downstream
Patch010: 0010-ui-improve-homepage-in-about-dialog.patch
Patch011: 0011-about-ui-year-2020-in-Copyright.patch
Patch012: 0012-ui-about-po-update-pot-file.patch

# rhbz#1448151
Patch013: 0013-vnc-show-an-error-dialog-upon-vnc-error.patch
Patch022: 0022-vnc-no-dialog-for-server-closed-connection-error.patch

# rhbz#1876719
Patch014: 0014-Fix-warning-by-Coverity.patch

# rhbz#1791261
Patch015: 0015-windows-fix-nonuniform-behavior-of-zoom-hotkeys.patch
Patch016: 0016-hotkeys-enable-setting-zoom-hotkeys-from-command-lin.patch
Patch017: 0017-hotkeys-enable-setting-zoom-hotkeys-from-a-vv-file.patch
Patch018: 0018-tests-hotkeys-add-zoom-hotkeys.patch
# patch19 slightly modified, no usb-device-reset accel
Patch019: 0019-man-add-zoom-hotkeys.patch
Patch020: 0020-zoom-hotkeys-disable-numpad-when-users-set-new-hotke.patch

# rhbz#1893584
Patch021: 0021-disable-default-grab-sequence-in-kiosk-mode.patch

# Patch022 is defined earlier

# rhbz#1911224 and rhbz#1926691
# Patches slightly modified so they apply
Patch023: 0023-vnc-session-save-message-from-vnc-error-for-vnc-disc.patch
Patch024: 0024-session-remove-session-error-signal.patch
Patch025: 0025-vnc-session-use-g_signal_connect_object.patch
Patch026: 0026-build-fix-build-without-gtk-vnc.patch
Patch027: 0027-ovirt-foreign-menu-Support-changing-ISO-from-Data-St.patch

# rhbz#1855716
Patch028: 0028-iso-dialog-Give-less-scary-error-if-there-are-no-ISO.patch

Requires: openssh-clients
Requires(post):   %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%if 0%{?enable_autotools}
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gettext-devel
BuildRequires: libtool
%endif

BuildRequires: gcc
BuildRequires: pkgconfig(glib-2.0) >= 2.38
BuildRequires: pkgconfig(gtk+-3.0) >= 3.18
BuildRequires: pkgconfig(libvirt) >= 0.10.0
BuildRequires: pkgconfig(libvirt-glib-1.0) >= 0.1.8
BuildRequires: pkgconfig(libxml-2.0) >= 2.6.0
BuildRequires: pkgconfig(gtk-vnc-2.0) >= 0.4.0
%if %{with_spice}
BuildRequires: pkgconfig(spice-client-gtk-3.0) >= 0.35
BuildRequires: pkgconfig(spice-protocol) >= 0.12.7
%endif
BuildRequires: /usr/bin/pod2man
BuildRequires: intltool
%if %{with_govirt}
BuildRequires: pkgconfig(govirt-1.0) >= 0.3.2
%endif

%if 0%{?fedora} >= 20
Obsoletes: spice-client < 0.12.3-2
%endif


%description
Virtual Machine Viewer provides a graphical console client for connecting
to virtual machines. It uses the GTK-VNC or SPICE-GTK widgets to provide
the display, and libvirt for looking up VNC/SPICE server details.

%prep
%setup -q

%patch001 -p1
%patch002 -p1
%patch003 -p1
%patch004 -p1
%patch005 -p1
%patch006 -p1
%patch007 -p1

%patch008 -p1
%patch009 -p1

%patch010 -p1
%patch011 -p1
%patch012 -p1

%patch013 -p1
%patch014 -p1

%patch015 -p1
%patch016 -p1
%patch017 -p1
%patch018 -p1
%patch019 -p1
%patch020 -p1

%patch021 -p1
%patch022 -p1

%patch023 -p1
%patch024 -p1
%patch025 -p1
%patch026 -p1
%patch027 -p1

%patch028 -p1

%build

%if 0%{?enable_autotools}
autoreconf -if
%endif

%if %{with_spice}
%define spice_arg --with-spice-gtk
%else
%define spice_arg --without-spice-gtk
%endif

%if %{with_govirt}
%define govirt_arg --with-ovirt
%endif

%configure %{spice_arg} %{govirt_arg} --with-buildid=%{release} --disable-update-mimedb --with-osid=rhel%{?rhel}
%__make %{?_smp_mflags} V=1


%install
rm -rf $RPM_BUILD_ROOT
%__make install  DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}

%files -f %{name}.lang
%doc README.md COPYING AUTHORS ChangeLog NEWS
%{_bindir}/%{name}
%{_bindir}/remote-viewer
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/devices/*
%{_datadir}/applications/remote-viewer.desktop
%{_datadir}/appdata/remote-viewer.appdata.xml
%{_datadir}/mime/packages/virt-viewer-mime.xml
%{_mandir}/man1/virt-viewer.1*
%{_mandir}/man1/remote-viewer.1*

%changelog
* Sun Oct 31 2021 Uri Lublin <uril@redhat.com> - 9.0-12
- iso-dialog: Give less scary error if there are no ISOs
  Resolves: rhbz#1855716

* Thu Aug 26 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 9.0.11
- Add support for changing ISO fom Data StorageDomain
  Resolves: rhbz#1835640

* Wed Mar 10 2021 Uri Lublin <uril@redhat.com> - 9.0-10
- VNC: errors handling improvements
  Resolves: rhbz#1911224
  Resolves: rhbz#1926691

* Thu Jan 21 2021 Uri Lublin <uril@redhat.com> - 9.0-9
- Show an error dialog upon vnc-error only if session was initialized
  Resolves: rhbz#1448151

* Mon Jan 18 2021 Uri Lublin <uril@redhat.com> - 9.0-8
- Disable default grab sequence in kiosk mode
  Resolves: rhbz#1893584

* Mon Jan 11 2021 Uri Lublin <uril@redhat.com> - 9.0-7
- Fix some zoom hotkeys issues
  Resolves: rhbz#1791261

* Tue Dec 22 2020 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 9.0-6
- Add back support for DATA storage domains.
  Resolves: rhbz#1835640

* Thu Dec 03 2020 Uri Lublin <uril@redhat.com> - 9.0-5
- More specific key accelerator description for cursor release
  Resolves: rhbz#1548371
- Report detailed error when file transfer fails
  Resolves: rhbz#1753563
- Update copyright year in "about ui"
  Resolves: rhbz#1848267
- Show an error dialog upon vnc-error
  Resolves: rhbz#1448151
- Fix warning by Coverity
  Resolves: rhbz#1876719

* Fri Aug 28 2020 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 9.0-4
- Revert support for DATA storage domains temporarily.
  Resolves: rhbz#1873549

* Thu Jun 25 2020 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 9.0-3
- Handle DATA storage domains properly
  Resolves: rhbz#1835640

* Tue Jun 9 2020 Julien Rope <jrope@redhat.com> - 9.0-2
- Display an error when no extension is given to a screenshot.
  Resolves: rhbz#1752514

* Tue May 19 2020 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 9.0-1
- Rebase to latest upstream
  Resolves: rhbz#1837489
- Do not filter out DATA storage domains
  Resolves: rhbz#1835640

* Tue Dec 17 2019 Victor Toso <victortoso@redhat.com> - 7.0-9
- Always add vm's name to settings file
  Related: rhbz#1750706

* Tue Aug 27 2019 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 7.0-8
- Request tolplevel storage domain API object
  Related: rhbz#1717900

* Mon Aug 19 2019 Kevin Pouget <kpouget@redhat.com> - 7.0-7
- Improve the error shown to the user when a file transfer fails.
  Resolves: rhbz#1496356

* Fri Aug 16 2019 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 7.0-6
- Bypass errors from oVirt foreign menu queries
  Resolves: rhbz#1717900

* Mon Jul 22 2019 Victor Toso <victortoso@redhat.com> - 7.0-5
- Listen to SpiceSession::disconnected
  Resolves: rhbz#1655957

* Wed Mar 20 2019 Victor Toso <victortoso@redhat.com> - 7.0-4
- Some .spec file changes missed by rebase from F28 on RHEL-8.0
  Resolves: rhbz#1660060

* Tue Dec 18 2018 Victor Toso <victortoso@redhat.com> - 7.0-3
- Fix connection with ovirt
  Resolves: rhbz#1584561

* Tue Oct 16 2018 Jonathon Jongsma <jjongsma@redhat.com> - 7.0-2
- Fix fullscreen displays on wrong monitors in wayland
  Resolves: rhbz#1584561

* Fri Jul 27 2018 Daniel P. Berrangé <berrange@redhat.com> - 7.0-1
- Update to 7.0 release

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Fabiano Fidêncio <fidencio@fedoraproject.org> - 6.0-5
- Add missing patch for spice-controller so being removed

* Thu Jun 28 2018 Daniel P. Berrangé <berrange@redhat.com> - 6.0-4
- Rebuild for spice-controller so being removed

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6.0-2
- Remove obsolete scriptlets

* Tue Aug 15 2017 Daniel P. Berrange <berrange@redhat.com> - 6.0-1
- Update to 6.0 release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Nov 24 2016 Daniel P. Berrange <berrange@redhat.com> - 5.0-1
- Update to 5.0 release

* Wed Oct 05 2016 Christophe Fergeau <cfergeau@redhat.com> 4.0-2
- Add upstream patch fixing virt-viewer window gradually getting bigger and
  bigger

* Thu Jun 30 2016 Daniel P. Berrange <berrange@redhat.com> - 4.0-1
- Update to 4.0 release

* Wed Jun 22 2016 Christophe Fergeau <cfergeau@redhat.com> - 3.0-3
- Rebuild for spice-gtk ABI break

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec  4 2015 Fabiano Fidêncio <fidencio@redhat.com> - 3.0-1
- Update to 3.0 release

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 12 2015 Daniel P. Berrange <berrange@redhat.com> - 2.0-1
- Update to 2.0 release

* Sat Sep 27 2014 Rex Dieter <rdieter@fedoraproject.org> - 1.0-3
- update/optimize mime scriptlets

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 21 2014 Daniel P. Berrange <berrange@redhat.com> - 1.0-1
- Update to 1.0 release

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 26 2014 Christophe Fergeau <cfergeau@redhat.com> 0.6.0-1
- Update to 0.6.0 release

* Tue Nov 26 2013 Christophe Fergeau <cfergeau@redhat.com> 0.5.7-2
- Rebuild for new libgovirt

* Wed Jul 31 2013 Daniel P. Berrange <berrange@redhat.com> - 0.5.7-1
- Update to 0.5.7 release

* Thu May 23 2013 Christophe Fergeau <cfergeau@redhat.com> - 0.5.6-2
- Mark remote-viewer as replacing spice-client

* Wed May  1 2013 Daniel P. Berrange <berrange@redhat.com> - 0.5.6-1
- Update to 0.5.6 release

* Wed Feb 13 2013 Daniel P. Berrange <berrange@redhat.com> - 0.5.5-1
- Update to 0.5.5 release

* Fri Dec 14 2012 Cole Robinson <crobinso@redhat.com> - 0.5.4-3
- Fix crash after entering spice password (bz #880381)

* Sat Oct 13 2012 Chris Tyler <chris@tylers.info> - 0.5.4-2
- Enabled spice support for ARM archs

* Mon Sep 17 2012 Daniel P. Berrange <berrange@redhat.com> - 0.5.4-1
- Update to 0.5.4 release

* Fri Sep 14 2012 Hans de Goede <hdegoede@redhat.com> - 0.5.3-6
- Rebuild for spice-gtk ABI breakage (previous spice-gtk build was borked)

* Tue Sep 11 2012 Hans de Goede <hdegoede@redhat.com> - 0.5.3-5
- Rebuild for spice-gtk ABI breakage

* Fri Sep  7 2012 Hans de Goede <hdegoede@redhat.com> - 0.5.3-4
- Rebuild for spice-gtk soname change

* Mon Aug 13 2012 Daniel P. Berrange <berrange@redhat.com> - 0.5.3-3
- Rebuild for spice-gtk soname change

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 16 2012 Daniel P. Berrange <berrange@redhat.com> - 0.5.3-1
- Update to 0.5.3 release

* Fri Mar  9 2012 Daniel P. Berrange <berrange@redhat.com> - 0.5.2-1
- Update to 0.5.2 release

* Fri Feb 17 2012 Daniel P. Berrange <berrange@redhat.com> - 0.5.1-1
- Update to 0.5.1 release

* Tue Feb 14 2012 Daniel P. Berrange <berrange@redhat.com> - 0.5.0-1
- Update to 0.5.0 release

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov  9 2011 Daniel P. Berrange <berrange@redhat.com> - 0.4.2-1
- Update to 0.4.2 release

* Sun Aug 14 2011 Daniel P. Berrange <berrange@redhat.com> - 0.4.1-3
- More ssh tunnelling port fixes

* Fri Aug 12 2011 Daniel P. Berrange <berrange@redhat.com> - 0.4.1-2
- Fix ssh tunnelling

* Thu Aug  4 2011 Daniel P. Berrange <berrange@redhat.com> - 0.4.1-1
- Update to 0.4.1 release

* Tue Aug  2 2011 Daniel P. Berrange <berrange@redhat.com> - 0.4.0-2
- Rebuild for accidental spice-glib soname change

* Tue Jul 12 2011 Daniel P. Berrange <berrange@redhat.com> - 0.4.0-1
- Update to 0.4.0 release
- Switch build to GTK3 instead of GTK2

* Tue May 31 2011 Daniel P. Berrange <berrange@redhat.com> - 0.3.1-2
- Rebuild for spice-glib ABI breakage

* Wed May 11 2011 Karsten Hopp <karsten@redhat.com> 0.3.1-1.1
- spice-gtk is x86 x86_64 only, don't require it on other archs

* Mon Feb 21 2011 Daniel P. Berrange <berrange@redhat.com> - 0.3.1-1
- Update to 0.3.1 release

* Mon Feb 21 2011 Daniel P. Berrange <berrange@redhat.com> - 0.3.0-1
- Update to 0.3.0 and enable SPICE

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 15 2010 Daniel P. Berrange <berrange@redhat.com> - 0.2.1-1
- Update to 0.2.1 release

* Wed Jul 29 2009 Daniel P. Berrange <berrange@redhat.com> - 0.2.0-1.fc12
- Update to 0.2.0 release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May  7 2009 Daniel P. Berrange <berrange@redhat.com> - 0.0.3-5.fc12
- Fix auth against libvirt (rhbz #499594)
- Fix confusion of VNC credentials (rhbz #499595)
- Correct keyboard grab handling (rhbz #499362)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.0.3-3.fc10
- fix conditional comparison
- remove file dep

* Wed Jun 25 2008 Daniel P. Berrange <berrange@redhat.com> - 0.0.3-2.fc10
- Rebuild for GNU TLS ABI bump

* Mon Mar 10 2008 Daniel P. Berrange <berrange@redhat.com> - 0.0.3-1.fc9
- Updated to 0.0.3 release

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.0.2-4
- Autorebuild for GCC 4.3

* Fri Jan 11 2008 Daniel P. Berrange <berrange@redhat.com> - 0.0.2-3.fc9
- Set domain name as window title
- Hide input for passwd fields during auth

* Mon Oct 15 2007 Daniel P. Berrange <berrange@redhat.com> - 0.0.2-2.fc8
- Change TLS x509 credential name to sync with libvirt

* Tue Aug 28 2007 Daniel P. Berrange <berrange@redhat.com> - 0.0.2-1.fc8
- Added support for remote console access

* Fri Aug 17 2007 Daniel P. Berrange <berrange@redhat.com> - 0.0.1-2.fc8
- Restrict built to x86 & ia64 because libvirt is only on those arches

* Wed Aug 15 2007 Daniel P. Berrange <berrange@redhat.com> - 0.0.1-1.fc8
- First release
