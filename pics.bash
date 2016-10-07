#!/bin/bash
set -e
cd /media/ero-bot/avis/
OUTPUT="$(ls -1 | wc -l)"
echo $OUTPUT
