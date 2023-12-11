#!/bin/sh
# Some common shell stuff.

echo "Importing from common.sh"

DB=usersDB
USER=WilliamYuxinXu
URI_FRONT='mongodb+srv://WilliamYuxinXu:'
URI_BACK='@swees.mumkgcx.mongodb.net/?retryWrites=true&w=majority'
URI="${URI_FRONT}${MONGODB_PASSWORD}${URI_BACK}"
CONNECT_STR="mongodb+srv://swees.mumkgcx.mongodb.net/"
if [ -z $DATA_DIR ]
then
    DATA_DIR=/Users/ez/Desktop/Git/SWEES_fall2023
fi
BKUP_DIR=$DATA_DIR/bkup
EXP=mongoexport
IMP=mongoimport

if [ -z $MONGODB_PASSWORD ]
then
    echo "You must set MONGDBO_PASSWORD in your env before running this script."
    exit 1
fi

UserCollections=("newsDB" "users")
echo ${UserCollections[@]}