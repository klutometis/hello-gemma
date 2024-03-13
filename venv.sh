#!/usr/bin/env sh

if (( HELLO_GEMMA_VENV__++ == 0)); then

function venv() {
    mkdir -p venv
    python3 -m venv venv
    . ./venv/bin/activate
}

fi  # include guard
