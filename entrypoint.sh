#!/usr/bin/env bash

echo "start tor"
tor &

# echo "setup playwright"
# playwright install --with-deps

echo "launch scraper"
# /usr/bin/sh -c "python3 ./src/web_scraper.py"
/usr/local/bin/supercronic /etc/crontab 
