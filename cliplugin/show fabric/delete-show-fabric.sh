#!/bin/bash
rm -f /etc/opt/srlinux/cli/plugins/fabric.py && rm -f ./set-show-fabric.sh

read -p "Do you want to remove get script as well? [No]" get_remove
get_remove=${get_remove:-No}

if [ $get_remove == "Yes" ]; then
   rm -f ./get-show-fabric.sh || echo "Failed to remove get script! It may not be at $PATH."
fi

rm $0 && echo "Removing the delete script!"
