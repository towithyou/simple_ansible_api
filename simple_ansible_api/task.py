# use `ansible-doc -s module_name` command query more parameters


class Task:
    def __init__(self, cli, **kwargs):
        self._cli = cli
        self._extend_params = kwargs

    def debug(self, msg, **kwargs):
        args = {
            "msg": msg
        }
        self._set_task("debug", args, **kwargs)

    def shell(self, cmd, **kwargs):
        args = {
            "cmd": cmd
        }
        self._set_task("shell", args, **kwargs)

    def ping(self):
        self._set_task("ping", None)

    def file(self, path, state, mode="0644", **kwargs):
        args = {
            "path": path,
            "state": state,
            "mode": mode,
        }
        self._set_task("file", args, **kwargs)

    def copy(self, src, dest, **kwargs):
        args = {
            "src": src,
            "dest": dest
        }
        self._set_task("copy", args, **kwargs)

    def stat(self, path, **kwargs):
        args = {
            "path": path
        }
        self._set_task("stat", args, **kwargs)

    def cron(self, job, name, **kwargs):
        args = {
            "job": job,
            "name": name
        }
        self._set_task("cron", args, **kwargs)

    def user(self, name, shell="/bin/bash", **kwargs):
        args = {
            "name": name,
            "shell": shell
        }
        self._set_task("user", args, **kwargs)

    def apt(self, name, state, **kwargs):
        args = {
            "name": name,
            "state": state
        }
        self._set_task("apt", args, **kwargs)

    def yum(self, name, state, **kwargs):
        args = {
            "name": name,
            "state": state
        }
        self._set_task("yum", args, **kwargs)

    def service(self, name, state, enabled="yes", **kwargs):
        args = {
            "name": name,
            "state": state,
            "enabled": enabled,
        }
        self._set_task("service", args, **kwargs)

    def script(self, executable, **kwargs):
        args = {
            "executable": executable
        }
        self._set_task("script", args, **kwargs)

    def supervisorctl(self, name, state, config, **kwargs):
        args = {
            "name": name,
            "state": state,
            "config": config
        }
        self._set_task("supervisorctl", args, **kwargs)

    def _set_task(self, module, args, **kwargs):
        if args:
            args.update(kwargs)
        self._cli.set_task(module=module, args=args, **self._extend_params)
