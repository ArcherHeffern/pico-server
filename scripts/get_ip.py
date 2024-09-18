import network
from time import sleep

ssid = 'COSI142-a'
password = 'embedded_system'

#Connect to WLAN
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
print(wlan.status())

while wlan.isconnected() == False:
    print('Waiting for connection...', wlan.status())
    sleep(3)
ip = wlan.ifconfig()[0]
print(f'ip: {ip}')