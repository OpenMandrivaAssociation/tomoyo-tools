Summary: TOMOYO Linux tools
%define  date 20111025
%define  ver  2.5.0

%define tomoyo_major 1
%define tomoyo_libname %mklibname tomoyotools %{tomoyo_major}

Name: 	 tomoyo-tools
Version: %{ver}
Release: %mkrel 1
License: GPLv2
URL:	 http://tomoyo.sourceforge.jp/
Group:	 System/Kernel and hardware
BuildRequires: help2man
BuildRequires: ncurses-devel
BuildRequires: readline-devel
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source0: http://osdn.dl.sourceforge.jp/tomoyo/27220/tomoyo-tools-%{ver}-%{date}.tar.gz
Source1: README.tomoyo-tools.urpmi
Source2: tomoyo.logrotate
Source3: tomoyo.init

Conflicts: ccs-tools
Obsoletes: ccs-tools

%description
TOMOYO Linux is an extension for Linux to provide Mandatory Access Control
(MAC) functions. This package contains the tools needed to configure,
activate and manage the TOMOYO Linux MAC system and policies.

%package -n	 %{tomoyo_libname}
Summary:	Shared tomoyotools library
Group:		System/Libraries

%description -n %{tomoyo_libname}
This package provides the tomoyo shared library

%prep
%setup -q -n tomoyo-tools

%build
# install library to correct path
make USRLIBDIR=%{_libdir} CFLAGS="-Wall $RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}

make INSTALLDIR=%{buildroot} USRLIBDIR=%{_libdir} install

install -m 644 %{SOURCE1} README.install.urpmi
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/tomoyo
mkdir -p %{buildroot}%{_initrddir}
install -m 700 %{SOURCE3} %{buildroot}%{_initrddir}/tomoyo-auditd
mkdir -p %{buildroot}%{_logdir}/tomoyo

%clean
rm -rf %{buildroot}

%post
%_post_service tomoyo-auditd

%preun
%_preun_service tomoyo-auditd

%files
%defattr(-,root,root)
%{_sysconfdir}/logrotate.d/tomoyo
%attr(700,root,root) %{_initrddir}/tomoyo-auditd
%attr(700,root,root) /sbin/tomoyo-init
%{_libdir}/tomoyo/
%{_sbindir}/tomoyo*
%{_mandir}/man8/tomoyo*
%{_mandir}/man8/init_policy.8*
%{_logdir}/tomoyo/
%doc README.install.urpmi

%files -n %{tomoyo_libname}
%{_libdir}/libtomoyotools.so.*
