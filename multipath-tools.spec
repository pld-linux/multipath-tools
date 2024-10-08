#
# Conditional build:
%bcond_with	initrd		# build initrd version (very broken)
%bcond_without	systemd		# systemd support

Summary:	Tools to manage multipathed devices with the device-mapper
Summary(pl.UTF-8):	Implementacja wielotrasowego dostępu do zasobów przy użyciu device-mappera
Name:		multipath-tools
Version:	0.10.0
Release:	1
License:	GPL v2
Group:		Base
#Source0Download: https://github.com/opensvc/multipath-tools/tags
Source0:	https://github.com/opensvc/multipath-tools/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	025586178f9daedc857bc13a36963bb1
Source100:	branch.sh
Source1:	multipathd.init
Source2:	multipathd.sysconfig
Source3:	%{name}-bindings
# http://git.opensvc.com/?p=multipath-tools/.git;a=blob_plain;f=multipath.conf.defaults;hb=d569988e7528cf3484b6acae19dc093de41a2488
Source4:	multipath.conf.defaults
Patch0:		%{name}-paths.patch
Patch1:		%{name}-kpartx-udev.patch
Patch2:		config.patch
Patch3:		%{name}-prototype.patch
Patch4:		%{name}-types.patch
URL:		http://christophe.varoqui.free.fr/
BuildRequires:	device-mapper-devel >= 1.02.08
BuildRequires:	json-c-devel
BuildRequires:	libaio-devel
BuildRequires:	libmount-devel
BuildRequires:	linux-libc-headers >= 7:2.6.12.0-5
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	sed >= 4.0
%{?with_systemd:BuildRequires:	systemd-devel >= 1:209}
BuildRequires:	udev-devel
BuildRequires:	userspace-rcu-devel
%if %{with initrd}
BuildRequires:	device-mapper-initrd-devel
BuildRequires:	klibc-static
%endif
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-libs = %{version}-%{release}
Requires:	device-mapper >= 1.02.08
Requires:	kpartx = %{version}-%{release}
Requires:	libaio >= 0.3.106-2
Requires:	rc-scripts
Requires:	systemd-units >= 38
Requires:	udev-core >= 1:127
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
multipath-tools provides the tools to manage multipathed devices by
instructing the device-mapper multipath module what to do. The tools
are:
- multipath: scan the system for multipathed devices, assembles them
  and update the device-mapper's maps
- multipathd: wait for maps events, then execs multipath
- devmap-name: provides a meaningful device name to udev for devmaps

%description -l pl.UTF-8
multipath-tools zawierają narzędzia do zarządzania wielotrasowym
dostępem do urządzeń poprzez instruowanie modułu multipath
device-mappera. Narzędzia to:
- multipath - przeszukuje system pod kątem urządzeń z dostępem
  wielotrasowym, łączy je i uaktualnia odwzorowania device-mappera
- multipathd - oczekuje na zdarzenia odwzorowań, po których uruchamia
  multipath
- devmap-name - dostarcza do udev znaczącą nazwę urządzenia dla map
  urządzeń

%package libs
Summary:	Shared libraries for multipath-tools
Summary(pl.UTF-8):	Biblioteki współdzielone multipath-tools
Group:		Libraries
Requires:	device-mapper-libs >= 1.02.08

%description libs
Shared libraries for multipath-tools.

%description libs -l pl.UTF-8
Biblioteki współdzielone multipath-tools.

%package devel
Summary:	Header files for multipath-tools libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek multipath-tools
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for multipath-tools libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek multipath-tools.

%package -n kpartx
Summary:	Partition device manager for device-mapper devices
Summary(pl.UTF-8):	Zarządca urządzeń partycji dla urządzeń device-mappera
Group:		Base
Requires:	device-mapper-libs >= 1.02.08
Conflicts:	udev-core < 1:127

%description -n kpartx
kpartx maps linear devmaps upon device partitions, which makes
multipath maps partionable.

%description -n kpartx -l pl.UTF-8
kpartx odwzorowuje liniowe mapy urządzeń na partycje urządzeń, co
umożliwia tworzenie partycji na odwzorowaniach wielotrasowych.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
cp -p %{SOURCE4} .
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%if %{with initrd}
%{__make} -j1 \
	BUILD=klibc \
	CC="klcc -static" \
	OPTFLAGS="%{rpmcflags} %{rpmcppflags} -Wall -Wunused -Wstrict-prototypes" \
	BUILDDIRS='multipath pathx' \
	klibcdir=%{_libdir}/klibc \
	libdm='$(klibcdir)/libdevmapper.a'

%{__make} clean
%endif

