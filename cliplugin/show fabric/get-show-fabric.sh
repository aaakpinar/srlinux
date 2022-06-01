#!/bin/bash
wget -O /etc/opt/srlinux/cli/plugins/fabric.py  https://raw.githubusercontent.com/aaakpinar/srlinux/main/cliplugin/show%20fabric/fabric.py 
wget -O ./set-show-fabric.sh https://raw.githubusercontent.com/aaakpinar/srlinux/main/cliplugin/show%20fabric/set-show-fabric.sh

chmod +x ./set-show-fabric.sh
./set-show-fabric.sh
sr_cli
