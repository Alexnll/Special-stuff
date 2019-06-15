#! /usr/bin/bash

read -p "You want to create a .sh file in current location? y/n   " judge1
if  [ $judge1 == "y" ]
then
	read -p "Please print the name of your .sh file: " name
	if [ -e $name ]
	then
		echo "The file "  $name  " is already existed. "
		echo "Please try more time with new file name."
	else
		touch $name
		chmod +x $name
		echo "#! /usr/bin/bash" >> $name
	fi
else
	read -p "You want to (1) create a .sh in a new dir or (2) exit? 1/2   " judge2
	if [ $judge2 == 1 ]
	then
		mkdir new
		cd new
		read -p "Please print the name of your .sh file: " name
		touch $name
		chmod +x $name
		echo "#! /usr/bin/bash" >> $name
	else
		echo "Ended."
	fi
fi