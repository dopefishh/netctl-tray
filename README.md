Netctltray version 0.2
======================
Netctltray is an application that provides a system tray icon for the netctl
network manager. Via the system icon you can change profile and get query the
status of the current connection.

### Requirements
- [Python3](http://www.python.org/downloads/)
- [PySide] (http://qt-project.org/wiki/PySide)
- [sudo] (http://www.sudo.ws)

#### Setup on a debian based system

	# apt-get install sudo python3 python3-pyside

#### Setup on a pacman based system

	# pacman -S sudo python python-pyside

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
