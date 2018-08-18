"""
    This file tells the server to to push to a shared directory,
    We then reload our macros from this shared directory
"""
import os
from os.path import join, expanduser

from dirsync import sync
import dragonfly
import aenea.communications

from _aenea import reload_code


shared_directory = r"E:\\"
macro_directory = "aenea_macros"


def reload_macros_from_server():
    # Tell the server to sync to the shared folder
    print "Starting sync to shared folder"
    aenea.communications.server.push_macros_to_shared()

    FROM = join(shared_directory, macro_directory)
    TO = r"C:\NatLink\NatLink\MacroSystem"
    assert os.path.exists(FROM)
    assert os.path.exists(TO)

    print "Starting sync to natlink macro folder"
    result = sync(FROM, TO, 'sync')
    print result

    # This has to happen before reload_code(), client goes down...
    aenea.communications.server.client_finished_macro_reload()
    print "Reload Natlink..."
    reload_code()


def reload_server_plugins():
    print "Telling server to reload plugins"
    aenea.communications.server.update_server_plugins()

class ReloadMacros(dragonfly.MappingRule):
    mapping = {
        'reload macros from server': dragonfly.Function(reload_macros_from_server),
        'reload server plugins': dragonfly.Function(reload_server_plugins),
        }

grammar = dragonfly.Grammar('tim reload shared dir macros')

grammar.add_rule(ReloadMacros())

grammar.load()


def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
