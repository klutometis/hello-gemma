#!/usr/bin/env bash

# shFlags implements Google commandline-style flags.*
#
# * https://github.com/kward/shflags
. external/shflags/shflags

function main() {
    gcloud functions call hello-gemma \
           --region=us-west1 \
           --gen2 \
           --data '{"name":"Kalani"}'
}

# Fail early.
set -e
set -o pipefail

# Parse flags.
FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

# Start!
main "$@"
