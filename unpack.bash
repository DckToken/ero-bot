#!/bin/bash
#usage: ./unpack.bash <zip name>

FILE=/media/erobot/list.txt
cd /media/doujins/
unzip $1.zip -d /media/erobot/ #unzips into the bot folder
cd /media/erobot/$1
OUTPUT="$(find . -mindepth 1 -type d | wc -l)" #how many doujinshi at folder
sed -i -e '$a\' $FILE #insert newline
echo "~$1|${OUTPUT}" >> $FILE #after newline, makes the show entrance
for (( i = 1; i < $OUTPUT + 1; i++ )); do #for every doujinshi do
	LINE="$(ls -1 | sed -n "$i p" )" # the line is the $ith line
	cd "$LINE" #enters into it
	rm _* #deletes unnecesary bullshit
	FILENAME="$(ls -1tr | grep -e '-1.jpg' | cut -d '1' -f 1)" #gets the filename, its safe to use cut because i alredy grep'ed the first file
	PAGES="$(ls -1 | wc -l)" # pages the linecount of ls -1
	EXT="$(ls -1tr | head -n 1 | cut -d '.' -f 2)" #same as filename, but poorly done
	echo "$LINE:$FILENAME:$PAGES:$EXT" >> $FILE
	cd ..
done
