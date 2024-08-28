export VIRTUAL_ENV  := ".venv"
export BIN := VIRTUAL_ENV + if os_family() == "unix" { "/bin" } else { "/Scripts" }


# list available commands
default:
    @{{ just_executable() }} --list


# compile requirements files
compile-reqs:
    #!/usr/bin/env bash
    set -euo pipefail

    uv --quiet pip compile --generate-hashes --strip-extras requirements.prod.in --output-file requirements.prod.txt
    uv --quiet pip compile --generate-hashes --strip-extras requirements.dev.in --output-file requirements.dev.txt


# install requirements
install-reqs:
    #!/usr/bin/env bash
    set -euo pipefail

    uv --quiet venv --python python3.12
    uv --quiet pip sync requirements.prod.txt requirements.dev.txt 


# check formatting, but don't modify anything
check: install-reqs
    #!/usr/bin/env bash
    set -euo pipefail

    $BIN/ruff format --diff .
    $BIN/ruff check .


# fix formatting
fix: install-reqs
    #!/usr/bin/env bash
    set -euo pipefail

    $BIN/ruff format .
    $BIN/ruff check --fix .
