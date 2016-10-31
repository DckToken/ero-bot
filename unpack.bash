#!/bin/bash
#usage: ./unpack.bash <zip name>
set -e
ARG="$1"
CHECK="/media/ero-bot/$ARG"
if [ -d "$CHECK" ]; then
  echo "[BASH] Folder alredy exist"
  exit 34
fi
FILE=/media/ero-bot/list.txt #file must have a blank newline to work
cd /media/doujins/
if ! [ -f "$ARG.zip" ]; then
  echo "[BASH] File not found"
  exit 69
fi
unzip -o /media/doujins/"$ARG".zip -d /media/ero-bot/ #unzips into the bot folder
rm "$ARG.zip"
cd /media/ero-bot/"$ARG"
OUTPUT="$(find . -mindepth 1 -type d | wc -l)" #how many doujinshi at folder
echo -e $"\n~$ARG|${OUTPUT}" >> $FILE #makes the show entrance
for (( i = 1; i < $OUTPUT + 1; i++ )); do #for every doujinshi do
        LINE="$(ls -1 | sed -n "$i p" )" #the line is the $ith line
        cd "${LINE}" #enters into it
        rm _* #deletes unnecesary bullshit
        FILENAME="$(ls -1tr | grep -e '-1.jpg')" #gets the filename, its safe to use cut because i alredy grep'ed the first file
        FILENAME=${FILENAME:0:${#FILENAME} - 5} #removes the alredy greped '-1.jpg'
        PAGES="$(ls -1 | wc -l)" #the linecount of ls -1
        EXT="$(ls -1tr | head -n 1 | cut -d '.' -f 2)" #same as filename, but poorly done
        echo "$LINE:$FILENAME:$PAGES:$EXT" >> $FILE
        cd ..
done

