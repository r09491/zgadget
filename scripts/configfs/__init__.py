import sys
import os
import glob

STORAGE = '/var/zgadget/storage/zgadget.img'
G1 = '/sys/kernel/config/usb_gadget/g1'

''' Used configuration number and function Name '''
C, N = 1, 'usb0'


def define():

    ''' Define the root ''' 
    os.makedirs(G1, exist_ok = True)
    
    ''' Define the common properties ''' 

    with open(os.path.join(G1, 'idVendor'), 'wb') as idVendor:
        idVendor.write(b'0x1d6b')
    with open(os.path.join(G1, 'idProduct'), 'wb') as idProduct:
        idProduct.write(b'0x0104')
    with open(os.path.join(G1, 'bcdDevice'), 'wb') as bcdDevice:
        bcdDevice.write(b'0x0100')
    with open(os.path.join(G1, 'bcdUSB'), 'wb') as bcdUSB:
        bcdUSB.write(b'0x0200')


    strings = os.path.join(G1, 'strings', '0x409')
    os.makedirs(strings, exist_ok = True)

    with open(os.path.join(strings, 'serialnumber'), 'wb') as serialnumber:
        serialnumber.write(b'1954195719821989')
    with open(os.path.join(strings, 'manufacturer'), 'wb') as manufacturer:
        manufacturer.write(b'r09491')
    with open(os.path.join(strings, 'product'), 'wb') as product:
        product.write(b'zgadget')


    ''' Define the functions '''

    ## The ethernet function 

    ecm = os.path.join(G1, 'functions', f'ecm.{N}')
    os.makedirs(ecm, exist_ok = True)

    with open(os.path.join(ecm, 'host_addr'), 'wb') as host_addr:
        host_addr.write(b'48:6f:73:74:50:43') # First byte even 57#57
    with open(os.path.join(ecm, 'dev_addr'), 'wb') as dev_addr:
        dev_addr.write(b'42:61:64:55:53:42')
    
    
    ## The mass storage function 

    mass_storage = os.path.join(G1, 'functions', f'mass_storage.{N}')
    os.makedirs(mass_storage, exist_ok = True)
    
    with open(os.path.join(mass_storage, 'stall'), 'wb') as stall:
        stall.write(b'1')
    with open(os.path.join(mass_storage, 'lun.0', 'cdrom'), 'wb') as cdrom:
        cdrom.write(b'0')
    with open(os.path.join(mass_storage, 'lun.0', 'ro'), 'wb') as ro:
        ro.write(b'0')
    with open(os.path.join(mass_storage, 'lun.0', 'nofua'), 'wb') as nofua:
        nofua.write(b'0')
    with open(os.path.join(mass_storage, 'lun.0', 'removable'), 'wb') as removable:
        removable.write(b'1')
    with open(os.path.join(mass_storage, 'lun.0', 'inquiry_string'), 'wb') as inquiry_string:
        inquiry_string.write(b'ZGADGET')
    with open(os.path.join(mass_storage, 'lun.0', 'file'), 'wb') as file:
        file.write(STORAGE.encode())


    ## other functions ...
        

    ''' Define the configuration '''
    
    configs = os.path.join(G1, 'configs', f'c.{C}')
    configs_strings = os.path.join(configs, 'strings', '0x409')
    os.makedirs(configs_strings, exist_ok = True)

    with open(os.path.join(configs_strings, 'configuration'), 'wb') as configuration:
        configuration.write(b'Config ZGADGET')

    with open(os.path.join(configs, 'MaxPower'), 'wb') as MaxPower:
        MaxPower.write(b'250')

    ## Link functions to configuration
    
    os.symlink(ecm, os.path.join(configs, os.path.basename(ecm)))
    
    os.symlink(mass_storage, os.path.join(configs, os.path.basename(mass_storage)))

    ## other function ...

    
    ''' Enable the gadget '''
    
    with open(os.path.join(G1, 'UDC'), 'wb') as UDC:
        UDC.write(' '.join(os.path.basename(i)
                           for i in glob.glob('/sys/class/udc/*')).encode())
        
    return 0


def clean():

    ''' Disable the gadget '''
    UDC = os.path.join(G1, 'UDC')
    if os.path.exists(UDC):
        with open(UDC, 'wb') as udc:
            udc.write(b'')
    
    
    ''' Get rid of the configurtion '''
    
    configs = os.path.join(G1, 'configs', f'c.{C}')
    if os.path.exists(configs):
        
        ''' Remove the function link from the configuration '''
    
        ecm = os.path.join(configs, f'ecm.{N}')
        if os.path.islink(ecm):
            os.unlink(ecm)
        
        mass_storage = os.path.join(configs, f'mass_storage.{N}')
        if os.path.islink(mass_storage):
            os.unlink(mass_storage)

        ## other functions ...

        ''' Remove the strings from the configurations '''

        configs_strings = os.path.join(configs, 'strings', '0x409')
        if os.path.isdir(configs_strings):
            os.rmdir(configs_strings) 

        ''' Remove the configurations direcrory its'''
        os.rmdir(configs)
    

    ''' Remove the functions from the gadget '''
    
    ecm = os.path.join(G1, 'functions', f'ecm.{N}')
    if os.path.isdir(ecm):
        os.rmdir(ecm)

    mass_storage = os.path.join(G1, 'functions', f'mass_storage.{N}')
    if os.path.isdir(mass_storage):
        os.rmdir(mass_storage)

    ## other functions ...

    strings = os.path.join(G1, 'strings', '0x409')
    if os.path.isdir(strings):
        os.rmdir(strings)

    
    ''' Remove the configuration of the gadget '''

    if os.path.isdir(G1):
        os.rmdir(G1)

    return 0









