from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


def test_ntp(Service):
    assert Service('systemd-timesyncd').is_running or Service(
        'ntpd').is_running or Service('openntpd').is_running
    try:
        Service('systemd-timesyncd').is_enabled or Service(
            'ntpd').is_enabled or Service('openntpd').is_enabled
    except NotImplementedError:
        pass
