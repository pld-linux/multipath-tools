#
# Conditional build:
%bcond_with	initrd		# build initrd version (very broken)

Summary:	Tools to manage multipathed devices with the device-mapper
Summary(pl.UTF-8):	Implementacja wielotrasowego dostępu do zasobów przy użyciu device-mappera
Name:		multipath-tools
Version:	0.5.0
Release:	1
License:	GPL v2
Group:		Base
Source0:	http://christophe.varoqui.free.fr/multipath-tools/%{name}-%{version}.tar.bz2
# Source0-md5:	faf261d4cc717bf4c979557dc7bf5f52
Source100:	branch.sh
Source1:	multipathd.init
Source2:	multipathd.sysconfig
Source3:	%{name}-bindings
Patch0:		%{name}-format.patch
Patch1:		%{name}-kpartx-udev.patch
Patch2:		config.patch
URL:		http://christophe.varoqui.free.fr/
BuildRequires:	device-mapper-devel >= 1.02.08
BuildRequires:	libaio-devel
BuildRequires:	linux-libc-headers >= 2.6.12.0-5
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	sed >= 4.0
BuildRequires:	sysfsutils-devel >= 2.0.0
BuildRequires:	systemd-devel
BuildRequires:	udev-devel
%if %{with initrd}
BuildRequires:	device-mapper-initrd-devel
BuildRequires:	klibc-static
%endif
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	device-mapper >= 1.02.08
Requires:	kpartx = %{version}-%{release}
Requires:	libaio >= 0.3.106-2
Requires:	rc-scripts
Requires:	systemd-units >= 38
%if "%{pld_release}" == "th"
Requires:	udev-core >= 1:127
%endif
%if "%{pld_release}" == "ti"
Conflicts:	udev < 1:124-3
%endif
%if "%{pld_release}" == "ac"
Requires:	udev-core >= 1:079-10
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	libmultipath.so.0 libmpathpersist.so.0
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

%package -n kpartx
Summary:	Partition device manager for device-mapper devices
Summary(pl.UTF-8):	Zarządca urządzeń partycji dla urządzeń device-mappera
Group:		Base
%if "%{pld_release}" == "th"
Conflicts:	udev-core < 1:127
%endif
%if "%{pld_release}" == "ti"
Conflicts:	udev-core < 1:124-3
%endif
%if "%{pld_release}" == "ac"
Conflicts:	udev-core < 1:079-10
%endif

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
%patch2 -p1

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
	OPTFLAGS="%{rpmcflags} %{rpmcppflags} -Wall -Wunused -Wstrict-prototypes %{?debug:-DDEBUG=1}" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_sysconfdir}/multipath}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	unitdir=%{systemdunitdir}

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/multipathd
cp -p multipath.conf.defaults $RPM_BUILD_ROOT%{_sysconfdir}/multipath.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/multipathd
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/multipath/bindings

# no -devel, so remove
%{__rm} $RPM_BUILD_ROOT%{_includedir}/mpath_persist.h
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/mpath_persistent_reserve_in.3*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/mpath_persistent_reserve_out.3*
%{__rm} $RPM_BUILD_ROOT/%{_lib}/libmpathpersist.so

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

%files
%defattr(644,root,root,755)
%doc AUTHOR ChangeLog FAQ README TODO
%doc multipath.conf.{annotated,defaults,synthetic}
%attr(755,root,root) %{_sbindir}/mpathpersist
%attr(755,root,root) %{_sbindir}/multipath
%attr(755,root,root) %{_sbindir}/multipathd
%dir /%{_lib}/multipath
%attr(755,root,root) /%{_lib}/multipath/lib*.so
%attr(755,root,root) /%{_lib}/libmpathpersist.so.0
%attr(755,root,root) /%{_lib}/libmultipath.so.0
%attr(754,root,root) /etc/rc.d/init.d/multipathd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/multipathd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/multipath.conf
%dir %{_sysconfdir}/multipath
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/multipath/bindings
%{systemdunitdir}/multipathd.service
%{systemdunitdir}/multipathd.socket
%{_mandir}/man5/multipath.conf.5*
%{_mandir}/man8/mpathpersist.8*
%{_mandir}/man8/multipath.8*
%{_mandir}/man8/multipathd.8*

%files -n kpartx
%defattr(644,root,root,755)
%doc kpartx/README
%attr(755,root,root) %{_sbindir}/kpartx
%attr(755,root,root) /lib/udev/kpartx_id
/etc/udev/rules.d/kpartx.rules
%{_mandir}/man8/kpartx.8*
