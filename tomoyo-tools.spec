Summary: TOMOYO Linux tools
%define  date 20100225
%define  ver  2.2.0

Name: 	 tomoyo-tools
Version: %{ver}
Release: %manbo_mkrel 1
License: GPLv2
URL:	 http://tomoyo.sourceforge.jp/
Group:	 System/Kernel and hardware
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
%make -s all

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
%attr(700,root,root) /sbin/tomoyo-init
/usr/lib/tomoyo/
%{_sbindir}/tomoyo-checkpolicy
%{_sbindir}/tomoyo-domainmatch
%{_sbindir}/tomoyo-editpolicy
%{_sbindir}/tomoyo-findtemp
%{_sbindir}/tomoyo-ld-watch
%{_sbindir}/tomoyo-loadpolicy
%{_sbindir}/tomoyo-pathmatch
%{_sbindir}/tomoyo-patternize
%{_sbindir}/tomoyo-pstree
%{_sbindir}/tomoyo-savepolicy
%{_sbindir}/tomoyo-setlevel
%{_sbindir}/tomoyo-setprofile
%{_sbindir}/tomoyo-sortpolicy
%{_mandir}/man8/tomoyo-checkpolicy.8*
%{_mandir}/man8/tomoyo-domainmatch.8*
%{_mandir}/man8/tomoyo-editpolicy.8*
%{_mandir}/man8/tomoyo-editpolicy-agent.8*
%{_mandir}/man8/tomoyo-findtemp.8*
%{_mandir}/man8/tomoyo-init.8*
%{_mandir}/man8/tomoyo-ld-watch.8*
%{_mandir}/man8/tomoyo-loadpolicy.8*
%{_mandir}/man8/tomoyo-pathmatch.8*
%{_mandir}/man8/tomoyo-patternize.8*
%{_mandir}/man8/tomoyo-pstree.8*
%{_mandir}/man8/tomoyo-savepolicy.8*
%{_mandir}/man8/tomoyo-setlevel.8*
%{_mandir}/man8/tomoyo-setprofile.8*
%{_mandir}/man8/tomoyo-sortpolicy.8*
%{_mandir}/man8/tomoyo_init_policy.8*
%{_logdir}/tomoyo/
%doc README.install.urpmi
