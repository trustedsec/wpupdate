WPUpdate is a simple update script that will automatically update your wordpress installation when a new release is out.  It does this by doing a compare on Wordpresses update API on their website then doing a comparison under wp-includes/version.php. From there, it will determine if changes are needed and an update. After that it will automatically update wordpress, set the permissions to be restricted to only root:root for security reasons (except uploads). After that, it'll check again at 2AM.

### Features

1. Automatically check for updates once a day. This is through the /etc/init.d/wpupdate service.

2. If a new release is out, it'll automatically update Wordpress for you.

3. It will sleep until 2AM the next day, then check for an update again.

4. Allows for multiple wordpress installations, simply edit the config file located under /usr/share/wpupdate/config and add /var/www/blog1,/var/www/blog2 for multiple blogs.

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

- Add support for plugin updates
