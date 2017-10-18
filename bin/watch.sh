#! /bin/sh

YO_NORM="\033[0m"
YO_RED="\033[0;31m"
YO_GREEN="\033[0;32m"
YO_BROWN="\033[0;33m"
YO_BLUE="\033[0;34m"
YO_CYAN="\033[0;36m"
YO_CYAN="\033[0;36m"

platform=$(uname)
dir="$1"
shift
cmd="$*"

info() {
    printf "[$YO_CYAN+$YO_NORM] $*"
}

error() {
    printf "[$YO_RED-$YO_NORM] $*"
}

getChecksum() {
    checksum=""
    if [ "$platform" = "Darwin" ]; then
        checksum="$(find $dir -print0 | sort -zn | xargs -0 stat -f '%m' | cksum)"
    else
         checksum="$(find $dir -print0 | sort -zn | xargs -0 stat --printf='%Y\n' | cksum)"
    fi
    echo "$checksum"
}

watchForChanges() {
    while [ "$(getChecksum)" = "$last_checksum" ]; do
        sleep 0.5
    done
    last_checksum="$(getChecksum)"
}

changeDetected() {
    info "[$(date +%s)] Change detected, running command\n    $cmd"
    echo ""
    $cmd 2>&1 | sed "s/^/ │  /" | sed "$ s/│/└/"
    # echo ""
    watchForChanges
    changeDetected
}

last_checksum="$(getChecksum)"

watchForChanges
changeDetected
