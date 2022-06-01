#!/bin/bash
wget -O /etc/opt/srlinux/cli/plugins/fabric.py  https://raw.githubusercontent.com/aaakpinar/srlinux/main/cliplugin/show%20fabric/fabric.py 
wget -O ./get-show-fabric.sh https://raw.githubusercontent.com/aaakpinar/srlinux/main/cliplugin/show%20fabric/get-show-fabric.sh
wget -O ./set-show-fabric.sh https://raw.githubusercontent.com/aaakpinar/srlinux/main/cliplugin/show%20fabric/set-show-fabric.sh
wget -O ./delete-show-fabric.sh https://raw.githubusercontent.com/aaakpinar/srlinux/main/cliplugin/show%20fabric/delete-show-fabric.sh
chmod +x ./get-show-fabric.sh ./set-show-fabric.sh ./delete-show-fabric.sh

bash ./set-show-fabric.sh
sr_cli
