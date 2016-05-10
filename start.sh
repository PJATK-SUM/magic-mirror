#!/bin/bash

APPNAME=magic-mirror
APP_PATH=/var/www/$APPNAME
BUNDLE_PATH=$APP_PATH/current
ENV_FILE=$APP_PATH/shared/env.list
PORT=8080

# Remove previous version of the app, if exists
docker rm -f $APPNAME

docker run \
  -d \
  --restart=always \
  --publish=$PORT:80 \
  --volume=$BUNDLE_PATH:/bundle \
  --env-file=$ENV_FILE \
  --link=mongodb:mongodb \
  --hostname="$HOSTNAME-$APPNAME" \
  --env=MONGO_URL=mongodb://mongodb:27017/$APPNAME \
  --name=$APPNAME \
  meteorhacks/meteord:base
