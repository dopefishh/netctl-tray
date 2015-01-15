import subprocess
import sys
import re

netctl_root = '/etc/netctl'


def get_profiles():
    profiles = subprocess.check_output(['netctl', 'list'])
    for profile in profiles.splitlines():
        profile = profile.decode(sys.getdefaultencoding())
        cp = {}
        cp['name'] = profile[2:].strip()
        cp['active'] = profile.startswith('*')
        cp['file'] = '{}/{}'.format(netctl_root, cp['name'])
        with open(cp['file'], 'r') as f:
            for line in f:
                interface = re.match('Interface=(?P<int>.*)', f.read())
                if interface:
                    cp['interface'] = interface.group('int')
                    break
            else:
                cp['interface'] = 'undetected'
        yield cp


def start_profile(profile):
    print('start: ', profile)


def end_profile(profile):
    print('end: ', profile)
