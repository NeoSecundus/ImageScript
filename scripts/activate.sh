#!/bin/bash

# Gets the project root path
BASEDIR="$( cd "$( dirname "${BASH_SOURCE}" )" >/dev/null 2>&1 && pwd)/.."
BASEDIR=$(realpath "$BASEDIR")

# Checks that this script is sourced
if [[ $0 != "/bin/bash" && $0 != "bash" && $0 != "-bash" && $0 != "/usr/bin/bash" ]]; then
    echo -e "\e[31;1mScript needs to be run with 'source'! source activate.sh\e[0m" >&2
    exit 1
fi

# Activate virtual environment
conda -V > /dev/null
if [[ $? == 0 ]]; then
    echo "> Activating virtual env"
    conda activate imgscript
else
    echo -e "\e[31m> Could not activate virtual env\e[0m"
fi
export PYTHONPATH="$BASEDIR:$PYTHONPATH"

# Run Pre-commit install
pre-commit install &> /dev/null && echo "> Pre-commit is installed" || echo -e "\e[31m> Pre-commit install FAILED\e[0m"


# Creating aliases
echo "> Creating command aliases"
alias is-lint="ruff check --config $BASEDIR/pyproject.toml --fix $BASEDIR/imagscript; pyright $BASEDIR/imagescript"
alias is-docs="pdoc -o docs/ -d google --footer-text \"© $(date +%Y) Nikolas Teuschl. All Rights Reserved.\" $BASEDIR/imagscript"
alias is-env-update="pip freeze > $BASEDIR/requirements.txt; conda env export > $BASEDIR/conda-env.yaml"
alias is-help="echo \"Story-Vault Repo Commands:
--------------------------
is-lint             - Runs linter and type checker.
is-docs             - Generates an updated module documentation and saves it to docs/module_docs.
is-env-update       - Updates requirements and conda env with the newest environment.
is-help             - Show this help.\"
"
echo -e "\e[33m> Enter is-help for command listing\e[0m"
