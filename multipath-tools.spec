Summary:	Tools to manage multipathed devices with the device-mapper
Summary(pl):	Implementacja wielotrasowego dostêpu do zasobów przy u¿yciu device-mappera
Name:		multipath-tools
Version:	0.4.5
Release:	0.4
License:	GPL v2
Group:		Base
Source0:	http://christophe.varoqui.free.fr/multipath-tools/%{name}-%{version}.tar.bz2
# Source0-md5:	d8f87a4f08448a209d6e5bb7aa426830
URL:		http://christophe.varoqui.free.fr/
Patch0:		%{name}-optflags.patch
Patch1:		%{name}-bashism.patch
Patch2:		%{name}-udev.patch
Patch3:		%{name}-llh.patch
BuildRequires:	device-mapper-devel >= 1.01.01
BuildRequires:	linux-libc-headers >= 2.6.12.0-5
BuildRequires:	readline-devel
BuildRequires:	sysfsutils >= 1.3.0-1.1
# patch here:
# http://www.kernel.org/git/gitweb.cgi?p=linux/storage/multipath-tools/.git;a=commitdiff_plain;h=88b2dceb95cc49d379a8dfa6d563b10559dead4e;hp=1df074ffd85c05a7eec2db7b25d6219cc6f4da02
BuildRequires:	sysfsutils < 2.0.0
Conflicts:	udev < 1:070-4.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		_bindir		%{_prefix}/sbin

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
multipath-tools zawieraj± narzêdzia do zarz±dzania wielotrasowym
dostêpem do urz±dzeñ poprzez instruowanie modu³u multipath
device-mappera. Narzêdzia to:
- multipath - przeszukuje system pod k±tem urz±dzeñ z dostêpem
  wielotrasowym, ³±czy je i uaktualnia odwzorowania device-mappera
- multipathd - oczekuje na zdarzenia odwzorowañ, po których uruchamia
  multipath
- devmap-name - dostarcza do udev znacz±c± nazwê urz±dzenia dla map
  urz±dzeñ
- kpartx - odwzorowuje liniowe mapy urz±dzeñ na partycje urz±dzeñ, co
  umo¿liwia tworzenie partycji na odwzorowaniach wielotrasowych

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
mv kpartx/README README.kpartx

%build
%{__make} -j1 \
	OPTFLAGS="%{rpmcflags}" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT{%{_prefix}/bin,%{_bindir}}/multipathd
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
