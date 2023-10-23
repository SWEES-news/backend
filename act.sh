#/bin/bash

API_KEY_FILE="api_key.txt" # put your API key in a file named api_key.txt

source .venv/bin/activate
# to get this venv on your own: 
# $ python -m venv .venv

if [ -f "$API_KEY_FILE" ]
then
  export NEWS_API_KEY="$(cat $API_KEY_FILE)";
  echo "News API key stored in NEWS_API_KEY."
else
  echo "could not find your news API key."
fi
