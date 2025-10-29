%define		gitref		74213af1e952c4683d2e35952507133b61394862

Summary:	Firmware for Rockchip devices
Name:		rockchip-firmware
Version:	20250613
Release:	1
License:	Redistributable
Group:		Base/Kernel
Source0:	https://github.com/rockchip-linux/rkbin/archive/%{gitref}/rkbin-%{version}.tar.gz
# Source0-md5:	8ca527c652fb5ada44839315e297f74a
URL:		https://github.com/rockchip-linux/rkbin
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%description
Firmware for Rockchip devices.

%prep
%setup -q -n rkbin-%{gitref}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/rockchip-firmware
cp -pr RKBOOT RKTRUST bin img $RPM_BUILD_ROOT%{_datadir}/rockchip-firmware

# provide constant symlinks (without version part)
# if multiple versions are present choose latest one
for bin in `find $RPM_BUILD_ROOT%{_datadir}/rockchip-firmware/bin -type f -regex '.*_v[0-9.]+\.\(bin\|elf\)$'`; do
	bin_nover=$(echo $bin | sed -e 's/\(.*\)_v[0-9.]\+\.\(bin\|elf\)$/\1.\2/')
	if [ -e $bin_nover ]; then
		if [ "$(rpmvercmp $(readlink -f $bin_nover) $bin > /dev/null || echo $?)" = "2" ]; then
			ln -sf $(basename $bin) $bin_nover
		fi
	else
		ln -s $(basename $bin) $bin_nover
	fi
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README doc/release/*_EN.md
%lang(zh_CN) %doc doc/release/*_CN.md
%{_datadir}/rockchip-firmware
