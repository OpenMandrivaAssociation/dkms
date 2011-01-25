Summary: 	Dynamic Kernel Module Support Framework
Name: 		dkms
Version: 	2.0.19
URL:		http://linux.dell.com/dkms
Release: 	%mkrel 22
License: 	GPL
Group:  	System/Base
BuildArch: 	noarch
Requires:	kernel-devel
Suggests:	kernel-devel-latest
Requires:	%{name}-minimal = %{version}-%{release}
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires:	patch
Requires:	sed
Source:		http://linux.dell.com/dkms/%{name}-%{version}.tar.gz
Source1:	template-dkms-mkrpm.spec
Source2:	dkms.depmod.conf
Source3:	autoload.awk
Patch1:		dkms-2.0.19-norpm.patch
Patch2:		dkms-2.0.17.5-mdkize.patch
Patch3:		dkms-fix-kernel-make-prepare.patch
Patch4:		dkms-2.0.17.6-compressed-module.patch
Patch5:		dkms-2.0.19-weak_module_name.patch
Patch7:		dkms-2.0.19-procconfig.patch
Patch8:		dkms-2.0.19-mdkrpm-split-ver-rel.patch
Patch9:		dkms-2.0.19-bash-completion-update.patch
Patch10:	dkms-2.0.19-binary_only.patch
Patch11:	dkms-2.0.17.5-min-max-kernel.patch
Patch12:	dkms-2.0.17.6-test-dkms.conf-existence.patch
Patch13:	dkms-2.0.17.6-status_default.patch
Patch14:	dkms-2.0.17.6-stdout.patch
Patch15:	dkms-2.0.19-no_custom_rpm_provides.patch
Patch16:	dkms-2.0.19-binary.patch
Patch17:	dkms-2.0.19-autoalias.patch
Patch18:	dkms-2.0.19-mkrpm_status.patch
Patch19:	dkms-2.0.19-skip-unused-check.patch
Patch20:	dkms-2.0.19-uninstall-speedup.patch
Patch21:	dkms-2.0.19-init-mdv-interactive.patch
Patch22:	dkms-symvers.patch
Patch23:	dkms-2.0.19-autoload_instead_of_udevadm.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root/

%define _dkmsdir %{_localstatedir}/lib/%{name}
%define _dkmsbinarydir %{_localstatedir}/lib/%{name}-binary

%description
This package contains the framework for the Dynamic
Kernel Module Support (DKMS) method for installing
module RPMS as originally developed by the Dell
Computer Corporation.

This package is intended for building binary kernel
modules with dkms source packages installed

%package minimal
Summary: 	Dynamic Kernel Module Support Framework - minimal package
License: 	GPL
Group: 		System/Base
Requires:	lsb-release
Requires(preun):	rpm-helper
Requires(post):	rpm-helper

%description minimal
This package contains the framework for the Dynamic
Kernel Module Support (DKMS) method for installing
module RPMS as originally developed by the Dell
Computer Corporation.

This package is intended for installing binary module RPMS
as created by dkms.

%prep
%setup -q
%patch1 -p1 -b .norpm
%patch2 -p1 -b .mdkize
%patch3 -p1 -b .fix-kernel-make-prepare
%patch4 -p1 -b .compressed-module
%patch5 -p1 -b .weak_module_name
%patch7 -p1 -b .procconfig
%patch8 -p1 -b .mdkrpm-split-ver-rel
%patch9 -p1 -b .bash-completion-update
%patch10 -p1 -b .binary_only
%patch11 -p1 -b .min-max-kernel
%patch12 -p1 -b .test-dkmsconf
%patch13 -p1 -b .status_default
%patch14 -p1 -b .stdout
%patch15 -p1 -b .no_custom_rpm_provides
%patch16 -p1 -b .binary
%patch17 -p0 -b .autoalias
%patch18 -p1 -b .mkrpm
%patch19 -p1 -b .versionsanity
%patch20 -p1 -b .uninst-speedup
%patch21 -p1 -b .mdv-interactive
%patch22 -p1 -b .symvers
%patch23 -p1 -b .autoload_instead_of_udevadm

sed -i -e 's,/var/%{name},%{_dkmsdir},g;s,init.d/dkms_autoinstaller,init.d/%{name},g' \
  dkms_autoinstaller \
  dkms_framework.conf \
  kernel_*.d_dkms \
  %{name}.8 \
  dkms

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_mandir}/man8
%makeinstall_std INITD=%{buildroot}%{_initrddir}
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/
install -m 755 dkms_mkkerneldoth %{buildroot}/%{_sbindir}/dkms_mkkerneldoth
install -m 755 %{SOURCE3} %{buildroot}/%{_sbindir}/dkms_autoload
mv %{buildroot}%{_initrddir}/dkms_autoinstaller %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_dkmsbinarydir}
mkdir -p %{buildroot}%{_sysconfdir}/depmod.d
install -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/depmod.d/%{name}.conf

%triggerpostun -- dkms < 2.0.19-11
rm -f /etc/rc.d/*/{K,S}??dkms

%clean 
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %attr (-,root,root) sample.spec sample.conf AUTHORS COPYING template-dkms-mkrpm.spec 
%{_sbindir}/dkms_autoinstaller

%files minimal
%defattr(-,root,root)
%{_sbindir}/dkms
%{_dkmsdir}
%dir %{_dkmsbinarydir}
%{_sbindir}/dkms_mkkerneldoth
%{_sbindir}/dkms_autoload
%{_mandir}/man8/dkms.8*
%config(noreplace) %{_sysconfdir}/dkms
# these dirs are for plugins - owned by other packages
%{_sysconfdir}/kernel/postinst.d/%{name}
%{_sysconfdir}/kernel/prerm.d/%{name}
%{_sysconfdir}/bash_completion.d/%{name}
%{_sysconfdir}/depmod.d/%{name}.conf
