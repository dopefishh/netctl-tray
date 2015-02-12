#!/usr/bin/env python

from PySide import QtGui
import shlex
import sys
import netctl
import argparse
import os

VERSION = '0.2'


class NetworkAction(QtGui.QAction):
    """QAction wrapper that can start of stop a profile.

    Variables:
    tray      - Tray icon object.
    profile   - Representing profile.
    profiles  - List of all profiles.
    """
    def __init__(self, tray, profile, profiles):
        super(NetworkAction, self).__init__(tray.contextMenu())
        self.tray = tray
        self.profile = profile
        self.profiles = profiles
        self.setText(profile['name'])
        if profile['active']:
            self.setIcon(tray.activenetwork)
        self.triggered.connect(self.sig_triggered)

    def sig_triggered(self):
        """Signal handler for activating the action. In practice this is
        starting or stopping the profile. When there is another profile active
        with the same interface it will be stopped."""
        if self.profile['active']:
            netctl.startstop_profile(self.profile['name'], False)
        else:
            concurents = [a for a in self.profiles if
                          a is not self.profile and
                          a['interface'] == self.profile['interface'] and
                          a['active']]
            for concurent in concurents:
                netctl.startstop_profile(concurent['name'], False)
            netctl.startstop_profile(self.profile['name'], True)
        self.tray.show_status()


class NetctlTray(QtGui.QSystemTrayIcon):
    """QSystemTrayIcon wrapper that control the system tray icon to interface
    with netctl.

    Variables:
    connect_menu - QMenu that contains the connections.
    """
    def __init__(self):
        super(NetctlTray, self).__init__()
        path = '/opt/netctltray/'
        self.activenetwork = QtGui.QIcon('{}/check.svg'.format(path))
        self.setIcon(QtGui.QIcon('{}/icon.svg'.format(path)))
        self.activated.connect(self.sig_activated)
        self.messageClicked.connect(self.sig_messageClicked)
        self.setContextMenu(QtGui.QMenu('Netctl-tray'))
        self.updateMenu()

    def updateMenu(self):
        """Update the menu according to netctl output and profile files."""
        self.contextMenu().clear()
        self.contextMenu().addSeparator()
        previous_interface = ''
        profs = sorted(netctl.get_profiles(), key=lambda x: x['interface'])
        last = None
        for p in profs:
            if p['interface'] != previous_interface:
                last = QtGui.QMenu(p['interface'])
                self.contextMenu().addMenu(last)
                previous_interface = p['interface']
            last.addAction(NetworkAction(self, p, profs))
        self.contextMenu().addAction('Exit').triggered.connect(self.sig_exit)

    def show_status(self):
        """Show the status of the connections"""
        status = list(netctl.get_statussus())
        status = '\n'.join(status) if status else 'No profiles active'
        self.showMessage('Current connection(s)', status,
                         QtGui.QSystemTrayIcon.NoIcon, msecs=5000)

    def sig_activated(self, reason):
        """Signal handler for clicking the tray icon.

        Arguments:
        Reason - QSystemTrayIcon.Reason:
            RightClick - Spawn the menu.
            LeftClick  - Show the status.
            Other      - Do nothing.
        """
        if reason == QtGui.QSystemTrayIcon.Context:
            self.updateMenu()
            self.contextMenu().popup(self.geometry().topLeft())
        elif reason == QtGui.QSystemTrayIcon.Trigger:
            self.show_status()

    def sig_messageClicked(self):
        """Signal handler for clicking the status popup. When this happens a
        1ms empty popup will be shown to clear the current popup."""
        self.showMessage('', '', msecs=1)

    def sig_exit(self):
        """Signal handler for the exit button in the main menu. When this
        happens the program quits."""
        sys.exit()


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Netctl profile switcher')
    parser.add_argument('--version', action='store_true',
                        help='Show the version')
    parser.add_argument('-6', '--ipv6', action='store_true',
                        help='Prefer ipv6 over ipv4 when showing the status.')
    parser.add_argument('-S', '--sudo', action='store',
                        help='Use the command SUDO for getting root permission'
                        's. By default this is command is "sudo -A" and it ass'
                        'umes that you have set the SUDO_ASKPASS environment v'
                        'ariable. It is tested with "ssh-askpass" as askpass p'
                        'rogram.')
    parser.add_argument('-N', '--netctl', action='store',
                        help='Location of the netctl binary. By default this i'
                        's just "netctl" and thus assumes it to be in $PATH.')
    parser.add_argument('-R', '--nroot', action='store',
                        help='Root of the netctl configuration directory. By d'
                        'efault this is "/etc/netctl".')
    namespace = vars(parser.parse_args())
    if namespace['version']:
        sys.stdout.write(VERSION + '\n')
        sys.exit()
    if namespace['ipv6']:
        netctl.prefer_ipv6 = True
    if namespace['sudo']:
        netctl.sudo_command = shlex.split(namespace['sudo'])
    if namespace['netctl']:
        netctl.netctl_command = namespace['netctl']
    if namespace['nroot']:
        netctl.netctl_root = namespace['nroot']

    app = QtGui.QApplication(sys.argv)

    icon = NetctlTray()
    icon.setVisible(True)
    icon.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
