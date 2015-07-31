%define __noautoreq '.*/bin/awk|.*/bin/gawk'

Summary:	Dynamic Kernel Module Support Framework
Name:		dkms
Version:	2.2.0.3.1
URL:		http://linux.dell.com/dkms
%define	gitdate	20130827
Release:	3.%{gitdate}.11
License:	GPLv2+
Group:		System/Base
BuildArch:	noarch
Suggests:	kernel-devel
Suggests:	kernel-nrjQL-desktop-devel-latest
# (tpg) these are needed before dkms.service starts
Requires(pre):	patch
Requires(pre):	coreutils
Requires(pre):	cpio
Requires(pre):	sed
Requires(pre):	gawk
Requires(pre):	grep
Requires(pre):	findutils
Requires(pre):	lsb-release
Requires(pre):	gcc
Requires(pre):	gcc-cpp
Requires(pre):	make
Requires(pre):	which
Requires(pre):	file
Requires(pre):	kmod
Requires(post,postun):	systemd-units
%rename		%{name}-minimal
# unofficial version, git rev a62d38d49148871c6b17636f31c93f986d31c914
Source0:	http://linux.dell.com/dkms/permalink/%{name}-%{version}.tar.xz
Source1:	dkms-mkrpm.spec.template
Source2:	dkms.depmod.conf
Source3:	autoload.awk
Source4:	dkms.service

Patch1:		dkms-2.0.19-norpm.patch
Patch2:		dkms-2.2.0.3-mdkize.patch
Patch4:		dkms-2.2.0.3-compressed-module.patch
Patch7:		dkms-2.2.0.3-procconfig.patch
Patch8:		dkms-2.2.0.3-mdkrpm-split-ver-rel.patch
Patch10:	dkms-2.2.0.3-binary_only.patch
Patch11:	dkms-2.2.0.3-min-max-kernel.patch
Patch17:	dkms-2.2.0.3-autoalias.patch
Patch18:	dkms-2.2.0.3-mkrpm_status.patch
Patch21:	dkms-2.2.0.3-init-mdv-interactive.patch
Patch22:	dkms-2.2.0.3-symvers.patch
Patch24:	dkms-2.2.0.3-generic-preparation-for-2.6.39-and-higher.patch
Patch25:	dkms-2.2.0.3-suggest-devel-not-source.patch
Patch26:	dkms-2.2.0.3.1-xz-support.patch
Patch27:	dkms-2.2.0.3-parallel-build.patch
Patch28:	dkms-man.patch
Patch29:	dkms-cleanup-after-removal.patch
Patch30:	dkms-do-not-fail-on-modules-dir.patch
Patch31:	dkms-use-STRIP-0-as-the-default-for-the-STRIP-array.patch
Patch32:	dkms-2.2.0.3.1-add-dependency-logic-for-automatic-builds.patch
Patch33:	dkms-fix-zfs-autoinstall-failures-for-kernel-upgrades.patch
Patch34:	dkms-reset-build-dependencies.patch
Patch35:	dkms-2.2.0.3-dont_fail_if_module_source_removed.patch
Patch36:	dkms-2.2.0.3-fix_obsolete_modules_check.patch

%define _dkmsdir %{_localstatedir}/lib/%{name}
%define _dkmsbinarydir %{_localstatedir}/lib/%{name}-binary

%description
This package contains the framework for the Dynamic
Kernel Module Support (DKMS) method for installing
module RPMS as originally developed by the Dell
Computer Corporation.

This package is intended for building binary kernel
modules with dkms source packages installed

%prep
%setup -q
%patch2 -p1 -b .mdkize~
%patch4 -p1 -b .compressed-module~
%patch7 -p1 -b .procconfig~
%patch8 -p1 -b .mdkrpm-split-ver-rel~
%patch10 -p1 -b .binary_only~
%patch11 -p1 -b .min-max-kernel~
%patch17 -p1 -b .autoalias~
%patch18 -p1 -b .mkrpm~
%patch21 -p1 -b .mdv-interactive~
%patch22 -p1 -b .symvers~
%patch24 -p1 -b .generic-prepare~
%patch25 -p1 -b .suggests-devel~
%patch26 -p1 -b .xz_support~
%patch27 -p1 -b .parallel~
%patch28 -p1 -b .man~
%patch29 -p1 -b .cleanup~
%patch30 -p1 -b .nofail~
%patch31 -p1 -b .strip0~
%patch32 -p1 -b .autodeplogic~
%patch33 -p1 -b .zfs~
%patch34 -p1 -b .resetdeps~
%patch35 -p1 -b .dontfail~
%patch36 -p1 -b .obs_mod_check~

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
install -m644 -p %{SOURCE4} -D %{buildroot}%{_unitdir}/%{name}.service

%if "%{disttag}" == "omv"
sed -i -e 's/moondrake/OpenMandriva/gI' %{buildroot}%{_sysconfdir}/%{name}/template-dkms-mkrpm.spec
%endif

%triggerpostun -- dkms < 2.0.19-11
rm -f /etc/rc.d/*/{K,S}??dkms

%pre
echo "Preinstalling packages"

%post
/bin/systemctl --quiet restart dkms.service
/bin/systemctl --quiet try-restart fedora-loadmodules.service

%files
%doc sample.spec sample.conf AUTHORS template-dkms-mkrpm.spec 
%{_unitdir}/%{name}.service
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
