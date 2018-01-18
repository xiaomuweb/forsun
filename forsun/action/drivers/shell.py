# -*- coding: utf-8 -*-
# 15/6/27
# create by: snower

import os
import time
import subprocess
import shlex
import threading
import json
import logging
from tornado import gen
from ..action import Action, ExecuteActionError

class ShellAction(Action):
    def __init__(self, *args, **kwargs):
        super(ShellAction, self).__init__(*args, **kwargs)

        self.start_time = time.time()

    @classmethod
    def init(cls):
        pass

    @gen.coroutine
    def execute(self, *args, **kwargs):
        if not self.params:
            raise ExecuteActionError("cmd is empty")

        cmd = self.params.get("cmd", 'ls .')
        cwd = self.params.get('cwd', None)
        env = {}
        if self.params.get("env", ""):
            for e in self.params.get("env", "").split(";"):
                if e:
                    for k in e.split("="):
                        env[k[0]] = k[1]

        env["FORSUN_TIMESTAMP"] = str(self.ts)

        subprocess.Popen(shlex.split(cmd), shell=True, close_fds=True, cwd = cwd, env=env)
        logging.debug("shell action %s %.2fms", cmd, (time.time() - self.start_time) * 1000)