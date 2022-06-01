OVERVIEW

The 'show fabric' command shows you statistics and the status of the uplinks and BGP peerings. 
It is programmed to be consumend by IP fabrics that are based on eBGP (between Spine/Leaf as IGP) and iBGP EVPN. 
Therefore it requires some inputs to discover your uplinks and BGP peerings. 

HOW TO GET AND SET SHOW FABRIC CLI PLUGIN INTO YOUR SR LINUX

1) Add the uplink interfaces (or a pattern that is common in uplink interface description) and eBGP/iBGP(RR) peer group names either via set-show-fabric.sh script or directly in the python code.
2) Go to SRL bash. 
3) Get the script the run it, or:
	3.1) Copy scripts to 'reports' folder
    	sudo scp username@{remote-IP}:/{path-to-scripts}/\fabric.py /etc/opt/srlinux/cli/plugins/
	3.2) Restart sr cli by logging out/in or simple run 'sr_cli' from bash.

Try 'show fabric' commands.

Enjoy!

-AA