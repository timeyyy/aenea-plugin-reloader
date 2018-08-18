"""
 This file pushes from the server to a shared directory
"""
from yapsy.IPlugin import IPlugin

import os
from os.path import join, expanduser
import shutil
import shlex
import subprocess
import sys

import config


enabled = True

# HERE = os.path.dirname(__file__)
# PROJECT_BASE = os.path.abspath(join(os.pardir, os.pardir, os.pardir, HERE))
# home = expanduser("~")
# shared_folder = "VirtualBox VMs/shared-folder/"
# macro_directory = "aenea_macros"
# SRC = join(PROJECT_BASE, "client", "my_macros")
# TO = join(home, shared_folder, macro_directory)
# SRC = config.APR_CLIENT_PLUGIN_SRC_PATTER
TO = config.APR_SERVER_SHARED_DIR


def notify(header, body=None):
    from gi.repository import Notify
    # One time initialization of libnotify
    Notify.init("sync aenea grammar files")

    notification = Notify.Notification.new(header, body)
    notification.show()

def push_macros_to_shared():
    print TO
    print os.path.exists(TO)
    assert os.path.exists(TO)

    print(os.getcwd())

    cmd = ["/usr/bin/find"]
    cmd.extend(config.APR_CLIENT_MACRO_SRC_PATTERN)

    # Will error if code is not 0
    subprocess.check_call(cmd)
    header = "Aenea Macro Sync"
    body = "rsync: server -> shared dir finished."
    notify(header, body)


def update_server_plugins():
    cmd = ["/usr/bin/find"]
    cmd.extend(config.APR_SERVER_PLUGIN_SRC_PATTERN)

    # Will error if code is not 0
    subprocess.check_call(cmd)
    header = "Aenea Server Plugin Refresh"
    body = "Server plugins collected and refreshed!"
    notify(header, body)

    # Now restart the server
    # import aenea.communications
    # aenea.communications.shutdown_server()
    # restart_cmd = "/bin/sleep 1; ./cmds.py start-server"
    # subprocess.Popen(restart_cmd, shell=True)
    # sys.exit()


def client_finished_macro_reload():
    # Will error if code is not 0
    header = "Aenea Macro sync "
    body = "sync shared dir -> client. (client restarting...)"
    notify(header, body)


def shutdown_server():
    sys.exit()


class ReloadMacrosPlugin(IPlugin):
    def register_rpcs(self, server):
        server.register_function(push_macros_to_shared)
        server.register_function(update_server_plugins)
        server.register_function(client_finished_macro_reload)


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1]
    if cmd == "sync_server_plugins":
        update_server_plugins()
    elif cmd == "sync_client_macros":
        push_macros_to_shared()
    else:
        print("bad command:", cmd)
        sys.exit(1)
