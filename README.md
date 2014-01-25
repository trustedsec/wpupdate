WPUpdate is a simple update script that will automatically update your wordpress installation when a new release is out. It does this by storing a copy of the latest zip under /usr/share/wpupdate/database/latest.zip. Every morning at 2AM, it will download a new zip file, do a hash compare to see if any changes are made. If there are changes, it will automatically update Wordpress for you, lock down the permissions (except for the uploads folder).

### Features

1. Automatically check for updates once a day. This is through the /etc/init.d/wpupdate service.

2. If a new release is out, it'll automatically update Wordpress for you.

3. It will sleep until 2AM the next day, then check for an update again.


### Bugs and enhancements

For bug reports or enhancements, please open an issue here https://github.com/trustedsec/wpupdate/issues

### Project structure

For those technical folks you can find all of the code in the following structure:

- ```src/wpcore.py``` - main central code reuse for things shared between each module
- ```setup.py``` - copies files to ```/usr/share/wpupdate/``` then edits ```/etc/init.d/wpupdate``` to ensure wpupdate starts per each reboot

### Supported platforms

- Linux

### HOWTO Install

Simply run python setup.py, hit yes to install. Note that if your installation isn't /var/www/ you will need to edit the source code.

### Future Plans

Add a configuration option to modify /var/www, time to check, etc.
