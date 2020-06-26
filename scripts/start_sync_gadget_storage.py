#!/usr/bin/python3

import sys
import time
import logging

import storage
import configfs

TIME_OUT = 60


def _main():

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.info(f'Started mass storage gadget synchronizer')

    configfs.clean()
    configfs.define()
    logger.info(f'Defined zero gadget with mass storage')

    storage.mount()
    logger.info(f'Mounted storage "{storage.WATCH_PATH}"')

    try:
        while True:
            storage.sync()
            logger.debug(f'Storage synch 1 "{storage.WATCH_PATH}" for update')
            time.sleep(1)

            storage.umount()
            logger.debug(f'Storage unmounted "{storage.WATCH_PATH}" for update')
            time.sleep(1)

            storage.sync()
            logger.debug(f'Storage synch 2 "{storage.WATCH_PATH}" for update')
            time.sleep(1)

            storage.mount()
            logger.debug(f'Storage mounted "{storage.WATCH_PATH}" for update')

            logger.info(f'Synced storage "{storage.WATCH_PATH}" with mass storage')

            time.sleep(60)

    except KeyboardInterrupt:
        storage.sync()
        storage.umount()
        logger.info(f'Storage unmounted "{storage.WATCH_PATH}"')
        configfs.clean()
        logger.info(f'Cleaned mass storage gadget')

    return 0


if __name__ == "__main__":
    sys.exit(_main())

