import subprocess


WATCH_PATH = '/media/gadget'

_CMD_MOUNT = ['/bin/mount', WATCH_PATH]
_CMD_UNMOUNT = ['/bin/umount', WATCH_PATH]
_CMD_SYNC = ['/bin/sync']


def mount():
    return subprocess.call(_CMD_MOUNT, stderr=subprocess.DEVNULL) ## 0 -> OK
    
def umount():
    return subprocess.call(_CMD_UNMOUNT, stderr=subprocess.DEVNULL) ## 0 -> OK

    
def sync():
    return subprocess.call(_CMD_SYNC, stderr=subprocess.DEVNULL) ## 0 -> OK
