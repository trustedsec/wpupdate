#!/usr/bin/python
#
# quick script for installing wpupdate
#
#
import subprocess,re,os,shutil

from src.wpcore import *

print """
Welcome to the installer for WPUpdate. This will check once a day for updates within Wordpress. If
a new version is detected, it will automatically download and install Wordpress for you automatically.

Written by: Dave Kennedy (@HackingDave)
"""

def kill_wpupdate():
    print "[*] Checking to see if WPUpdate is currently running..."
    proc = subprocess.Popen("ps -au | grep /usr/share/wpupdate/wpupdate.py", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout = proc.communicate()
    try:
        for line in stdout:
            match = re.search("python /var/wpupdate/wpupdate.py", line) or re.search("python wpupdate.py", line)
            if match:
                print "[*] Killing running version of WPUpdate.."
                line = line.split(" ")
                pid = line[6]
                subprocess.Popen("kill %s" % (pid), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
                print "[*] Killed the WPUpdate process: " + pid
    except: pass

if os.path.isfile("/etc/init.d/wpupdate"):
    answer = raw_input("WPUpdate detected. Do you want to uninstall [y/n:] ")
    if answer.lower() == "yes" or answer.lower() == "y":
        answer = "uninstall"

if not os.path.isfile("/etc/init.d/wpupdate"):
    answer = raw_input("Do you want to proceed to install wpupdate? [y/n]: ")

    if answer.lower() == "y" or answer.lower() == "yes" or answer.lower() == "":
            print "[*] Checking out WPUpdate through github to /usr/share/wpupdate"
            # if old files are there
            if os.path.isdir("/usr/share/wpupdate"):
                shutil.rmtree('/usr/share/wpupdate')
            subprocess.Popen("git clone https://github.com/trustedsec/wpupdate /usr/share/wpupdate", shell=True).wait()
           # os.makedirs("/usr/share/wpupdate")
           # subprocess.Popen("cp -rf * /usr/share/wpupdate/", shell=True).wait()

            print "[*] Installing the service for you.."


            if not os.path.isfile("/etc/init.d/wpupdate"):
                fileopen = file("src/startup_wpupdate", "r")
                config = fileopen.read()
                filewrite = file("/etc/init.d/wpupdate", "w")
                filewrite.write(config)
                filewrite.close()
                print "[*] Triggering update-rc.d on wpupdate to automatically start..."
                subprocess.Popen("chmod +x /etc/init.d/wpupdate", shell=True).wait()
                subprocess.Popen("update-rc.d artillery defaults", shell=True).wait()

            print "[*] Finished. If you want to update WPUpdate go to /usr/share/wpupdate and type 'git pull'"

            choice = raw_input("Would you like to start WPUpdate now? [y/n]: ")
            if choice == "yes" or choice == "y":
            	subprocess.Popen("/etc/init.d/wpupdate start", shell=True).wait()
            	print "[*] Installation complete. Wordpress will update every morning at 2am."

if answer == "uninstall":
        os.remove("/etc/init.d/wpupdate")
        subprocess.Popen("rm -rf /usr/share/wpupdate", shell=True)
        subprocess.Popen("rm -rf /usr/share/wpupdate", shell=True)
        kill_wpupdate()
        print "[*] WPUpdate has been uninstalled. Manually kill the process if it is still running."
