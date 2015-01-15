from PySide import QtGui
import sys
import netctl


class NetctlTray(QtGui.QSystemTrayIcon):
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
        self.connect_menu.clear()
        self.int_profs = {}
        profiles = sorted(netctl.get_profiles(), key=lambda x: x['interface'])
        for profile in profiles:
            if profile['interface'] not in self.int_profs:
                self.connect_menu.addSeparator()
                self.int_profs[profile['interface']] = []
            self.int_profs[profile['interface']].append(profile['name'])
            item = self.connect_menu.addAction(profile['name'])
            item.setCheckable(True)
            if profile['active']:
                item.setChecked(True)
            item.triggered.connect

    def sig_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.Unknown:
            print('Unknown trigger')
        elif reason == QtGui.QSystemTrayIcon.Context:
            self.updateMenu()
            self.contextMenu().popup(self.geometry().topLeft())
        elif reason == QtGui.QSystemTrayIcon.DoubleClick:
            pass
        else:
            self.showMessage(
                'Current connection',
                'connected to: blablabla',
                QtGui.QSystemTrayIcon.NoIcon, msecs=5000)

    def sig_messageClicked(self):
        self.showMessage('', '', msecs=1)

    def sig_exit(self):
        sys.exit()

    def sig_about(self):
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
