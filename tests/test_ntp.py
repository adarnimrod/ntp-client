from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


def test_ntp(Service, SystemInfo):
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
