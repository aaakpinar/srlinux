HOW TO ADD CLI PLUGIN

1) Add the uplink ports, spine/RR BGP peer groups in the python code.
2) Go to SRL bash. 
3) Copy scripts to 'reports' folder
    sudo scp username@{remote-IP}:/{path-to-scripts}/\fabric.py /etc/opt/srlinux/cli/plugins/

4) Restart sr cli by logging out/in or simple run 'sr_cli' from bash.
5) Try 'show fabric' commands.

Enjoy!

-AA