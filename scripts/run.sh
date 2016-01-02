#!/usr/bin/env bash
APP_ROOT="$(dirname "$(dirname "$(readlink "$0")")")"

echo "Start import procedure."
python $APP_ROOT/microblogging/main.py

echo "Import finished!"

echo "Starting the queries..."

python $APP_ROOT/microblogging/queries.py