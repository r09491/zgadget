#Raspberry Zero USB gadget with ethernet and and mass storage

Per default the Raspberry Zero runs in host mode as any other member
of the Raspberry family.  A OTG cable is connected to to inner USB
port and it controls USB devices like webcams or Usb sticks for
excample.

The Zero can be setup to run as an USB device. Then it may provide some
services to a connected host. In this case ethernet over USB and a mass
storage.

## Setup with *configfs*

* In */boot/config.txt* append
```
dtoverlay=dwc2
```

* In */etc/modules* append
```
dwc2
libcomposite
```

* Clone the repository with
```
/var $ git clone https://github.com/r09491/zgadget.git
```

* In the *storage* directory create the FAT image to be mounted as a loop file
```
/var/zgadget $ cd storage
/var/zgadget/storage $ sudo dd bs=1M if=/dev/zero of=/piusb.bin count=4048
/var/zgadget/storage $ sudo mkdosfs zgadget.img -F 32 -I
/var/zgadget/storage $
```

* In the */etc/fstab* append:
```
/var/zgadget/storage/zgadget.img /media/zgadget vfat loop,users,umask=000,noauto 0 2
```

* Create the directory */media/zgadget* for mounting:
```
/var/zgadget/storage $ sudo mkdir /media/zgadget
```

## Usage

* Create configuration tree and start sync server.
```
/var/zgadget/storage $ cd /var/zgadget/scripts
/var/zgadget/scripts $ sudo ./start_sync_storage.py
```

The configuration tree should look as follows:
```
/sys/kernel/config/usb_gadget/
└── g1
    ├── bcdDevice
    ├── bcdUSB
    ├── bDeviceClass
    ├── bDeviceProtocol
    ├── bDeviceSubClass
    ├── bMaxPacketSize0
    ├── configs
    │   └── c.1
    │       ├── bmAttributes
    │       ├── ecm.usb0 -> ../../../../usb_gadget/g1/functions/ecm.usb0
    │       ├── mass_storage.usb0 -> ../../../../usb_gadget/g1/functions/mass_storage.usb0
    │       ├── MaxPower
    │       └── strings
    │           └── 0x409
    │               └── configuration
    ├── functions
    │   ├── ecm.usb0
    │   │   ├── dev_addr
    │   │   ├── host_addr
    │   │   ├── ifname
    │   │   └── qmult
    │   └── mass_storage.usb0
    │       ├── lun.0
    │       │   ├── cdrom
    │       │   ├── file
    │       │   ├── inquiry_string
    │       │   ├── nofua
    │       │   ├── removable
    │       │   └── ro
    │       └── stall
    ├── idProduct
    ├── idVendor
    ├── os_desc
    │   ├── b_vendor_code
    │   ├── qw_sign
    │   └── use
    ├── strings
    │   └── 0x409
    │       ├── manufacturer
    │       ├── product
    │       └── serialnumber
    └── UDC

14 directories, 29 files
```

* Connect the Raspberry Zero with a Linux Machine
  ** A USB disk is mounted and available for Linux file managment
  
  ** A random IP address is generated for the Zero (Avahi). In my case: 169.254.158.207/16

  On the host side a port may be setup with:
  ```
  sudo ip a add 169.254.158.207/16 dev enx486f73745043
  ```

  This allows to connect the host to Zero:
  '''
  ssh 169.254.158.207
  '''

* Cleanup if you are done
``
var/zgadget/scripts $ sudo ./stop_sync_storage.py
```

* The process may be automated  by adding *zgadget_sync_watchdog.service*
  to */etc/systemd/system*
  ```
  [Unit]
  Description=USB gadget storage sync watchdog

  [Service]
  Type=simple
  ExecStart=/var/zgadget/scripts/start_sync_storage.py
  ExecStop=/var/zgadget/scripts/stop_sync_storage.py
  KillMode=process

  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```

* Activate the service
```
sudo systemctl daemon-reload
sudo systemctl enable zgadget_sync_watchdog.service
sudo systemctl start zgadget_sync_watchdog.service
```


