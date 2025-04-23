

# pip3 install alpyca
from alpaca.safetymonitor import *

Bolt = SafetyMonitor('192.168.74.74:80', 0)
print("Connecting...")
Bolt.Connected = True
if Bolt.Connected:
    print(f'Found {Bolt.Name}')
    state = 'safe' if Bolt.IsSafe else 'unsafe'
    print(f'Sky is {state}')
else:
    print('Cannot find Boltwood')
print("Disconnecting...")
Bolt.Connected = False
