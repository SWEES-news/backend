#!/bin/bash
# This shell script deploys a new version to a server.

PROJ_DIR=SWEES_fall2023
VENV=SWEES
PA_DOMAIN="SWEES.pythonanywhere.com"
PA_USER='SWEES'
echo "Project dir = $PROJ_DIR"
echo "PA domain = $PA_DOMAIN"
echo "Virtual env = $VENV"

if [ -z "$PA_PWD" ]
then
    echo "The PythonAnywhere password var (PA_PWD) must be set in the env."
    exit 1
fi

echo "PA user = $PA_USER"
echo "PA password = $PA_PWD"

echo "SSHing to PythonAnywhere."
sshpass -p $PA_PWD ssh -o "StrictHostKeyChecking no" $PA_USER@ssh.pythonanywhere.com << EOF
    cd ~/$PROJ_DIR; PA_USER=$PA_USER PROJ_DIR=~/$PROJ_DIR VENV=$VENV PA_DOMAIN=$PA_DOMAIN ./rebuild.sh
EOF
