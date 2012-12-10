#!/bin/bash

set -e

. /usr/share/opengl-games-utils/opengl-game-functions.sh

checkDriOK quake3

if [ ! -f $HOME/.q3a/baseq3/pak0.pk3 ]; then
  set +e
  /usr/share/autodl/AutoDL.py /usr/share/ioquake3/ioquake3.autodlrc
  STATUS=$?
  set -e
  # status 2 means download was ok, but the user choice not to start the game
  if [ "$STATUS" = "0" -o "$STATUS" = "2" ]; then
    cd ~/.q3a
    unzip -qq -u quake3-latest-pk3s.zip
    tail -n +165 linuxq3ademo-1.11-6.x86.gz.sh | gzip -d -c | \
      tar x demoq3/pak0.pk3
    # remove any old versions (if present) otherwise the mv fails
    rm -fr baseq3 missionpack
    mv quake3-latest-pk3s/* .
    mv demoq3/pak0.pk3 baseq3
    rm quake3-latest-pk3s.zip linuxq3ademo-1.11-6.x86.gz.sh
    rmdir quake3-latest-pk3s demoq3
  fi
  if [ "$STATUS" != "0" ]; then
    exit $STATUS
  fi
fi

exec ioquake3 "$@"
