#!/usr/bin/env bash

. venv.sh

function main() {
    venv
    pip install flake8
    flake8 --exclude=venv,external .
}

# Fail early.
set -e
set -o pipefail

# Start!
main "$@"
