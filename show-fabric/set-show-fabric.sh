#!/bin/bash
read -p "Uplink Interfaces Description Pattern: [spine] " description
description=${description:-spine}
echo $description
read -p "eBGP Group Name: [spine]:" uplink_peer_group
uplink_peer_group=${uplink_peer_group:-spine}
echo $uplink_peer_group
read -p "iBGP EVPN Group Name: [EVPN] " rr_peer_group
rr_peer_group=${rr_peer_group:-EVPN}
echo $rr_peer_group
read -p "Network Instance: [default] " uplink_network_instance
uplink_network_instance=${uplink_network_instance:-default}
echo $uplink_network_instance
#sed -i 's/description = ".*"/description = \"$description\"/'; 's/uplink_peer_group = ".*"/uplink_peer_group = \"$uplink_peer_group\"/'; 's/rr_peer_group = ".*"/rr_peer_group = \"$rr_peer_group\"/'; 's/uplink_network_instance = ".*"/uplink_network_instance = \"$uplink_network_instance\"/' /etc/opt/srlinux/cli/plugins/fabric.py

sed -i "s/description = ".*"/description = \"$description\"/" /etc/opt/srlinux/cli/plugins/fabric.py
sed -i "s/uplink_peer_group = ".*"/uplink_peer_group = \"$uplink_peer_group\"/" /etc/opt/srlinux/cli/plugins/fabric.py
sed -i "s/rr_peer_group = ".*"/rr_peer_group = \"$rr_peer_group\"/" /etc/opt/srlinux/cli/plugins/fabric.py
sed -i "s/uplink_network_instance = ".*"/uplink_network_instance = \"$uplink_network_instance\"/" /etc/opt/srlinux/cli/plugins/fabric.py

sr_cli



