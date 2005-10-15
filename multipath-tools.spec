# TODO: optflags
Summary:	Tools to manage multipathed devices with the device-mapper.
Summary(pl):	Implementacja wielotrasowego dostêpu do zasobów dla Linuksa
Name:		multipath-tools
Version:	0.4.5
Release:	0.1
License:	GPL
Group:		Base
Source0:	http://christophe.varoqui.free.fr/multipath-tools/%{name}-%{version}.tar.bz2
# Source0-md5:	d8f87a4f08448a209d6e5bb7aa426830
URL:		http://christophe.varoqui.free.fr/
BuildRequires:	sysfsutils >= 1.3.0-1.1
Requires:	udev >= 1:070-4.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir /sbin

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
Implementacja wielotrasowego dostêpu do zasobów dla Linuksa.

%prep
%setup -q

%build
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_sysconfdir}/dev.d/block/multipath.dev
%{_sysconfdir}/udev/rules.d/multipath.rules
%attr(755,root,root) %{_sbindir}/devmap_name
%attr(755,root,root) %{_sbindir}/kpartx
%attr(755,root,root) %{_sbindir}/mpath_prio_alua
%attr(755,root,root) %{_sbindir}/mpath_prio_emc
%attr(755,root,root) %{_sbindir}/multipath
%attr(755,root,root) %{_sbindir}/pp_balance_units
%attr(755,root,root) %{_bindir}/multipathd
%{_mandir}/man8/devmap_name.8*
%{_mandir}/man8/kpartx.8*
%{_mandir}/man8/mpath_prio_alua.8*
%{_mandir}/man8/multipath.8*
%{_mandir}/man8/multipathd.8*

%if %{with initrd}
%exclude %{_sbindir}/initrd-*

%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/initrd-*
%endif
