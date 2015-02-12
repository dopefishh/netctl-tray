# Netctltray version 0.2
Netctltray is an application that provides a system tray icon for the netctl
network manager. Via the system icon you can change profile and get query the
status of the current connection.

### Installation
#### Requirements
Requirements with a \* are optional

- Python3 : Main programming language.
- PySide : Python interface to Qt.
- netctl : Network management.
- sudo\* : Default option for acquiring permissions to run netctl. Sudo will
	run with the ``-A`` flag that runs the password entry program in
	``$SUDO_ASKPASS``
- x11-ssh-askpass\* : Default option for querying the sudo password.

sudo and x11-ssh-askpass are needed when the user can not run the netctl
commands and 

#### Installation

	# pacman -S python python-pyside
	# pacman -S sudo x11-ssh-askpass

### Usage and setup
By default the command that runs netctl is prefixed with ``sudo -A``. This is
stored in the variable ``sudo_command``. This is done to not have to setup a
daemon to access netctl with root permission. To use ``sudo`` in combination
with ``ssh-askpass`` you can add 
``export SUDO_ASKPASS=/usr/lib/ssh/ssh-askpass`` to your ``~/.bashrc`` or
similar file. 

``netctl.py`` can also work with 
[flexible interfaces](https://wiki.archlinux.org/index.php/Netctl#Using_any_interface)
but it does this in a naive way. It runs the script and imports the
``$Interface`` variable. When an interface already has an active profile the
active profile will be stopped prior to the start of the new profile.

### Author(s)
-	Mart (mart@martlubbers.net).

### Changelog
- Version 0.2 (2015-02-12)

	- Rewritten menu.
	- Remove logging.
	- Added checkmark icon for active networks.
	- Added password question for network changes.

- Version 0.1 (2015-01-05)

	- Initial script.
	- README.md created.
