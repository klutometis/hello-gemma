#!/usr/bin/env bash

# shFlags implements Google commandline-style flags.*
#
# * https://github.com/kward/shflags
. external/shflags/shflags

function main() {
    dir=$(mktemp -d)

    cp -frv main.py requirements.txt data "${dir}"

    cd "${dir}"

    gcloud functions deploy hello-gemma \
           --gen2 \
           --runtime=python312 \
           --region=us-west1 \
           --source=. \
           --entry-point=hello \
           --trigger-http \
           --allow-unauthenticated \
           --cpu=1 \
           --memory=2048M \
           --verbosity=debug

    # gcloud run deploy hello-gemma \
    #        --region=us-west1 \
    #        --source=. \
    #        --allow-unauthenticated \
    #        --cpu=1 \
    #        --memory=2048M \
    #        --verbosity=debug
}

# Fail early.
set -e
set -o pipefail

# Parse flags.
FLAGS "$@" || exit $?
eval set -- "${FLAGS_ARGV}"

# Start!
main "$@"
