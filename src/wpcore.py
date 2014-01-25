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

# quick progress bar downloader
def download_file(url,filename):
    u = urllib2.urlopen(url)
    f = open("database/" + filename, 'wb')
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

# check for updates
def update_check():
    while 1:

        # if we don't already have a baseline, grab it
        if not os.path.isfile("/usr/share/wpupdate/database/latest.zip"):
            if not os.path.isfile("wpupdate.py"):
                os.chdir("/usr/share/wpupdate")
            download_file("https://wordpress.org/latest.zip", "latest.zip")
            print "[*] Updating Wordpress right now for the first time..."
            subprocess.Popen("cp database/latest.zip /tmp", shell=True).wait()
            os.chdir("/tmp") 
            subprocess.Popen("unzip latest.zip;cp -rf wordpress/* /var/www", shell=True).wait()
            print "[*] Fixing permissions, allowing www-data:www-data in uploads only."
            subprocess.Popen("chown -R root:root /var/www/*;chown -R www-data:www-data /var/www/wp-content/uploads", shell=True).wait()
            os.chdir("/usr/share/wpupdate")
            # clean up
            subprocess.Popen("rm -rf /tmp/wordpress;rm -rf /tmp/latest.zip", shell=True).wait()

        # store the hash of the latest wordpress in memory
        fileopen1 = file("/usr/share/wpupdate/database/latest.zip", "rb")
        data1 = fileopen1.read()
        hash = hashlib.sha512()
        hash.update(data1)
        hash1 = hash.hexdigest()

        # grab the latest and compare
        download_file("http://wordpress.org/latest.zip", "check.zip")
        fileopen2 = file("/usr/share/wpupdate/database/check.zip")
        print "[*] Comparing the database now...."
        data2 = fileopen2.read()
        hash = hashlib.sha512()
        hash.update(data2)
        hash2 = hash.hexdigest()

        # time to update
        if hash1 != hash2:
            print "[!] New version of Wordpress detected, updating to the latest for you.."
            subprocess.Popen("copy database/check.zip /tmp;mv database/check.zip database/latest.zip", shell=True).wait()
            print "Updating Wordpress right now..."
            os.chdir("/tmp")
            subprocess.Popen("unzip check.zip;cp -rf wordpress/* /var/www/", shell=True).wait()
            print "[*] Fixing permissions, allowing www-data:www-data in uploads only."
            subprocess.Popen("chown -R root:root /var/www/*;chown -R www-data:www-data /var/wwp-contents/uploads", shell=True).wait()
            print "[*] Wordpress update complete! Updating again at the same time, same place."
            # cleanup
            subprocess.Popen("rm -rf /tmp/check.zip;rm -rf /tmp/wordpress", shell=True).wait()

        else:
            print "No updates needed! We will now sleep for 61 seconds before starting counter.."

        os.remove("/usr/share/wpupdate/database/check.zip")

        # sleep for at least a minute, 1 second
        time.sleep(61)
        # sleep until 2am
        t = datetime.datetime.today()
        future = datetime.datetime(t.year,t.month,t.day,2,0)
        if t.hour >= 2:
            future += datetime.timedelta(days=1)
        print "Okay, WPUpdate is now sleeping for another: " + str(future-t)
        time.sleep((future-t).seconds)

