def test_ntp(Service, Ansible):
    if Ansible('setup')['ansible_facts']['ansible_service_mgr'] == 'systemd':
        assert Service('systemd-timesyncd').is_running
    elif Ansible('setup')['ansible_facts']['ansible_os_family'] == 'Debian':
        assert Service('openntpd').is_running
    elif Ansible('setup')['ansible_facts']['ansible_os_family'] == 'OpenBSD':
        assert Service('ntpd').is_running
