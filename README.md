# simple_ansilbe_api

### ad-hoc
``` python
from simple_ansible_api.api import AnsiBleApi
from simple_ansible_api.task import Task

cli = AnsiBleApi(hosts_list=["192.168.0.108", "192.168.0.109"])
t1 = Task(cli, name="t1", register="root_dir")
t1.shell(cmd="ls /root", )
cli.ansible(hosts="192.168.0.107", name="test ad-hoc task")
```

### playbook
``` python
from simple_ansible_api.api import AnsiBleApi

cli = AnsiBleApi(hosts_list="/etc/ansible/hosts")
cli.ansible_playbook(playbooks=["test.yaml"])
```