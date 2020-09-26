from simple_ansible_api.api import AnsiBleApi
from simple_ansible_api.callback import ResultsResultCallBack


def v1():
    cli = AnsiBleApi(hosts_list="/etc/ansible/hosts")
    # set custom callback object
    cli.set_callback(callback=ResultsResultCallBack())
    cli.ansible_playbook(playbooks=["test.yaml"])
    ret = cli.result(to_json=True)
    return ret


if __name__ == '__main__':
    r = v1()
    print(r)