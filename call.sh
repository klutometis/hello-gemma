#!/usr/bin/env bash

function main() {
    curl -i localhost:8080 \
         -X POST \
         -H 'Content-Type: application/x-www-form-urlencoded' \
         --data-urlencode 'SpeechResult=I have a fever'
}

# Fail early.
set -e
set -o pipefail

# Start!
main "$@"
