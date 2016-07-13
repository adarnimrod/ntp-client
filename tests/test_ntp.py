def test_ntp(Service, Ansible):
    if Ansible('setup')['ansible_facts']['ansible_service_mgr'] == 'systemd':
        service = Service('systemd-timesyncd')
    elif Ansible('setup')['ansible_facts']['ansible_os_family'] == 'Debian':
        service = Service('openntpd')
    elif Ansible('setup')['ansible_facts']['ansible_os_family'] == 'OpenBSD':
        service = Service('ntpd')
    assert service.is_running
    try:
        assert service.is_enabled
    except NotImplementedError:
        pass
