

# Two commands

'reload macros from server'

'reload server plugins': Not yet finished (doesn't do server restart)

# Setup

1. the rel_rsync.py needs to be exectuable. It can be used to help move found files.., useful on the server.

rel_rsync 'home/client/test/file.py' 'client' 'dest/'

will result in files rsynced to -> dest/test/file.py

Note: 'client' is a python regex pattern

2. on client `pip install dirsync`
