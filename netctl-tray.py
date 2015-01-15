from PySide import QtGui
import sys
import subprocess


def get_profiles():
    profiles = subprocess.check_output(['netctl', 'list'])
    actives = []
    passives = []
    for profile in profiles.splitlines():
        profile = profile.decode(sys.getdefaultencoding())
        if profile.startswith('*'):
            actives.append(profile[2:].strip())
        elif profile:
            passives.append(profile.strip())
    return actives, passives


def start_profile(profile):
    pass


def end_profile(profile):
    pass


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
        actives, passives = get_profiles()
        for active in actives:
            active = self.connect_menu.addAction(active)
            active.setCheckable(True)
            active.setChecked(True)
        for passive in passives:
            passive = self.connect_menu.addAction(passive)
            passive.setCheckable(True)
            passive.setChecked(False)

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
