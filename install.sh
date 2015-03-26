#!/bin/bash
if [ "$(whoami)" != "root" ]; then
	echo "Ce script doit être lancé avec les droits administrateur."
	exit 1
else
	echo "You're a super admin motherfucker !"
	apt-get install mysql-client-5.5 > ./result.txt
	apt-get install python-pip >> ./result.txt
	apt-get install python-mysqldb >> ./result.txt
	pip install jsonpickle >> ./result.txt
	pip install flask >> ./result.txt
	pip install passlib >> ./result.txt
fi
