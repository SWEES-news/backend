#!/bin/sh
# Some common shell stuff.

echo "Importing from common.sh"

DB=usersDB
USER=WilliamYuxinXu
URI_FRONT='mongodb+srv://WilliamYuxinXu:'
URI_BACK='@swees.mumkgcx.mongodb.net/?retryWrites=true&w=majority'
URI=URI_FRONT+URI_BACK
CONNECT_STR="mongodb+srv://koukoumongo1.yud9b.mongodb.net/"
if [ -z $DATA_DIR ]
then
    DATA_DIR=/mnt/c/Users/xuwil/SWEES_fall2023
fi
BKUP_DIR=$DATA_DIR/bkup
EXP=/usr/local/bin/mongoexport
IMP=/usr/local/bin/mongoimport

if [ -z $MONGODB_PASSWORD ]
then
    echo "You must set MONGDBO_PASSWORD in your env before running this script."
    exit 1
fi

UserCollections=("newsDB" "users")
echo ${UserCollections[@]}