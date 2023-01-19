Steps To make it work

1: from command line, in folder where you want to store the files, do:  
   - git clone https://github.com/currentnetworks/edgeos-remote-changes/
2: Look through and follow commands in prereqs.txt  
3: Fill routers.txt with list of router ip addresses that you want to change  
4: run python3 changes_edgeos.py from the folder containing the files  
5: Watch output on screen, if a username / password is wrong, it will give you the chance to try 2 more times with different credentials before moving onto the next  
6: Check log.txt for all details after script has completed, copy this file if you want to keep it before running the script again.   