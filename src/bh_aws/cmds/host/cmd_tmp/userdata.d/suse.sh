#!/bin/bash
# userdata: userdata.d/suse.sh

INSTALL=/INSTALL
LOG=${INSTALL}/install.log
REPO=${INSTALL}/repo

sudo mkdir -p ${INSTALL}
sudo touch ${LOG}
sudo chmod 777 ${LOG}

now () { echo $(date '+%Y-%m-%d %H:%M:%S')  ;       }
log () { echo $(now) : "$@" >> $LOG         ;       }
run () { log "running: [$*]"                ; $*  ; }

_install () {
      log "_install: $1 is at [$(which $1)]"
      which $1 && return
      run echo _install is not configured
      log "_install: $1 is at [$(which $1)]"
 }

log "++ user-data [$0] [$*]"
log "user-data: tilde is [~]"
log "user-data: HOME is [$HOME]"
_install stow
_install mcrypt
_install gh
_install expect
_install python3
_install curl
_install tasksel
_install slim
_install Ubuntu-desktop
_install tigervnc-standalone-server
run git clone http://github.com/bryanhann/bh-hostconfig -b ubuntu ${REPO}
#curl -LsSf https://astral.sh/uv/install.sh | sh
#sudo snap install astral-uv
log "-- user-data [$0] [$*]"
