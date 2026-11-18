%define		gitref		3e288fe814e059dd06833495f845cab04ac20a5c

Summary:	Firmware for Rockchip devices
Name:		rockchip-firmware
Version:	20260626
Release:	1
License:	Redistributable
Group:		Base/Kernel
Source0:	https://github.com/rockchip-linux/rkbin/archive/%{gitref}/rkbin-%{version}.tar.gz
# Source0-md5:	55f7fd3c1198d4eccbf68f235b866f80
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
%doc LICENSE README.md doc/release/*_EN.md
%lang(zh_CN) %doc README.zh.md doc/release/*_CN.md
%{_datadir}/rockchip-firmware
