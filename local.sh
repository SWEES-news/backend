#!/bin/bash

export FLASK_ENV=development
export PROJ_DIR=$PWD
export DEBUG=1
export SECRET_KEY='h-J_l62fxF1uDXqKjHS3EQ'

# run our server locally:
PYTHONPATH=$(pwd):$PYTHONPATH
pip install -r requirements.txt
FLASK_APP=server.endpoints flask run --debug --host=127.0.0.1 --port=8000
