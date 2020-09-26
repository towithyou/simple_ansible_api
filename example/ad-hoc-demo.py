from simple_ansible_api.api import AnsiBleApi
from simple_ansible_api.task import Task
from simple_ansible_api.callback import ResultsResultCallBack


def v1():
    cli = AnsiBleApi(hosts_list="/etc/ansible/hosts")
    # set custom callback object
    # cli.set_callback(callback=ResultsResultCallBack())

    t1 = Task(cli, name="t1", register="root_dir")
    t1.shell(cmd="ls /root", )

    t2 = Task(cli, name="t2")
    t2.debug("{{root_dir.stdout_lines}}")

    t3 = Task(cli, name="t3")
    t3.debug("{{src}}")  # Var parameter definition

    t4 = Task(cli, name="t4")
    t4.debug("{{dest}}")  # Var parameter definition

    t5 = Task(cli, name="t5")
    t5.yum(name="tree", state="latest")

    t6 = Task(cli, name="t6")
    t6.copy(src="{{src}}", dest="{{dest}}")

    t7 = Task(cli, name="t7")
    t7.file(path="/tmp/example_dir", state="directory")

    cli.ansible(hosts=["web", "db", "mongo"], var={"src": "/root/install.log", "dest": "/tmp/"},
                name="test ad-hoc task")


def v2():
    cli = AnsiBleApi(hosts_list=["192.168.0.107", "192.168.0.108", "192.168.0.109"])
    t1 = Task(cli, name="t1", register="root_dir")
    t1.shell(cmd="ls /root", )
    t2 = Task(cli, name="t2")
    t2.debug("{{root_dir.stdout_lines}}")

    cli.ansible(hosts="192.168.0.107", name="test ad-hoc task")
    # cli.ansible(hosts=["192.168.0.108", "192.168.0.109"], name="test ad-hoc task")


if __name__ == '__main__':
    # v1()
    v2()