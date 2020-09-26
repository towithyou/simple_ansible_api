import json
import shutil

import ansible.constants as C
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.vars.manager import VariableManager
from ansible import context


class AnsiBleApi:
    def __init__(self,
                 connection="smart",
                 module_path=None,
                 remote_user="root",
                 forks=10,
                 become=None,
                 become_method=None,
                 become_user=None,
                 check=False,
                 diff=False,
                 hosts_list=None,
                 verbosity=0,
                 syntax=None,
                 start_at_task=None,
                 results_call_back=None,
                 *args,
                 **kwargs,
                 ):

        context.CLIARGS = ImmutableDict(
            connection=connection,
            module_path=module_path,
            remote_user=remote_user,
            forks=forks,
            become=become,
            become_method=become_method,
            become_user=become_user,
            check=check,
            diff=diff,
            syntax=syntax,
            start_at_task=start_at_task,
            verbosity=verbosity,
            *args,
            **kwargs
        )
        self.forks = forks
        self.sources = hosts_list
        self.results_callback = results_call_back
        self.loader = DataLoader()

        def _(host):
            if isinstance(host, str):
                pass
            elif isinstance(host, list):
                s = ','.join(host)  #
                if len(host) == 1:
                    s += ','
                host = s
            return host

        self._host_format = _

        self.inventory = InventoryManager(loader=self.loader,
                                          sources=self._host_format(self.sources))
        self.variable_manager = VariableManager(loader=self.loader,
                                                inventory=self.inventory)
        self._play_source_template = {
            "name": "",
            "hosts": "",
            "gather_facts": "",
            "tasks": [],
        }

    def _play(self, play_source):
        var = play_source.pop("vars")
        return Play().load(play_source,
                           variable_manager=self.variable_manager,
                           loader=self.loader,
                           vars=var
                           )

    def _tqm(self):
        return TaskQueueManager(
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            forks=self.forks,
            passwords=None,
            stdout_callback=self.results_callback,
        )

    def set_task(self, module="shell", args=None, **kwargs):
        task = {
            "action": {"module": module, "args": args}
        }
        task.update(kwargs)

        self._play_source_template["tasks"].append(task)

    def set_callback(self, callback=None):
        self.results_callback = callback

    def ansible(self, hosts, name="task name", gather_facts="no", var=None):
        if isinstance(hosts, list):
            hosts = self._host_format(hosts)

        self._play_source_template["name"] = name
        self._play_source_template["hosts"] = hosts
        self._play_source_template["vars"] = var
        self._play_source_template["gather_facts"] = gather_facts

        print("AD-HOC DEBUG", self._play_source_template)

        play = self._play(self._play_source_template)
        tqm = self._tqm()
        try:
            tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
            if self.loader:
                self.loader.cleanup_all_tmp_files()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def ansible_playbook(self, playbooks):
        pb = playbooks if isinstance(playbooks, list) else [playbooks]
        playbook = PlaybookExecutor(playbooks=pb,  # 注意这里是一个列表
                                    inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader,
                                    passwords=dict(vault_pass=None))
        playbook._tqm = self._tqm()
        print("Playbook DEBUG", pb)
        playbook.run()

    def result(self, to_json=False):
        result_raw = None
        if self.results_callback is None:
            return result_raw
        else:
            result_raw = self.results_callback.result()

        if to_json:
            return json.dumps(result_raw, indent=4)
        else:
            return result_raw