%{__make} -j1 \
	CC="%{__cc}" \
	LIB=%{_lib} \
	OPTFLAGS="%{rpmcflags} %{rpmcppflags} -Wall -Wunused -Wstrict-prototypes %{?debug:-DDEBUG=1}" \
	V=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_sysconfdir}/multipath,/%{_lib}/multipath}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIB=%{_lib} \
	V=1 \
	libudevdir=/lib/udev \
	unitdir=%{systemdunitdir} \
	usr_prefix=%{_prefix}

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/multipathd
cp -p multipath.conf.defaults $RPM_BUILD_ROOT%{_sysconfdir}/multipath.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/multipathd
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/multipath/bindings

# devel files in /usr
install -d $RPM_BUILD_ROOT%{_libdir}
%{__rm} $RPM_BUILD_ROOT/%{_lib}/{libmpathcmd,libmpathpersist,libmpathutil,libmpathvalid,libmultipath}.so
ln -sf /%{_lib}/libmpathpersist.so.0 $RPM_BUILD_ROOT%{_libdir}/libmpathpersist.so
ln -sf /%{_lib}/libmpathcmd.so.0 $RPM_BUILD_ROOT%{_libdir}/libmpathcmd.so
ln -sf /%{_lib}/libmpathutil.so.0 $RPM_BUILD_ROOT%{_libdir}/libmpathutil.so
ln -sf /%{_lib}/libmpathvalid.so.0 $RPM_BUILD_ROOT%{_libdir}/libmpathvalid.so
ln -sf /%{_lib}/libmultipath.so.0 $RPM_BUILD_ROOT%{_libdir}/libmultipath.so

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add multipathd
%service multipathd restart
%systemd_post multipathd.service

%preun
if [ "$1" = "0" ]; then
	%service multipathd stop
	/sbin/chkconfig --del multipathd
fi
%systemd_preun multipathd.service

%postun
%systemd_reload

%triggerpostun -- %{name} < 0.4.9-7
%systemd_trigger multipathd.service

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md multipath.conf.defaults
%attr(755,root,root) %{_sbindir}/mpathpersist
%attr(755,root,root) %{_sbindir}/multipath
%attr(755,root,root) %{_sbindir}/multipathc
%attr(755,root,root) %{_sbindir}/multipathd
%dir /%{_lib}/multipath
%attr(755,root,root) /%{_lib}/multipath/libcheck*.so
%attr(755,root,root) /%{_lib}/multipath/libforeign-nvme.so
%attr(755,root,root) /%{_lib}/multipath/libprio*.so
%attr(754,root,root) /etc/rc.d/init.d/multipathd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/multipathd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/multipath.conf
%dir %{_sysconfdir}/multipath
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/multipath/bindings
/lib/udev/rules.d/11-dm-mpath.rules
/lib/udev/rules.d/11-dm-parts.rules
/lib/udev/rules.d/56-multipath.rules
/lib/udev/rules.d/99-z-dm-mpath-late.rules
# TODO: package for systemd?
#/usr/lib/modules-load.d/multipath.conf
%if %{with systemd}
%{systemdunitdir}/multipathd.service
%{systemdunitdir}/multipathd.socket
%endif
%{systemdtmpfilesdir}/multipath.conf
%{_mandir}/man5/multipath.conf.5*
%{_mandir}/man8/mpathpersist.8*
%{_mandir}/man8/multipath.8*
%{_mandir}/man8/multipathc.8*
%{_mandir}/man8/multipathd.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libmpathcmd.so.0
%attr(755,root,root) /%{_lib}/libmpathpersist.so.0
%attr(755,root,root) /%{_lib}/libmpathutil.so.0
%attr(755,root,root) /%{_lib}/libmpathvalid.so.0
%attr(755,root,root) /%{_lib}/libmultipath.so.0
%attr(755,root,root) %{_libdir}/libdmmp.so.0.2.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdmmp.so
%attr(755,root,root) %{_libdir}/libmpathcmd.so
%attr(755,root,root) %{_libdir}/libmpathpersist.so
%attr(755,root,root) %{_libdir}/libmpathutil.so
%attr(755,root,root) %{_libdir}/libmpathvalid.so
%attr(755,root,root) %{_libdir}/libmultipath.so
%{_includedir}/libdmmp
%{_includedir}/mpath_cmd.h
%{_includedir}/mpath_persist.h
%{_includedir}/mpath_valid.h
%{_pkgconfigdir}/libdmmp.pc
%{_mandir}/man3/dmmp_*.3*
%{_mandir}/man3/libdmmp.h.3*
%{_mandir}/man3/mpath_persistent_reserve_in.3*
%{_mandir}/man3/mpath_persistent_reserve_out.3*

%files -n kpartx
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/kpartx
%attr(755,root,root) /lib/udev/kpartx_id
/lib/udev/rules.d/66-kpartx.rules
/lib/udev/rules.d/68-del-part-nodes.rules
%{_mandir}/man8/kpartx.8*
