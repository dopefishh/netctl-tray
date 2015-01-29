import subprocess
import sys


netctl_command = 'netctl'      # Netctl command
netctl_root = '/etc/netctl'    # Root of the netctl configuration files
prefer_ipv6 = False            # Flag to print ipv6 address over ipv4
sudo_command = ['sudo', '-A']  # Sudo command to have a graphical sudo


def get_real_interface(interface):
    """Translate virtual interface to a physical interface if it wasn't already
    a physical interface.

    interface - Name of the interface.
    """
    query = 'source {}/interfaces/{} 1>/dev/null 2>&1; echo $Interface'.format(
        netctl_root, interface)
    return subprocess.check_output(['bash', '-c', query]).decode(
        sys.getdefaultencoding()).strip() or interface


def startstop_profile(profile, start):
    """Start or stop a profile.

    profile - String containing the name of the profile.
    start   - Flag for starting, if False the profile will be stopped.
    """
    cmd = 'start' if start else 'stop'
    return subprocess.call(sudo_command + [netctl_command, cmd, profile])


def get_profiles():
    """Give the current profiles registered with netctl.

    Yields dictionary for every profile containing at least the keys:
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
                    iface = line[10:].strip()
                    cp['interface'] = get_real_interface(iface)
                    break
            else:
                cp['interface'] = None
        yield cp


def get_statussus():
    """Give the statusses of the active connections.

    Yields string for every active status.
    """
    for prof in (x for x in get_profiles() if x['active'] and x['interface']):
        ips = {}
        ip = subprocess.check_output([
            'ip', 'addr', 'show', prof['interface']]).decode(
                sys.getdefaultencoding())
        ip = (x.strip() for x in ip.split('\n'))
        for ent in (x for x in ip if x.startswith('inet')):
            splits = ent.split()[:2]
            ips[splits[0]] = splits[1]
        ip = ips['inet6'] if prefer_ipv6 and 'inet6' in ips else ips['inet']
        yield '{}: {}'.format(prof['name'], ip)
