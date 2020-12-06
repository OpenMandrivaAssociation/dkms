%define _dkmsdir %{_localstatedir}/lib/%{name}
%define _dkmsbinarydir %{_localstatedir}/lib/%{name}-binary
%global __requires_exclude /bin/awk

Summary:	Dynamic Kernel Module Support Framework
Name:		dkms
Version:	2.8.4
URL:		https://github.com/dell/dkms
Release:	1
License:	GPLv2+
Group:		System/Base
# unofficial version, git rev a62d38d49148871c6b17636f31c93f986d31c914
Source0:	https://github.com/dell/dkms/archive/v%{version}.tar.gz
Source1:	dkms-mkrpm.spec.template
Source2:	dkms.depmod.conf
Source4:	dkms.service

#Patch1:		dkms-2.0.19-norpm.patch
Patch2:		dkms-2.6.1-mdkize.patch
Patch7:		dkms-2.6.1-procconfig.patch
Patch8:		dkms-2.6.1-mdkrpm-split-ver-rel.patch
Patch10:	dkms-2.6.1-binary_only.patch
Patch11:	dkms-2.6.1-min-max-kernel.patch
Patch17:	dkms-2.6.1-autoalias.patch
Patch18:	dkms-2.6.1-mkrpm_status.patch
Patch22:	dkms-2.6.1-symvers.patch
Patch24:	dkms-2.6.1-generic-preparation-for-2.6.39-and-higher.patch
Patch25:	dkms-2.6.1-suggest-devel-not-source.patch
Patch35:	dkms-2.6.1-dont_fail_if_module_source_removed.patch
Patch37:	dkms-2.6.1-parallel_fix.patch
Patch38:	dkms-2.6.1-display_plymouth_message.patch

BuildRequires:	systemd-macros
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
Requires(pre,post):	systemd
%rename		%{name}-minimal

%description
This package contains the framework for the Dynamic
Kernel Module Support (DKMS) method for installing
module RPMS as originally developed by the Dell
Computer Corporation.

This package is intended for building binary kernel
modules with dkms source packages installed

%prep
%autosetup -p1

%build

%install
%make_install INITD=%{buildroot}%{_initrddir} \
		 SBIN=%{buildroot}%{_sbindir} \
		 VAR=%{buildroot}%{_localstatedir}/lib/%{name} \
		 MAN=%{buildroot}%{_mandir}/man8 \
		 ETC=%{buildroot}%{_sysconfdir}/%{name} \
		 BASHDIR=%{buildroot}%{_sysconfdir}/bash_completion.d \
		 LIBDIR=%{buildroot}%{_prefix}/lib/%{name}

install -m644 -p %{SOURCE1} -D %{buildroot}%{_sysconfdir}/%{name}/template-dkms-mkrpm.spec
install -m755 -p dkms_mkkerneldoth -D %{buildroot}%{_sbindir}/dkms_mkkerneldoth
rm %{buildroot}%{_prefix}/lib/%{name}/dkms_autoinstaller
mkdir -p %{buildroot}%{_dkmsbinarydir}
install -m644 -p %{SOURCE2} -D %{buildroot}%{_sysconfdir}/depmod.d/%{name}.conf
install -m644 -p %{SOURCE4} -D %{buildroot}%{_unitdir}/%{name}.service

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-dkms.preset << EOF
enable dkms.service
EOF

%pre
printf '%s\n' "Preinstalling packages needed for building kernel modules. Please wait... "

%post
/bin/systemctl --quiet restart dkms.service
/bin/systemctl --quiet try-restart loadmodules.service
/bin/systemctl --quiet try-restart systemd-modules-load.service

%files
%doc sample.spec sample.conf AUTHORS template-dkms-mkrpm.spec
%{_presetdir}/86-dkms.preset
%{_unitdir}/%{name}.service
%{_sbindir}/dkms
%{_dkmsdir}
%dir %{_dkmsbinarydir}
%{_sbindir}/dkms_mkkerneldoth
%{_mandir}/man8/dkms.8*
%config(noreplace) %{_sysconfdir}/dkms
# these dirs are for plugins - owned by other packages
%dir %{_prefix}/lib/%{name}
%{_prefix}/lib/%{name}/common.postinst
%{_sysconfdir}/kernel/postinst.d/%{name}
%{_sysconfdir}/kernel/prerm.d/%{name}
%{_sysconfdir}/bash_completion.d/%{name}
%{_sysconfdir}/depmod.d/%{name}.conf
