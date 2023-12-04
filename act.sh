#/bin/bash
ROOT_DIR=$(git rev-parse --show-toplevel); cd $ROOT_DIR
ENV_FILE=".env" # put your API keys in a .env file

# set all keys in env
if [ -f "$ENV_FILE" ]
then
  set -a
  . ./$ENV_FILE
  set +a
else
  echo "Could not find your env file \"$ENV_FILE\". Create it in the root directory."
fi

# activate venv if exists
if [[ -n $PYENV_DIR ]]; then
  source $PYENV_DIR/bin/activate
fi
