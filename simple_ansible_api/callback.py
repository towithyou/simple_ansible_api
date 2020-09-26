from ansible.plugins.callback import CallbackBase


class ResultsResultCallBack(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultsResultCallBack, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self._load_data(result, self.host_unreachable)

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self._load_data(result, self.host_ok)

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self._load_data(result, self.host_failed)

    def _load_data(self, result, container):
        host_name = self.get_host(result)
        result = self.get_result(result)

        if container.get(host_name):
            container[host_name].append(result)
        else:
            container[host_name] = [result]

    @classmethod
    def get_result(cls, r):
        return r._result

    @classmethod
    def get_host(cls, r):
        return r._host.get_name()

    @classmethod
    def get_task(cls, r):
        return r._task

    def result(self):
        result_raw = {'success': {}, 'failed': {}, 'unreachable': {}}

        for host, result in self.host_ok.items():
            result_raw['success'][host] = result
        for host, result in self.host_failed.items():
            result_raw['failed'][host] = result
        for host, result in self.host_unreachable.items():
            result_raw['unreachable'][host] = result

        return result_raw