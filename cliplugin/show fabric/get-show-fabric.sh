#!/bin/bash
wget -O /etc/opt/srlinux/cli/plugins/fabric.py  https://raw.githubusercontent.com/aaakpinar/srlinux/main/cliplugin/show%20fabric/fabric.py 
echo ${PWD##*/}
if [["${PWD##*/}" == "show-fabric"]]; then 
   mkdir -p show-fabric 
fi
wget -O ./show-fabric/get-show-fabric.sh https://raw.githubusercontent.com/aaakpinar/srlinux/main/cliplugin/show%20fabric/get-show-fabric.sh
wget -O ./show-fabric/set-show-fabric.sh https://raw.githubusercontent.com/aaakpinar/srlinux/main/cliplugin/show%20fabric/set-show-fabric.sh
wget -O ./show-fabric/delete-show-fabric.sh https://raw.githubusercontent.com/aaakpinar/srlinux/main/cliplugin/show%20fabric/delete-show-fabric.sh
chmod +x ./show-fabric/get-show-fabric.sh ./show-fabric/set-show-fabric.sh ./show-fabric/delete-show-fabric.sh

bash ./show-fabric/set-show-fabric.sh
