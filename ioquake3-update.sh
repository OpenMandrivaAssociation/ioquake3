#!/bin/bash

set -e

if [ ! -f $HOME/.q3a/baseq3/pak8.pk3 ]; then
  set +e
  /usr/share/autodl/AutoDL.py /usr/share/ioquake3/ioquake3-update.autodlrc
  STATUS=$?
  set -e
  # status 2 means download was ok, but the user choice not to start the game
  if [ "$STATUS" = "0" -o "$STATUS" = "2" ]; then
    cd ~/.q3a
    sh linuxq3apoint-1.32b-3.x86.run  --tar xf -C . --exclude setup.*
    rm linuxq3apoint-1.32b-3.x86.run
  fi
else
  echo "You already have quake 3 1.32b update!" ;
fi
