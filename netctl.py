from PySide import QtGui
import subprocess
import sys

netctl_root = '/etc/netctl'


def get_profiles():
    """Give the current profiles registered with netctl.

    Yields:
        Dictionary for every profile containing at least the keys:
        active    - Boolean that shows if the profile is currently in use.
        file      - String containing the profile file location.
        interface - String containing the interface name.
        name      - String containing the name of the profile.
    """

    profiles = subprocess.check_output(['netctl', 'list'])
    for profile in profiles.splitlines():
        profile = profile.decode(sys.getdefaultencoding())
        cp = {'name': profile[2:].strip(), 'active': profile.startswith('*')}
        cp['file'] = '{}/{}'.format(netctl_root, cp['name'])
        with open(cp['file'], 'r') as f:
            for line in f:
                if line.startswith('Interface='):
                    cp['interface'] = line[10:]
                    break
            else:
                cp['interface'] = 'undetected'
        yield cp


def start_profile(profile, notify=None):
    """Starts a profile and optionally notifies the progress.

    Arguments:
    profile - String containing the name of the profile.
    """
    if notify:
        notify.showMessage(
            '', 'Starting {}...'.format(profile),
            QtGui.QSystemTrayIcon.NoIcon, msecs=5000)


def stop_profile(profile, notify=None):
    """Stops a profile and optionally notifies the progress.

    Arguments:
    profile - String containing the name of the profile.
    """
    if notify:
        notify.showMessage(
            '', 'Stopping {}...'.format(profile),
            QtGui.QSystemTrayIcon.NoIcon, msecs=5000)
