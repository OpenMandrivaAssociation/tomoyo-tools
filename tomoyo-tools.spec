%define date 20130406
%define major 2
%define libname %mklibname tomoyotools %{major}

Summary:	TOMOYO Linux tools
Name:		tomoyo-tools
Version:	2.4.0
Release:	7
Epoch:		2
License:	GPLv2
URL:		http://tomoyo.sourceforge.jp/
Group:		System/Kernel and hardware
Source0:	http://osdn.dl.sourceforge.jp/tomoyo/27220/tomoyo-tools-%{version}-%{date}.tar.gz
Source1:	README.tomoyo-tools.urpmi
Source2:	tomoyo.logrotate
Source3:	tomoyo-auditd.service
BuildRequires:	help2man
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel

%rename	ccs-tools

%description
TOMOYO Linux is an extension for Linux to provide Mandatory Access Control
(MAC) functions. This package contains the tools needed to configure,
activate and manage the TOMOYO Linux MAC system and policies.

%package -n	 %{libname}
Summary:	Shared tomoyotools library
Group:		System/Libraries

%description -n %{libname}
This package provides the tomoyo shared library.

%prep
%setup -q -n tomoyo-tools

%build
# Fix libdir
sed -i \
	-e "s:gcc:%{__cc}:" \
	-e "s:/usr/lib:%{_libdir}:g" \
	-e "s/\(CFLAGS.*:=\).*/\1 %{optflags}/" \
	Include.make

%make

%install
make INSTALLDIR=%{buildroot} install

install -m 644 %{SOURCE1} README.install.urpmi
install -m 644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/tomoyo
install -m 644 -D %{SOURCE3} %{buildroot}%{_unitdir}/tomoyo-auditd.service
install -m 700 -d %{buildroot}%{_logdir}/tomoyo

%post
%_add_service_helper --no-sysv %{name} $1 tomoyo-auditd.service

%preun
%_del_service_helper --no-sysv %{name} $1 tomoyo-auditd.service

%files
%{_sysconfdir}/logrotate.d/tomoyo
%attr(700,root,root) /sbin/tomoyo-init
%{_libdir}/tomoyo/
%{_sbindir}/tomoyo*
%{_mandir}/man8/tomoyo*
%{_mandir}/man8/init_policy.8*
%{_logdir}/tomoyo/
%{_unitdir}/tomoyo-auditd.service
%doc README.install.urpmi

%files -n %{libname}
%{_libdir}/libtomoyotools.so.%{major}*
