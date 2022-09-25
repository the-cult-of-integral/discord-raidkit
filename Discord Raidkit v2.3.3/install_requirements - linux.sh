#!/bin/bash
output=$(git --version)

if [ "$output" == "" ]
then
	echo "Git --version gave no output; assuming Git is not installed.";
	echo "Installing Git now. . .";
	sudo apt-get install git;
fi
python3 -m pip install git+https://github.com/Rapptz/discord.py selenium colorama requests bs4;
