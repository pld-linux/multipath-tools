Summary:	Tools to manage multipathed devices with the device-mapper
Summary(pl.UTF-8):	Implementacja wielotrasowego dostępu do zasobów przy użyciu device-mappera
Name:		multipath-tools
Version:	0.4.8
Release:	0.1
License:	GPL v2
Group:		Base
Source0:	http://christophe.varoqui.free.fr/multipath-tools/%{name}-%{version}.tar.bz2
# Source0-md5:	3563b863b408d07c46929b6e8c2c248c
URL:		http://christophe.varoqui.free.fr/
Patch0:		%{name}-llh.patch
# was not used - is OPTIONS+="last_rule" stille needed?
#Patch1:		%{name}-udev.patch
BuildRequires:	device-mapper-devel >= 1.02.07
BuildRequires:	libaio-devel
BuildRequires:	linux-libc-headers >= 2.6.12.0-5
BuildRequires:	readline-devel
BuildRequires:	sysfsutils-devel >= 2.0.0
Conflicts:	udev < 1:070-4.1
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
- kpartx: maps linear devmaps upon device partitions, which makes
  multipath maps partionable

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
- kpartx - odwzorowuje liniowe mapy urządzeń na partycje urządzeń, co
  umożliwia tworzenie partycji na odwzorowaniach wielotrasowych

%prep
%setup -q
%patch0 -p1
mv kpartx/README README.kpartx

%build
%{__make} -j1 \
	OPTFLAGS="%{rpmcflags} -Wall -Wunused -Wstrict-prototypes" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D multipath.conf.annotated $RPM_BUILD_ROOT%{_sysconfdir}/multipath.conf
install -d $RPM_BUILD_ROOT/var/lib/multipath
mv $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/{,40-}multipath.rules
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/dev.d/block/multipath.dev

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHOR ChangeLog FAQ README* TODO
%attr(755,root,root) %{_sbindir}/devmap_name
%attr(755,root,root) %{_sbindir}/kpartx
%attr(755,root,root) %{_sbindir}/mpath_prio_alua
%attr(755,root,root) %{_sbindir}/mpath_prio_balance_units
%attr(755,root,root) %{_sbindir}/mpath_prio_emc
%attr(755,root,root) %{_sbindir}/mpath_prio_hds_modular
%attr(755,root,root) %{_sbindir}/mpath_prio_hp_sw
%attr(755,root,root) %{_sbindir}/mpath_prio_netapp
%attr(755,root,root) %{_sbindir}/mpath_prio_random
%attr(755,root,root) %{_sbindir}/mpath_prio_rdac
%attr(755,root,root) %{_sbindir}/multipath
%attr(755,root,root) %{_sbindir}/multipathd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/multipath.conf
%{_sysconfdir}/udev/rules.d/40-multipath.rules
%{_sysconfdir}/udev/rules.d/kpartx.rules
%attr(755,root,root) /lib/udev/kpartx_id
%dir /var/lib/multipath
%{_mandir}/man5/multipath.conf.5*
%{_mandir}/man8/devmap_name.8*
%{_mandir}/man8/kpartx.8*
%{_mandir}/man8/mpath_prio_alua.8*
%{_mandir}/man8/multipath.8*
%{_mandir}/man8/multipathd.8*
