#!/usr/bin/env bash

# shFlags implements Google commandline-style flags.*
#
# * https://github.com/kward/shflags
. external/shflags/shflags

function main() {
    gcloud functions deploy hello-gemma \
           --gen2 \
           --runtime=python312 \
           --region=us-west1 \
           --source=. \
           --entry-point=hello \
           --trigger-http \
           --allow-unauthenticated
}

# Fail early.
set -e
set -o pipefail

# Parse flags.
FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

# Start!
main "$@"
