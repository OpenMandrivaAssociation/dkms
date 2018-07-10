%define __noautoreq '.*/bin/awk|.*/bin/gawk'

%define _dkmsdir %{_localstatedir}/lib/%{name}
%define _dkmsbinarydir %{_localstatedir}/lib/%{name}-binary

Summary:	Dynamic Kernel Module Support Framework
Name:		dkms
Version:	2.6.1
Release:	2
License:	GPLv2+
Group:		System/Base
URL:		http://linux.dell.com/dkms
Source0:	https://github.com/dell/dkms/archive/%{name}-%{version}.tar.gz
Source1:	dkms-mkrpm.spec.template
Source2:	dkms.depmod.conf
Source3:	autoload.awk
BuildRequires:	systemd
BuildRequires:	rpm-helper
BuildArch:	noarch
Requires:	kernel-devel
Suggests:	kernel-devel-latest
# (tpg) these are needed before dkms.service starts
Requires(pre):	patch
Requires(pre):	coreutils
Requires(pre):	cpio
Requires(pre):	sed
Requires(pre):	gawk
Requires(pre):	grep
Requires(pre):	findutils
Requires(pre):	lsb-release
Requires(pre):	gcc >= 7.2.1_2017.11-3
Requires(pre):	gcc-cpp
Requires(pre):	make
Requires(pre):	which
Requires(pre):	file
Requires(pre):	kmod
Requires(pre):	pkgconfig(libelf) >= 0.170
Requires(pre):	rpm-helper
Requires(post,postun): systemd
%rename		%{name}-minimal

%description
This package contains the framework for the Dynamic
Kernel Module Support (DKMS) method for installing
module RPMS as originally developed by the Dell
Computer Corporation.

This package is intended for building binary kernel
modules with dkms source packages installed

%prep
%setup -q
%autopatch -p1

%install
%makeinstall_std INITD=%{buildroot}%{_initrddir} \
		 SBIN=%{buildroot}%{_sbindir} \
		 VAR=%{buildroot}%{_localstatedir}/lib/%{name} \
		 MAN=%{buildroot}%{_mandir}/man8 \
		 ETC=%{buildroot}%{_sysconfdir}/%{name} \
		 BASHDIR=%{buildroot}%{_sysconfdir}/bash_completion.d \
		 LIBDIR=%{buildroot}%{_prefix}/lib/%{name}

install -m644 -p %{SOURCE1} -D %{buildroot}%{_sysconfdir}/%{name}/template-dkms-mkrpm.spec
install -m755 -p dkms_mkkerneldoth -D %{buildroot}%{_sbindir}/dkms_mkkerneldoth
rm %{buildroot}%{_prefix}/lib/%{name}/dkms_autoinstaller
install -m755 -p %{SOURCE3} %{buildroot}%{_sbindir}/dkms_autoload
mkdir -p %{buildroot}%{_dkmsbinarydir}
install -m644 -p %{SOURCE2} -D %{buildroot}%{_sysconfdir}/depmod.d/%{name}.conf

install -m644 -p dkms.service -D %{buildroot}%{_systemunitdir}/dkms.service
install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-dkms.preset << EOF
enable dkms.service
EOF

%triggerpostun -- dkms < 2.0.19-11
rm -f /etc/rc.d/*/{K,S}??dkms

%pre
printf '%s\n' "Preinstalling packages needed for building kernel modules. Please wait... "

%post
/bin/systemctl --quiet restart dkms.service
/bin/systemctl --quiet try-restart fedora-loadmodules.service

%files
%doc sample.spec sample.conf AUTHORS template-dkms-mkrpm.spec
%{_presetdir}/86-dkms.preset
%{_systemunitdir}/%{name}.service
%{_sbindir}/dkms
%{_dkmsdir}
%dir %{_dkmsbinarydir}
%{_sbindir}/dkms_mkkerneldoth
%{_sbindir}/dkms_autoload
%{_mandir}/man8/dkms.8*
%config(noreplace) %{_sysconfdir}/dkms
# these dirs are for plugins - owned by other packages
%dir %{_prefix}/lib/%{name}
%{_prefix}/lib/%{name}/common.postinst
%{_sysconfdir}/kernel/postinst.d/%{name}
%{_sysconfdir}/kernel/prerm.d/%{name}
%{_sysconfdir}/bash_completion.d/%{name}
%{_sysconfdir}/depmod.d/%{name}.conf
