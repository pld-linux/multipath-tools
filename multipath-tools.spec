Summary:	Tools to manage multipathed devices with the device-mapper
Summary(pl):	Implementacja wielotrasowego dost�pu do zasob�w przy u�yciu device-mappera
Name:		multipath-tools
Version:	0.4.7
Release:	0.1
License:	GPL v2
Group:		Base
Source0:	http://christophe.varoqui.free.fr/multipath-tools/%{name}-%{version}.tar.bz2
# Source0-md5:	0a7574f0dd85f2b50f6aff91d83633ad
URL:		http://christophe.varoqui.free.fr/
Patch0:		%{name}-llh.patch
Patch1:		%{name}-selinux.patch
Patch2:		%{name}-optflags.patch
# was not used - is OPTIONS+="last_rule" stille needed?
#Patch2:		%{name}-udev.patch
BuildRequires:	device-mapper-devel >= 1.01.01
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

%description -l pl
multipath-tools zawieraj� narz�dzia do zarz�dzania wielotrasowym
dost�pem do urz�dze� poprzez instruowanie modu�u multipath
device-mappera. Narz�dzia to:
- multipath - przeszukuje system pod k�tem urz�dze� z dost�pem
  wielotrasowym, ��czy je i uaktualnia odwzorowania device-mappera
- multipathd - oczekuje na zdarzenia odwzorowa�, po kt�rych uruchamia
  multipath
- devmap-name - dostarcza do udev znacz�c� nazw� urz�dzenia dla map
  urz�dze�
- kpartx - odwzorowuje liniowe mapy urz�dze� na partycje urz�dze�, co
  umo�liwia tworzenie partycji na odwzorowaniach wielotrasowych

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
mv kpartx/README README.kpartx

%build
%{__make} -j1 \
	OPTFLAGS="%{rpmcflags} -Wall -Wunused -Wstrict-prototypes" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/{,40-}multipath.rules
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/dev.d/block/multipath.dev

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHOR ChangeLog FAQ README* TODO
%{_sysconfdir}/udev/rules.d/*.rules
%attr(755,root,root) %{_sbindir}/devmap_name
%attr(755,root,root) %{_sbindir}/kpartx
%attr(755,root,root) %{_sbindir}/mpath_prio_alua
%attr(755,root,root) %{_sbindir}/mpath_prio_balance_units
%attr(755,root,root) %{_sbindir}/mpath_prio_emc
%attr(755,root,root) %{_sbindir}/mpath_prio_netapp
%attr(755,root,root) %{_sbindir}/mpath_prio_random
%attr(755,root,root) %{_sbindir}/mpath_prio_tpc
%attr(755,root,root) %{_sbindir}/multipath
%attr(755,root,root) %{_sbindir}/multipathd
%{_mandir}/man8/devmap_name.8*
%{_mandir}/man8/kpartx.8*
%{_mandir}/man8/mpath_prio_alua.8*
%{_mandir}/man8/multipath.8*
%{_mandir}/man8/multipathd.8*
