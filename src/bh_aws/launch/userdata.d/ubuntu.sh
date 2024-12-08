#!/usr/bin/env bash
# userdata: ./userdata.d/ubuntu.sh

REPO_SRC="http://github.com/bryanhann/bh-hostconfig -b ubuntu"
REPO_DST=/INSTALL/repo
REPO_INSTALL=
INSTALL=/INSTALL
LOGFILE=/var/log/log.bh.install

sudo touch $LOGFILE
sudo chmod 777 $LOGFILE
_now () { echo $(date '+%Y-%m-%d-t-%H:%M:%S') ;       }
_log () { echo $(_now) : "$@" >> $LOGFILE     ;       }
_run () { _log "running: [$*]"                ; $*  ; }

_log "++ user-data [$0] [$*]" >> $LOGFILE
_run sudo mkdir /INSTALL
_run git clone $REPO_SRC $REPO_DST
_run . ${REPO_DST}/bin/activate
_log "user-data: tilde is [~]"
_log "user-data: HOME is [$HOME]"
_run bozovnc
_log "-- user-data [$0] [$*]"
