#!/bin/bash
rm -f /etc/opt/srlinux/cli/plugins/fabric.py && echo fabric.py is removed!
rm -f ./set-show-fabric.sh && echo set script is removed!

read -p "Do you want to remove the get script as well? (Yes/No) [No]" get_remove
get_remove=${get_remove:-No}

if [ $get_remove == "Yes" ]; then
   SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";
   rm -rf $SCRIPT_DIR  || echo "Kaboom! It's gone!"
else
   rm $0 && echo "Removing the delete script!"
fi
