from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


def test_ntp_service(Service, SystemInfo):
    if SystemInfo.type == 'openbsd':
        service = Service('ntpd')
    elif SystemInfo.type == 'linux':
        if SystemInfo.codename in ['jessie', 'stretch', 'xenial']:
            service = Service('systemd-timesyncd')
        else:
            service = Service('openntpd')
    assert service.is_running
    try:
        assert service.is_enabled
    except NotImplementedError:
        pass


def test_ntp_config(SystemInfo, Command):
    if SystemInfo.type == 'openbsd' or (
            SystemInfo.type == 'linux' and
            SystemInfo.codename not in ['jessie', 'stretch', 'xenial']):
        command = Command('ntpd -n')
        assert command.rc == 0
        assert 'configuration OK' in command.stderr


def test_ntp_status(SystemInfo, Command):
    if SystemInfo.type == 'openbsd':
        assert Command('ntpctl -s status').rc == 0
        assert 'peers valid' in Command('ntpctl -s status').stdout
    elif SystemInfo.type == 'linux' and SystemInfo.codename in [
            'jessie', 'stretch', 'xenial'
    ]:
        command = Command('timedatectl status')
        assert command.rc == 0
        assert 'Network time on: yes' in command.stdout
