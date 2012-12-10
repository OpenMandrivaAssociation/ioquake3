#define debug_package	%{nil}
%define         svnrev svn2102
Name:           ioquake3
Version:        1.36
Release:        1.%{svnrev}
Summary:        Quake 3 Arena engine (ioquake3 version)
Group:          Games/Arcade
License:        GPLv2+
URL:            http://ioquake3.org/
# to regenerate (note included systemlib copies are removed for size, lcc
# is removed as it is not Free software):
# svn co svn://svn.icculus.org/quake3/tags/%{version} %{name}-%{version}
# pushd %{name}-%{version}
# rm -fr `find -name .svn` code/AL code/SDL12 code/libcurl code/libs
# rm -fr code/jpeg-8c code/zlib code/libspeex code/tools/lcc
# popd
# tar cvfj %{name}-%{version}.tar.bz2 %{name}-%{version}
Source0:        %{name}-%{version}-svn2102.tar.bz2
Source1:        %{name}-demo.sh
Source2:        %{name}.autodlrc
Source3:        %{name}.desktop
Source4:        %{name}.png
Source5:        %{name}-update.sh
Source6:        %{name}-update.autodlrc
Patch1:         quake3-1.34-rc4-demo-pak.patch
# patches from Debian for openarena compatibility (increase some buffer sizes)
Patch2:         0011-Double-the-maximum-number-of-cvars.patch
Patch3:         0012-Increase-the-command-buffer-from-16K-to-128K-followi.patch
# big-endian build fix
Patch4:         quake3-1.36-build.patch
BuildRequires:  pkgconfig(sdl)
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(openal)
BuildRequires:  jpeg-devel
BuildRequires:  pkgconfig(speex)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
%ifarch %{ix86} x86_64
BuildRequires:  nasm
%endif
# for quake3-update
Requires:       autodownloader 

%description
This package contains the enhanced opensource ioquake3 version of the Quake 3
Arena engine. This engine can be used to play a number of games based on this
engine, below is an (incomplete list):

* OpenArena, Free, Open Source Quake3 like game, recommended!
  (packagename: openarena)

* Urban Terror, gratis, but not Open Source FPS best be described as a
  Hollywood tactical shooter, a downloader and installer including an
  application menu entry is available in the urbanterror package.

* World of Padman, gratis, but not Open Source Comic FPS, a downloader and
  installer including an application menu entry is available in the
  worldofpadman package.

* Smokin' Guns, gratis, but not Open Source FPS, a semi-realistic simulation of 
  the "Old West's" great atmosphere, a downloader and installer including an
  application menu entry is available in the smokinguns package.

* Quake3 Arena, the original! A downloader and installer for the gratis, but
  not Open Source demo, including an application menu entry is available in
  the quake3-demo package.
  
  If you own a copy of quake 3, you will need to copy pak0.pk3 from the
  original CD-ROM and your q3key to /usr/share/quake3/baseq3 or ~/.q3a/baseq3.
  Also copy the pak?.pk3 files from the original 1.32 Quake 3 Arena point
  release there if you have them available or run quake3-update to download
  them for you.


%package demo
Summary:        Quake 3 Arena tournament 3D shooter game demo installer
Group:          Games/Arcade
Requires:       ioquake3 = %{version}-%{release}
Requires:       opengl-games-utils 
BuildArch:      noarch

# quake3-demo used to be part of the quake3 package, make sure that people
# who have the old version with the demo included don't all of a sudden have
# the demo menu entry disappear.


%description demo
Quake 3 Arena tournament 3D shooter game demo installer. The Quake3 engine is
Open Source and as such is available as part of Mageia. The original Quake3
data files however are not Open Source and thus are not available as part of
Mageia. There is a gratis, but not Open Source demo available on the internet.

This package installs an application menu entry for playing the Quake3 Arena
demo. The first time you click this menu entry, it will offer to download and
install the Quake 3 demo datafiles for you.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1



%build
# the CROSS_COMPILING=1 is a hack to not build q3cc and qvm files
# since we've stripped out q3cc as this is not Free Software.
%make \
    OPTIMIZE="$RPM_OPT_FLAGS -fno-strict-aliasing" \
    DEFAULT_BASEDIR=%{_datadir}/%{name} \
    USE_CODEC_VORBIS=1 \
    USE_LOCAL_HEADERS=0 \
    BUILD_GAME_SO=0 \
    GENERATE_DEPENDENCIES=0 \
    USE_INTERNAL_SPEEX=0 \
    USE_INTERNAL_ZLIB=0 \
    USE_INTERNAL_JPEG=0 \
    BUILD_CLIENT_SMP=1 \
    CROSS_COMPILING=1


%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}

install -m 755 build/release-linux-*/%{name}.* \
  $RPM_BUILD_ROOT%{_bindir}/%{name}
install -m 755 build/release-linux-*/%{name}-smp.* \
  $RPM_BUILD_ROOT%{_bindir}/%{name}-smp
install -m 755 build/release-linux-*/ioq3ded.* \
  $RPM_BUILD_ROOT%{_bindir}/ioq3ded
install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/ioquake3-demo
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/%{name}

install -p -m 755 %{SOURCE5} $RPM_BUILD_ROOT%{_bindir}/ioquake3-update
install -p -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_datadir}/%{name}

# below is the desktop file and icon stuff.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE3}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps
install -p -m 644 %{SOURCE4} \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps


%files
%doc BUGS ChangeLog COPYING.txt id-readme.txt md4-readme.txt NOTTODO README
%doc TODO
%{_bindir}/%{name}
%{_bindir}/%{name}-smp
%{_bindir}/%{name}-update
%{_bindir}/ioq3ded
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/%{name}-update.autodlrc

%files demo
%{_bindir}/%{name}-demo
%{_datadir}/%{name}/%{name}.autodlrc
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
