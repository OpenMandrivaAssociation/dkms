Summary: 	Dynamic Kernel Module Support Framework
Name: 		dkms
Version: 	2.0.16
URL:		http://linux.dell.com/dkms
Release: 	%mkrel 3
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
Source2:	dkms.bash-completion
Patch1:		dkms-2.0.5.9-norpm.patch
Patch2:		dkms-2.0.13-mdkize.patch
Patch3:		dkms-2.0.9-rpmbuild.patch
Patch4:		dkms-2.0.2-compressed-module.patch
Patch5:		dkms-2.0.9-pinit.patch
Patch6:		dkms-2.0.8-pass-arch.patch
Patch7:		dkms-2.0.9-procconfig.patch
Patch8:		dkms-2.0.10-split-version-release.patch
Patch9:		dkms-fix-kernel-make-prepare.patch
Patch10:	dkms-2.0.16-alias_number.patch
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
%patch3 -p1 -b .rpmbuild
%patch4 -p1 -b .compressed-module
%patch5 -p1 -b .pinit
%patch6 -p1 -b .pass-arch
%patch7 -p1 -b .procconfig
%patch8 -p3 -b .mkdrpm-split-ver-rel
%patch9 -p1 -b .fix-kernel-make-prepare
%patch10 -p1 -b .alias_number

#gunzip %{name}.8.gz
sed -i -e 's,/var/%{name},%{_dkmsdir},g;s,init.d/dkms_autoinstaller,init.d/%{name},g' %{name}.8 dkms dkms_autoinstaller dkms_framework.conf
gzip %{name}.8

%install
if [ "%{buildroot}" != "/" ]; then
        rm -rf %{buildroot}
fi
mkdir -p %{buildroot}/{%{_dkmsdir},%{_sbindir},%{_mandir}/man8,%{_sysconfdir}/%{name},%{_initrddir}}
install -m 755 dkms %{buildroot}/%{_sbindir}/dkms
install -m 644 dkms.8.gz %{buildroot}/%{_mandir}/man8
install -m 644 dkms_framework.conf  %{buildroot}%{_sysconfdir}/%{name}/framework.conf
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/
install -m 644 dkms_dbversion %{buildroot}/%{_dkmsdir}/dkms_dbversion
install -m 755 dkms_autoinstaller %{buildroot}%{_initrddir}/%{name}
install -m 755 dkms_mkkerneldoth %{buildroot}/%{_sbindir}/dkms_mkkerneldoth

# bash completion
install -d -m 755 %{buildroot}%{_sysconfdir}/bash_completion.d
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}

%clean 
if [ "%{buildroot}" != "/" ]; then
        rm -rf %{buildroot}
fi

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


