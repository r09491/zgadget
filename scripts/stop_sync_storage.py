#!/usr/bin/python3

import sys
import time
import logging

import storage
import configfs

def _main():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()

    storage.mount()
    time.sleep(1)
    storage.sync()
    time.sleep(1)
    storage.umount()
    configfs.clean()

    return 0


if __name__ == "__main__":
    sys.exit(_main())

