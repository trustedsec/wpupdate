#!/usr/bin/python
#
# automatic installation of wordpress
#
#
from src.wpcore import *
import os
import sys

# first check if we are installed
if not os.path.isfile("/etc/init.d/wpupdate"):
    print "[!] WPUpdate not installed. Run python setup.py to install"

# create the database directory if its not there
if not os.path.isdir("/usr/share/wpupdate/database"):
    os.makedirs("/usr/share/wpupdate/database")

# kick start the updates
update_check()
