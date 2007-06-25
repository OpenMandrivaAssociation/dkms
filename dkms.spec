Summary: 	Dynamic Kernel Module Support Framework
Name: 		dkms
Version: 	2.0.17
URL:		http://linux.dell.com/dkms
Release: 	%mkrel 4
License: 	GPL
Group:  	System/Base
BuildArch: 	noarch
Requires:	kernel-source
Requires:	%{name}-minimal = %{version}-%{release}
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires:	patch
Source:		http://linux.dell.com/dkms/%{name}-%{version}.tar.bz2
Source1:	template-dkms-mkrpm.spec
Patch1:		dkms-2.0.17-norpm.patch
Patch2:		dkms-2.0.13-mdkize.patch
Patch4:		dkms-2.0.2-compressed-module.patch
Patch7:		dkms-2.0.9-procconfig.patch
Patch8:		dkms-2.0.17-split-version-release.patch
Patch9:		dkms-2.0.17-bash-completion-update.patch
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
%patch4 -p1 -b .compressed-module
%patch7 -p1 -b .procconfig
%patch8 -p1 -b .mkdrpm-split-ver-rel
%patch9 -p1 -b .bash-completion-update

sed -i -e 's,/var/%{name},%{_dkmsdir},g;s,init.d/dkms_autoinstaller,init.d/%{name},g' %{name}.8 dkms dkms_autoinstaller dkms_framework.conf

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_mandir}/man8
%makeinstall_std INITD=%{buildroot}%{_initrddir}
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


