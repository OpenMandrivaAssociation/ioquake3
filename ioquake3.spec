  
%define q3dir %{buildroot}%{_libdir}/ioquake3
%define svnrev 1486

Name:	ioquake3
%define with_installer %{?_with_installer:1}%{!?_with_installer:0}
BuildRequires:	SDL-devel curl-devel nasm openal-devel
%if 0%{?mandriva_version}
BuildRequires:	mesagl-devel mesaglu-devel openal-devel
# XXX: ambiguous requirement of alsa-plugins
BuildRequires:	libspeex
%else
%endif
%if 0%{?fedora_version} || 0%{?rhel_version} || 0%{?centos_version}
# XXX bug in openal-devel, should be worked around in build config
BuildRequires:	openal-devel
%endif
%if %with_installer
BuildRequires:	loki_setup xdg-utils
%endif
License:	GPLv2+
URL:	http://icculus.org/quake3/
Group:	Games/Arcade
# don't forget to change the version in the win32 spec file as well!
Version:	1.35
%define rel 2
%if %{?svnrev:1}%{?!svnrev:0}
Release:	%mkrel %rel -c %{svnrev}
%else
Release:	%mkrel %rel
%endif
Summary:	Quake III
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Source:	ioquake3-%{version}%{?svnrev:_SVN%{svnrev}}.tar.bz2
%if %with_installer
Recommends:	openal
%endif

%package devel
License:	GPLv2+
Summary:	Quake III
Group:	Development/Other
%if %with_installer

%package setup
License:	GPLv2+
Summary:	Quake III loki-setup based installer
Group:	Games/Arcade
%endif

%description
Quake III first person shooter. This package only includes the binary
files, you still need the data files from the original Quake III CD or
the Demo.



Authors:
--------
	Id Software, Inc.

%description devel
Quake III development tools for creating mods: q3lcc, q3rcc, q3cpp,
q3asm



Authors:
--------
	Id Software, Inc.

%if %with_installer
%description setup
Quake III first person shooter. This package includes the binary files
repackaged as loki-setup installer



Authors:
--------
	Id Software, Inc.

%endif
%prep
%setup -q -n %{name}-%{version}%{?svnrev:_SVN%{svnrev}}
rm -rf code/SDL12 code/libs code/AL

%build
cat > dobuild <<'EOF'
#!/bin/sh
make %{?jobs:-j%jobs} \
	VERSION=%{version} \
	RELEASE=%{release} \
	OPTIMIZE="%{optflags} -O3 -ffast-math -fno-strict-aliasing" \
	TOOLS_OPTIMIZE="%{optflags} -fno-strict-aliasing" \
	GENERATE_DEPENDENCIES=0 \
	USE_LOCAL_HEADERS=0 \
%if %with_installer
	USE_OPENAL_DLOPEN=1 \
%endif
	V=1 \
	"$@"
EOF
chmod 755 dobuild
#
./dobuild release
#
%if %with_installer
./dobuild installer
%endif
#
%install
rm -rf %{buildroot}
arch=`uname -m`
case $arch in
	i?86) arch=i386 ;;
esac
install -d -m 755 %{q3dir}
install -d -m 755 %{q3dir}/baseq3/vm
install -d -m 755 %{q3dir}/demoq3
install -d -m 755 %{q3dir}/missionpack/vm
pushd build/release-linux-$arch/
install -m 755 ioquake3.$arch %{q3dir}/
#install -m 755 linuxquake3-smp %{q3dir}/ioquake3-smp.$arch
install -m 755 ioq3ded.$arch %{q3dir}/
install -m 644 baseq3/*.so %{q3dir}/baseq3
install -m 644 baseq3/vm/*.qvm %{q3dir}/baseq3/vm
pushd %{q3dir}/demoq3
ln -s ../baseq3/*.so .
popd
install -m 644 missionpack/*.so %{q3dir}/missionpack
install -m 644 missionpack/vm/*.qvm %{q3dir}/missionpack/vm
popd
#
# icons and start scripts
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_datadir}/pixmaps
install -d -m 755 %{buildroot}%{_datadir}/applications
install -m 644 misc/quake3.png %{buildroot}%{_datadir}/pixmaps
install -m 644 misc/setup/ioquake3.desktop %{buildroot}%{_datadir}/applications/ioquake3.desktop
install -m 755 misc/setup/ioq3demo.sh %{q3dir}/
install -m 755 misc/setup/ioquake3.sh %{q3dir}/
# COOLO! *grr*
#ln -s %{_prefix}/lib/quake3/ioq3demo.sh %{buildroot}%{_bindir}/ioq3demo
#ln -s %{_prefix}/lib/quake3/ioquake3.sh %{buildroot}%{_bindir}/ioquake3
for i in ioq3demo ioquake3; do
	echo -e "#!/bin/sh\nexec /usr/lib/ioquake3/$i.sh \"\$@\"" > %{buildroot}%{_bindir}/$i
	chmod 755 %{buildroot}%{_bindir}/$i
done
#
# devel tools
install -d -m 755 %{buildroot}%{_bindir}
install -m 755 build/release-linux-$arch/tools/q3{lcc,cpp,rcc,asm} %{buildroot}%{_bindir}
#
# installer
%if %with_installer
install -d -m 755 %{buildroot}/%{_gamesbindir}
install -m 755 misc/setup/*.run %{buildroot}/%{_gamesbindir}
%endif

%clean
rm -rf %{buildroot}

%post

%files
%defattr(-,root,root)
%doc COPYING.txt README id-readme.txt
%doc voip-readme.txt
%{_bindir}/ioq*
%{_libdir}/ioquake3
%{_datadir}/applications/*
%{_datadir}/pixmaps/*

%files devel
%defattr(-,root,root)
%doc code/tools/lcc/COPYRIGHT
%{_bindir}/q3*
%if %with_installer

%files setup
%defattr(-,root,root)
%{_prefix}/games/*
%endif
