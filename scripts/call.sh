#!/usr/bin/env bash

function main() {
    # curl -i $(gcloud functions describe hello-gemma --region=us-west1 | yq -r .url) \
    #      -X POST \
    #      -H 'Content-Type: application/x-www-form-urlencoded' \
    #      --data-urlencode 'SpeechResult=Programmers block'
    # curl -i https://us-west1-gen-lang-client-0615388941.cloudfunctions.net/hello-gemma \
    #      -X POST \
    #      -H 'Content-Type: application/x-www-form-urlencoded' \
    #      --data-urlencode 'SpeechResult=Programmers block'
    # curl -i https://hello-gemma-flkn235aya-uw.a.run.app \
    #      -X GET \
    #      -H 'Content-Type: application/x-www-form-urlencoded' \
    #      --data-urlencode 'SpeechResult=Programmers block'
    curl -i localhost:8080 \
         -X GET \
         -H 'Content-Type: application/x-www-form-urlencoded' \
         --data-urlencode 'SpeechResult=Programmers block'
    # gcloud functions call hello-gemma \
    #        --region=us-west1 \
    #        --gen2 \
    #        --data '{"name":"Kalani"}'
}

# Fail early.
set -e
set -o pipefail

# Start!
main "$@"
