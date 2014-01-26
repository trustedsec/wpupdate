#!/usr/bin/python
#
#
# functions for wpupdate
#
#
import time
import datetime
import hashlib
import subprocess
import os
import urllib2
import re

# check config
def check_config(param):
        # grab the default path
        if os.path.isfile("config"):
            path = "config"
        else:
            path = "/usr/share/wpupdate/config"
        fileopen = file(path, "r")
        # iterate through lines in file
        for line in fileopen:
            if not line.startswith("#"):
                match = re.search(param, line)
                if match:
                    line = line.rstrip()
                    line = line.replace('"', "")
                    line = line.split("=", 1)
                    return line[1]

# quick progress bar downloader
def download_file(url,filename):
    u = urllib2.urlopen(url)
    f = open("/tmp/" + filename, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (filename, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,
    f.close()

# current version
def grab_current_version():
    url = "https://api.wordpress.org/core/version-check/1.1/"
    u = urllib2.urlopen(url).readlines()
    counter = 0
    for line in u:
        line = line.rstrip()
        counter = counter + 1
        if counter == 3:
            return line

# check for updates
def update_check():
    while 1:
        
        # grab the current version of wordpress
        current_version = grab_current_version()
        print "[*] The current version of Wordpress is: " + str(current_version)
        
        # check directories
        wp_path = check_config("BLOG_PATH=").split(",")
        update_counter = 0
        for paths in wp_path:    
            data = file("%s/wp-includes/version.php" % (paths), "r").readlines()
            for line in data:
                if "wp_version =" in line:
                        line = line.rstrip()
                        version = line.replace("$wp_version = '", "").replace("';", "")
                        print "[*] Your version of wordpress is: " + str(version) + " for installation located in: " + paths

            if current_version != version:
                print "[*] Upgrade detected. Performing upgrade now for %s." % (paths)
                if update_counter == 0:
                    print "[*] Downloading latest version of wordpress..."
                    download_file("https://wordpress.org/latest.zip", "latest.zip")
                    print "[*] Extracting file contents.."
                    os.chdir("/tmp")
                    subprocess.Popen("unzip /tmp/latest.zip", shell=True).wait()
                    os.chdir("/usr/share/wpupdate")
                    update_counter = 1

                # copy the files over
                subprocess.Popen("cp -rf /tmp/wordpress/* %s/" % (paths), shell=True).wait()
                print "[*] Fixing up permissions now..."
                subprocess.Popen("chown -R root:root %s/;chown -R www-data:www-data %s/wp-content/uploads/" % (paths,paths), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        else:
            print "[*] You are up to date! Waiting until 2am until next check."

        if os.path.isfile("/tmp/latest.zip"):
            subprocess.Popen("rm /tmp/latest.zip;rm -rf /tmp/wordpress", shell=True).wait()

        # sleep for at least a minute, 1 second
        time.sleep(61)
        # sleep until 2am
        t = datetime.datetime.today()
        future = datetime.datetime(t.year,t.month,t.day,2,0)
        if t.hour >= 2:
            future += datetime.timedelta(days=1)
        print "WPUpdate is now sleeping for another: " + str(future-t)
        time.sleep((future-t).seconds)
