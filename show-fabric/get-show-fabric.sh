#!/bin/bash
wget -O /etc/opt/srlinux/cli/plugins/fabric.py  https://raw.githubusercontent.com/aaakpinar/srlinux/main/show-fabric/fabric.py
if [ "${PWD##*/}" != "show-fabric" ]; then
   mkdir -p show-fabric && cd show-fabric
fi
wget -O ./get-show-fabric.sh https://raw.githubusercontent.com/aaakpinar/srlinux/main/show-fabric/get-show-fabric.sh
wget -O ./set-show-fabric.sh https://raw.githubusercontent.com/aaakpinar/srlinux/main/show-fabric/set-show-fabric.sh
wget -O ./delete-show-fabric.sh https://raw.githubusercontent.com/aaakpinar/srlinux/main/show-fabric/delete-show-fabric.sh
chmod +x ./get-show-fabric.sh ./set-show-fabric.sh ./delete-show-fabric.sh
echo -e 'You got the show fabric plugin and the scripts now! \n If you want to set the parameters later, EXIT with Ctrl+C... \n'
bash ./set-show-fabric.sh
