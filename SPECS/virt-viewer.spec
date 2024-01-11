# -*- rpm-spec -*-

%if 0%{?rhel} >= 9
%global with_govirt 0
%global with_spice 0
%else
%global with_govirt 1
%global with_spice 1
%endif

Name: virt-viewer
Version: 11.0
Release: 1%{?dist}
Summary: Virtual Machine Viewer
License: GPLv2+
URL: https://gitlab.com/virt-viewer/virt-viewer
Source0: https://virt-manager.org/download/sources/%{name}/%{name}-%{version}.tar.xz
Requires: openssh-clients

# Our bash completion script uses virsh to list domains
Requires: libvirt-client

BuildRequires: gcc
BuildRequires: meson
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(libvirt)
BuildRequires: pkgconfig(libvirt-glib-1.0)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(gtk-vnc-2.0)
BuildRequires: pkgconfig(vte-2.91)
%if %{with_spice}
BuildRequires: pkgconfig(spice-client-gtk-3.0)
BuildRequires: pkgconfig(spice-protocol)
%endif
BuildRequires: /usr/bin/pod2man
BuildRequires: gettext
%if %{with_govirt}
BuildRequires: pkgconfig(govirt-1.0)
BuildRequires: pkgconfig(rest-0.7)
%endif
BuildRequires: pkgconfig(bash-completion)


%description
Virtual Machine Viewer provides a graphical console client for connecting
to virtual machines. It uses the GTK-VNC or SPICE-GTK widgets to provide
the display, and libvirt for looking up VNC/SPICE server details.

%prep
%autosetup -p1

%build

%define buildid_opt -Dbuild-id=%{release}

%if !%{with_govirt}
%define ovirt_opt -Dovirt=disabled
%endif

%if !%{with_spice}
%define spice_opt -Dspice=disabled
%endif

%if 0%{?rhel} > 0
%define osid_opt -Dos-id=rhel%{?rhel}
%endif

%meson %{buildid_opt} %{?ovirt_opt} %{?spice_opt} %{?osid_opt}
%meson_build

%install
%meson_install

%find_lang %{name}

%files -f %{name}.lang
%doc README.md COPYING AUTHORS NEWS
%{_bindir}/%{name}
%{_bindir}/remote-viewer
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/applications/remote-viewer.desktop
%{_datadir}/metainfo/remote-viewer.appdata.xml
%{_datadir}/mime/packages/virt-viewer-mime.xml
%{_mandir}/man1/virt-viewer.1*
%{_mandir}/man1/remote-viewer.1*
%{_datadir}/bash-completion/completions/virt-viewer

%changelog
* Wed Dec  8 2021 Daniel P. Berrangé <berrange@redhat.com> - 11.0-1
- Rebase to 11.0 release
- Add missing dep on libvirt-client for bash completion
- Resolves: rhbz#2028604, rhbz#2000528

* Thu Aug 19 2021 Uri Lublin <uril@redhat.com> - 10.0-3
- Show OS-ID when running 'remote-viewer -V'
  Resolves: rhbz#1953282
- Clear auth entry fields
  Resolves: rhbz#1953933

* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 10.0-2
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Wed Apr 21 2021 Daniel P. Berrangé <berrange@redhat.com> - 10.0-1
- Update to 10.0 release
- Resolves: rhbz#1949526

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 9.0-4
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May  1 2020 Daniel P. Berrangé <berrange@redhat.com> - 9.0-1
- Update to 9.0 release

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
