# simple_ansilbe_api

### How to install
``` bash
pip install simple-ansible-api
```

### ad-hoc
``` python
from simple_ansible_api.api import AnsiBleApi
from simple_ansible_api.task import Task

# 初始化， api 实例
cli = AnsiBleApi(hosts_list=["192.168.0.108", "192.168.0.109"])

# 针对 api 实例，创建一个task, 可以指定task 相关属性
t1 = Task(cli, name="task name 1", register="addr")
#指定 shell 模块，不同模块参数不同 参考 `ansible-doc -s module_name` 获取更多参数
t1.shell(cmd="ifconfig", ) 

t2 = Task(cli, name="task name 2")
t2.debug(msg="{{addr}}")

# 定义一个playbook，并指定hosts, 参数， 更多参数可以参考playbook yaml
cli.ansible(hosts="192.168.0.107", name="playbook name"， 
            gather_facts="no")

```

``` yaml
- name:  playbook name
  gather_facts: no
  hosts: "192.168.0.107"
  tasks:
  - name: task name 1
    shell: ifconfig
    register: addr
  - name: task name 2
    debug: msg="{{addr}}"
```

### playbook
``` python
from simple_ansible_api.api import AnsiBleApi

cli = AnsiBleApi(hosts_list="/etc/ansible/hosts")
cli.ansible_playbook(playbooks=["test.yaml"])
```

### 结果回调
``` python 
from simple_ansible_api.callback import ResultsResultCallBack

# 自定义回调函数， 可以获取到执行结果。
cli = AnsiBleApi(hosts_list="/etc/ansible/hosts")
# set custom callback object
cli.set_callback(callback=ResultsResultCallBack())
```