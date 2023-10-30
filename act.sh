#/bin/bash

PYENV_DIR=".venv"
API_KEY_FILE="api_key.txt" # put your API key in a file named api_key.txt

source $PYENV_DIR/bin/activate
# to get this venv on your own: 
# $ python -m venv .venv

if [ -f "$API_KEY_FILE" ]
then
  export NEWS_API_KEY="$(cat $API_KEY_FILE)";
  echo "News API key stored in NEWS_API_KEY."
else
  echo "Could not find your news API key. Store it at the root directory in a file named $API_KEY_FILE."
fi
