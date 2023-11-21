#/bin/bash

PYENV_DIR=".venv"
ENV_FILE=".env" # put your API keys in a .env file
API_KEY_FILE="api_key.txt" # put your API key in a file named api_key.txt

source $PYENV_DIR/bin/activate
# to get this venv on your own: 
# $ python -m venv .venv

# set all keys in env
if [ -f "$ENV_FILE" ]
then
  set -a
  . ./$ENV_FILE
  set +a
else
  echo "Could not find your env file \"$ENV_FILE\". Create it in the root directory."

  # TODO delete once everyone's switched over
  if [ -f "$API_KEY_FILE" ]
  then
    echo "Warning: \"$API_KEY_FILE\" will be entirely replaced soon with \"$ENV_FILE\". See the README for details."
    export NEWS_API_KEY="$(cat $API_KEY_FILE)";
    echo "News API key stored in NEWS_API_KEY."
  fi

fi

