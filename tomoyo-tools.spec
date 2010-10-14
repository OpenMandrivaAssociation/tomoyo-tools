Summary: TOMOYO Linux tools
%define  date 20100820
%define  ver  2.3.0

Name: 	 tomoyo-tools
Version: %{ver}
Release: %manbo_mkrel 1
License: GPLv2
URL:	 http://tomoyo.sourceforge.jp/
Group:	 System/Kernel and hardware
BuildRequires: help2man
BuildRequires: ncurses-devel
BuildRequires: readline-devel
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
#NoSource: 0

Source0: http://osdn.dl.sourceforge.jp/tomoyo/27220/tomoyo-tools-%{ver}-%{date}.tar.gz
Source1: README.tomoyo-tools.urpmi
Source2: tomoyo.logrotate
Source3: tomoyo.init
Patch0:  tomoyo-tools-dont-use-chown.patch

Conflicts: ccs-tools

%description
TOMOYO Linux is an extension for Linux to provide Mandatory Access Control
(MAC) functions. This package contains the tools needed to configure, 
activate and manage the TOMOYO Linux MAC system and policies.

%prep
%setup -q -n tomoyo-tools
%patch0 -p1

%build
# parallell build is broken / tmb 14.10.2010
make -s all

%install
rm -rf %{buildroot}
%makeinstall -s INSTALLDIR=%{buildroot}
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
/usr/lib/tomoyo/
/usr/lib/libtomoyo*
%{_sbindir}/tomoyo*
%{_mandir}/man8/tomoyo*
%{_mandir}/man8/init_policy.8*
%{_logdir}/tomoyo/
%doc README.install.urpmi
