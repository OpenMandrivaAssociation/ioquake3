%define gitrev	ee7fde

Name:           ioquake3
Version:        1.36
Release:        12.%{gitrev}.1
Summary:        Quake 3 Arena engine (ioquake3 version)
Group:          Games/Shooter
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
Source0:        %{name}-%{version}-%{gitrev}.tar.xz
Source1:        %{name}-demo.sh
Source2:        %{name}.autodlrc
Source3:        %{name}.desktop
Source4:        %{name}.png
Source5:        %{name}-update.sh
Source6:        %{name}-update.autodlrc
#commented out because builds ok without them, just want to test it more
#to be sure they're not needed anymore
#Source7:       jpeg_memsrc.h
#Source8:       jpeg_memsrc.c
#Patch1:         quake3-1.34-rc4-demo-pak.patch
# patches from Debian for openarena compatibility (increase some buffer sizes)
# big-endian build fix
#Patch5:		cflags.patch
BuildRequires:  pkgconfig(sdl2)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:  pkgconfig(speexdsp)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  openal-soft-devel
BuildRequires:  jpeg-devel
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:  pkgconfig(opus)
BuildRequires:	pkgconfig(zlib)
BuildRequires:  desktop-file-utils
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
Group:          Games/Shooter
Requires:       ioquake3 = %{version}-%{release}
Requires:       opengl-games-utils 
BuildArch:      noarch

# quake3-demo used to be part of the quake3 package, make sure that people
# who have the old version with the demo included don't all of a sudden have
# the demo menu entry disappear.
#Obsoletes:      ioquake3 <= 1.34-0.4.rc4.fc9

%description demo
Quake 3 Arena tournament 3D shooter game demo installer. The Quake3 engine is
Open Source and as such is available as part of Mageia. The original Quake3
data files however are not Open Source and thus are not available as part of
Mageia. There is a gratis, but not Open Source demo available on the internet.

This package installs an application menu entry for playing the Quake3 Arena
demo. The first time you click this menu entry, it will offer to download and
install the Quake 3 demo datafiles for you.


%prep
%setup -qn %{name}-%{version}-%{gitrev}
%apply_patches

%build
# the CROSS_COMPILING=1 is a hack to not build q3cc and qvm files
# since we've stripped out q3cc as this is not Free Software.
%make \
    DEFAULT_BASEDIR=%{_datadir}/%{name} \
    USE_CODEC_VORBIS=1 \
    USE_CODEC_OPUS=1 \
    USE_LOCAL_HEADERS=0 \
    OPTIMIZE="%{optflags}" \
    CFLAGS="%{optflags}" \
    LDFLAGS="%{ldflags}" \
    CC=%{__cc} \
    BUILD_GAME_SO=0 \
    GENERATE_DEPENDENCIES=0 \
    USE_INTERNAL_SPEEX=0 \
    USE_INTERNAL_ZLIB=0 \
    USE_INTERNAL_JPEG=0 \
    BUILD_CLIENT_SMP=1 \
    V=1 \
    CROSS_COMPILING=1


%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/%{name}

install -m 755 build/release-linux-*/%{name}.* \
  %{buildroot}%{_bindir}/%{name}

install -m 755 build/release-linux-*/*.so* \
  %{buildroot}%{_datadir}/%{name}

install -m 755 build/release-linux-*/ioq3ded.* \
  %{buildroot}%{_bindir}/ioq3ded
install -p -m 755 %{SOURCE1} %{buildroot}%{_bindir}/ioquake3-demo
install -p -m 644 %{SOURCE2} %{buildroot}%{_datadir}/%{name}

install -p -m 755 %{SOURCE5} %{buildroot}%{_bindir}/ioquake3-update
install -p -m 644 %{SOURCE6} %{buildroot}%{_datadir}/%{name}

# below is the desktop file and icon stuff.
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install --vendor %{_vendor} \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE3}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/64x64/apps
install -p -m 644 %{SOURCE4} \
  %{buildroot}%{_datadir}/icons/hicolor/64x64/apps


%files
%doc BUGS ChangeLog COPYING.txt id-readme.txt md4-readme.txt NOTTODO
%doc TODO
%{_bindir}/%{name}
%{_bindir}/%{name}-update
%{_bindir}/ioq3ded
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/%{name}-update.autodlrc
%{_datadir}/%{name}/*.so

%files demo
%{_bindir}/%{name}-demo
%{_datadir}/%{name}/%{name}.autodlrc
%{_datadir}/applications/%{_vendor}-%{name}.desktop
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
