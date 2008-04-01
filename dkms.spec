Summary: 	Dynamic Kernel Module Support Framework
Name: 		dkms
Version: 	2.0.17.6
URL:		http://linux.dell.com/dkms
Release: 	%mkrel 2
License: 	GPL
Group:  	System/Base
BuildArch: 	noarch
Requires:	kernel-devel
Suggests:	kernel-devel-latest
Requires:	%{name}-minimal = %{version}-%{release}
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires:	patch
Source:		http://linux.dell.com/dkms/%{name}-%{version}.tar.gz
Source1:	template-dkms-mkrpm.spec
Patch1:		dkms-2.0.17-norpm.patch
Patch2:		dkms-2.0.17.5-mdkize.patch
Patch3:		dkms-fix-kernel-make-prepare.patch
Patch4:		dkms-2.0.17.6-compressed-module.patch
Patch7:		dkms-2.0.9-procconfig.patch
Patch8:		dkms-2.0.17.5-split-version-release.patch
Patch9:		dkms-2.0.17-bash-completion-update.patch
Patch10:	dkms-2.0.17-binary_only.patch
Patch11:	dkms-2.0.17.5-min-max-kernel.patch
Patch12:	dkms-2.0.17.6-test-dkms.conf-existence.patch
Patch13:	dkms-2.0.17.6-status_default.patch
Patch14:	dkms-2.0.17.6-stdout.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root/

%define _dkmsdir %{_localstatedir}/%{name}

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
%patch7 -p1 -b .procconfig
%patch8 -p1 -b .mdkrpm-split-ver-rel
%patch9 -p1 -b .bash-completion-update
%patch10 -p1 -b .binary_only
%patch11 -p1 -b .min-max-kernel
%patch12 -p1 -b .test-dkmsconf
%patch13 -p1 -b .status_default
%patch14 -p1 -b .stdout

sed -i -e 's,/var/%{name},%{_dkmsdir},g;s,init.d/dkms_autoinstaller,init.d/%{name},g' \
  dkms_autoinstaller \
  dkms_framework.conf \
  %{name}.8 \
  dkms

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_mandir}/man8
%makeinstall_std INITD=%{buildroot}%{_initrddir}
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/
install -m 755 dkms_mkkerneldoth %{buildroot}/%{_sbindir}/dkms_mkkerneldoth
mv %{buildroot}%{_initrddir}/dkms_autoinstaller %{buildroot}%{_initrddir}/dkms

%clean 
rm -rf %{buildroot}

%post minimal
%_post_service %{name}

%preun minimal
%_preun_service %{name}

%files
%defattr(-,root,root)
%doc %attr (-,root,root) sample.spec sample.conf AUTHORS COPYING template-dkms-mkrpm.spec 

%files minimal
%defattr(-,root,root)
%{_sbindir}/dkms
%{_dkmsdir}
%{_initrddir}/%{name}
%{_sbindir}/dkms_mkkerneldoth
%{_mandir}/man8/dkms.8*
%config(noreplace) %{_sysconfdir}/dkms
%{_sysconfdir}/bash_completion.d/%{name}
