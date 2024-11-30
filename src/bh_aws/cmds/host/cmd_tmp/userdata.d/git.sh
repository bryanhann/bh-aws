#!/usr/bin/env bash

export branch='ubuntu'
export url=http://github.com/bryanhann/bh-hostconfig
export install=/INSTALL
export repo=${install}/repo
export logfile=${install}/install.log
sudo mkdir -p  ${install}
sudo touch     ${logfile}
sudo chmod 777 ${logfile}

now () { echo $(date '+%Y-%m-%d-t %H:%M:%S') ;       }
log () { echo $(now) : "$@" >> ${logfile}    ;       }
run () { log "running: [$*]"                 ; $*  ; }

log "++ user-data [$0] [$*]"
log "[\$PWD]==[$PWD]  [\$\$]==[$$] [\$PPID]==[$PPID]"
run git clone ${url} -b ${branch} ${repo}
run ${repo}/bin/userdata apt $*
log "-- user-data [$0] [$*]"
