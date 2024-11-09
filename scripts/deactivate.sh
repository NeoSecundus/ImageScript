#!/bin/bash

# Gets the project root path
BASEDIR="$( cd "$( dirname "${BASH_SOURCE}" )" >/dev/null 2>&1 && pwd)"
BASEDIR=$(realpath "$BASEDIR")

# Checks that this script is sourced
if [[ $0 != "/bin/bash" && $0 != "bash" && $0 != "-bash" && $0 != "/usr/bin/bash" ]]; then
    echo -e "\e[31;1mScript needs to be run with 'source'! source activate.sh\e[0m" >&2
    exit 1
fi

# Deactivate virtual env
conda -V > /dev/null
if [[ $? == 0 ]]; then
    echo "Deactivating virtual env..."
    conda deactivate
fi

# Removing Path variables
# if [[ -n $OLDPATH ]]; then
#     echo "Removing PATH variables..."
#     export PATH=$OLDPATH
#     export OLDPATH=""
# fi
export PYTHONPATH=""

# Removes all command aliases
unalias sv-lint sv-help sv-docs sv-env-update 2> /dev/null

echo "Done!"
