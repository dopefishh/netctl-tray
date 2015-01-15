from PySide import QtGui
import sys
import netctl


class NetworkAction(QtGui.QAction):
    """QAction wrapper that can start of stop a profile.

    Variables:
    tray      - Tray icon object.
    profile   - Representing profile.
    profiles  - List of all profiles.
    """
    def __init__(self, parent, tray, profile, profiles):
        super(NetworkAction, self).__init__(parent)
        self.tray = tray
        self.profile = profile
        self.profiles = profiles
        self.setText(profile['name'])
        self.setCheckable(True)
        self.setChecked(profile['active'])
        self.triggered.connect(self.sig_triggered)

    def sig_triggered(self):
        """Signal handler for activating the action. In practice this is
        starting or stopping the profile. When there is another profile active
        with the same interface it will be stopped."""
        if self.profile['active']:
            netctl.stop_profile(self.profile['name'], self.tray)
        else:
            concurents = [a for a in self.profiles if
                          a is not self.profile and
                          a['interface'] == self.profile['interface'] and
                          a['active']]
            for concurent in concurents:
                netctl.stop_profile(concurent['name'], self.tray)
            netctl.start_profile(self.profile['name'], self.tray)


class NetctlTray(QtGui.QSystemTrayIcon):
    """QSystemTrayIcon wrapper that control the system tray icon to interface
    with netctl.

    Variables:
    connect_menu - QMenu that contains the connections.
    """
    def __init__(self):
        super(NetctlTray, self).__init__()
        self.setIcon(QtGui.QIcon('icon.svg'))
        self.activated.connect(self.sig_activated)
        self.messageClicked.connect(self.sig_messageClicked)
        menu = QtGui.QMenu('Netctl-tray')

        self.connect_menu = menu.addMenu('Connect')

        about = menu.addAction('About')
        about.triggered.connect(self.sig_about)

        quit = menu.addAction('Exit')
        quit.triggered.connect(self.sig_exit)

        self.setContextMenu(menu)

    def updateMenu(self):
        """Update the menu according to netctl output and profile files."""
        self.connect_menu.clear()
        self.int_profs = {}
        profiles = sorted(netctl.get_profiles(), key=lambda x: x['interface'])
        for profile in profiles:
            if profile['interface'] not in self.int_profs:
                self.connect_menu.addSeparator()
                self.int_profs[profile['interface']] = []
            self.int_profs[profile['interface']].append(profile['name'])
            self.connect_menu.addAction(
                NetworkAction(self.connect_menu, self, profile, profiles))

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
        elif reason == QtGui.QSystemTrayIcon.Click:
            self.showMessage(
                'Current connection',
                'connected to: blablabla',
                QtGui.QSystemTrayIcon.NoIcon, msecs=5000)

    def sig_messageClicked(self):
        """Signal handler for clicking the status popup. When this happens a
        1ms empty popup will be shown to clear the current popup."""
        self.showMessage('', '', msecs=1)

    def sig_exit(self):
        """Signal handler for the exit button in the main menu. When this
        happens the program quits."""
        sys.exit()

    def sig_about(self):
        """Signal handler for the about button in the main menu. When this
        happens the program shows a dialog box containing the about info."""
        QtGui.QMessageBox.information(
            None,
            'About',
            'This is an about window',
            QtGui.QMessageBox.Close)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    icon = NetctlTray()
    icon.setVisible(True)
    icon.show()
    sys.exit(app.exec_())
