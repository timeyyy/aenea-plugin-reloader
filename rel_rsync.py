#!/usr/bin/python

import subprocess
import sys


def rsync(file_path_with_rel_symbol, dst):
    src = file_path_with_rel_symbol

    cmd = ["/usr/bin/rsync"]
    cmd.extend(["--prune-empty-dirs", "--relative", src, dst])

    # Will error if code is not 0
    subprocess.check_call(cmd)


def main():
    """
    does a relative rsync after the folder matching var rel_from
    """
    file_path = sys.argv[1]
    rel_from = sys.argv[2]
    destination = sys.argv[3]

    after = file_path.index(rel_from) + len(rel_from)
    rsync_rel_symbol = "/."
    new_file_path = file_path[:after] + rsync_rel_symbol + file_path[after:]
    rsync(new_file_path, destination)

    sys.exit(0)


if __name__ == "__main__":
    main()


