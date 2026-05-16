#!/usr/bin/env bash

echo "start tor"
tor &

# echo "setup playwright"
# playwright install --with-deps

echo "launch scraper"
python3 ./src/web_scraper.py
