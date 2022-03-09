#!bin/bash
gnome-terminal --command="bash -c 'cd web/gs; npm start; $SHELL'"
gnome-terminal --command="bash -c 'cd web/flask; . start.sh; $SHELL'"