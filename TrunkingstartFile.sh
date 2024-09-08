#Modify this file to include your OP25 configuration and setup.
#!/bin/bash
cd /home/pi/op25/op25/gr-op25_repeater/apps
#./rx.py --args 'rtl' -N 'LNA:47' -S 1024000 -2 -x 0.8 -T TrunkingstartFile.tsv -q 0 -l http:0.0.0.0:8080 -U 2> stderr.2 ## regular .rx.py configuration
./multi_rx.py -c TrunkingstartFile.json 2> stderr.2 #multi_rx.py example
