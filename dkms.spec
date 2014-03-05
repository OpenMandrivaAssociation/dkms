%define __noautoreq '.*/bin/awk|.*/bin/gawk'

Summary:	Dynamic Kernel Module Support Framework
Name:		dkms
Version:	2.2.0.3.1
URL:		http://linux.dell.com/dkms
Release:	1
License:	GPLv2+
Group:		System/Base
BuildArch:	noarch
Suggests:	kernel-devel
Requires:	%{name}-minimal = %{version}-%{release}
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires:	patch
Requires:	sed
Requires:	gawk
# unofficial version, from latest git 
Source0:	http://linux.dell.com/dkms/permalink/%{name}-%{version}.tar.xz
Source1:	dkms-mkrpm.spec.template
Source2:	dkms.depmod.conf
Source3:	autoload.awk
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


%define _dkmsdir %{_localstatedir}/lib/%{name}
%define _dkmsbinarydir %{_localstatedir}/lib/%{name}-binary

%description
This package contains the framework for the Dynamic
Kernel Module Support (DKMS) method for installing
module RPMS as originally developed by the Dell
Computer Corporation.

This package is intended for building binary kernel
modules with dkms source packages installed

%package	minimal
Summary:	Dynamic Kernel Module Support Framework - minimal package
Group:		System/Base
Requires:	gawk
Requires:	lsb-release
Requires(preun):rpm-helper
Requires(post):	rpm-helper

%description	minimal
This package contains the framework for the Dynamic
Kernel Module Support (DKMS) method for installing
module RPMS as originally developed by the Dell
Computer Corporation.

This package is intended for installing binary module RPMS
as created by dkms.

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

sed -i -e 's,/var/%{name},%{_dkmsdir},g;s,init.d/dkms_autoinstaller,init.d/%{name},g' \
  dkms_autoinstaller \
  dkms_framework.conf \
  kernel_*.d_dkms \
  %{name}.8 \
  dkms

%install
%makeinstall_std INITD=%{buildroot}%{_initrddir} \
		 SBIN=%{buildroot}%{_sbindir} \
		 VAR=%{buildroot}%{_localstatedir}/lib/%{name} \
		 MAN=%{buildroot}%{_mandir}/man8 \
		 ETC=%{buildroot}%{_sysconfdir}/%{name} \
		 BASHDIR=%{buildroot}%{_sysconfdir}/bash_completion.d \
		 LIBDIR=%{buildroot}%{_prefix}/lib/%{name}

install -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/%{name}/template-dkms-mkrpm.spec
install -m755 dkms_mkkerneldoth -D %{buildroot}%{_sbindir}/dkms_mkkerneldoth
mv %{buildroot}%{_prefix}/lib/%{name}/dkms_autoinstaller %{buildroot}%{_sbindir}
install -m755 %{SOURCE3} %{buildroot}%{_sbindir}/dkms_autoload
mkdir -p %{buildroot}%{_dkmsbinarydir}
install -m644 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/depmod.d/%{name}.conf

%triggerpostun -- dkms < 2.0.19-11
rm -f /etc/rc.d/*/{K,S}??dkms

%files
%doc sample.spec sample.conf AUTHORS template-dkms-mkrpm.spec 
%{_sbindir}/dkms_autoinstaller

%files minimal
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
