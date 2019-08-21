import pycom
import time
import ubinascii
import binascii
import os
import machine
import micropython
import json
import socket
import struct
import ustruct
import array
from network import LoRa
from network import Bluetooth
from network import WLAN
################################################################################

lora = LoRa(mode=LoRa.LORAWAN,region=LoRa.AS923, device_class=LoRa.CLASS_C, adr=False)

# create an OTA authentication params
dev_eui = ubinascii.unhexlify('007DD231238580F0')
app_eui = ubinascii.unhexlify('70B3D57ED0018276')
app_key = ubinascii.unhexlify('D4FF29049A27405AC5D01B750D299B9E')

# set the 3 default channels to the same frequency
lora.add_channel(0, frequency=923200000, dr_min=0, dr_max=6)
lora.add_channel(1, frequency=923400000, dr_min=0, dr_max=6)
lora.add_channel(2, frequency=923400000, dr_min=0, dr_max=6)
# join a network using OTAA
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=2)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not joined yet...')

# remove all the non-default channels
for i in range(0, 8):
    lora.remove_channel(i)

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket non-blocking
s.setblocking(False)

#Loops The scan every 2 minutes
pycom.heartbeat(False)

#initialize bluetooth
bluetooth = Bluetooth()

MacAddressList = []
MacAddressL = []

whiteList = [b'c2516b8e459d',b'f00f695ff143',b'c538524c4d77']
mapDict = {whiteList[0]:'Tag1', whiteList[1]: 'Tag2', whiteList[2]: 'Tag3'}

bluetooth.start_scan(20)

while True:
    #Retrieves mac adresses in the allocated time
    while bluetooth.isscanning():
        adv = bluetooth.get_adv()

        #CHANGE KONTAKT TO THE ADV NAME OF THE BLE TAGS YOU ARE USING
        if adv and bluetooth.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL) == 'Kontakt':
            print(ubinascii.hexlify(adv.mac))
            MacAddressList.append(ubinascii.hexlify(adv.mac))
            MacAddressList = [x for x in MacAddressList if x in whiteList]
            MacAddressList = list(set(MacAddressList))
            MacAddressL = [mapDict.get(n, n) for n in MacAddressList]
            MacAddressString = ' '.join(map(str, MacAddressL))
            data_out = json.dumps(MacAddressString)
            print("encoded" + data_out)
            data_in = data_out
            Mac_in = json.loads(data_in)
            print("decoded" + data_in)
            #pycom.rgbled(0x00FF00)
            time.sleep(1)


if bluetooth.isscanning() == False:
        print("TimeOut")
        time.sleep(3)
        print(data_out)
        s.send(data_out)
        print("published")
        #pycom.rgbled(0xFF0000)
        time.sleep(2)
        time.sleep(5)
        bluetooth.start_scan(20)
        MacAddressList.clear()
        MacAddressL.clear()
        data_out = json.dumps("")

###############################################################################
###############################################################################
