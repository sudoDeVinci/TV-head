"""
mm_wlan
--------
The ``mm_wlan`` module defines a couple of methods to simplify connecting to a 
wireless network. https://github.com/monkmakes/mm_wlan

"""

import network, time, sys

wlan = network.WLAN(network.STA_IF)

def connect_to_network(ssid, password, retries=10, verbose=True):
    wlan.active(True)
    if sys.platform != 'esp32':
        wlan.config(pm = 0xa11140)  # Disable power-save mode
    wlan.connect(ssid, password)
    if verbose: print('Connecting to ' + ssid, end=' ')
        
    while retries > 0 and wlan.status() in (network.STAT_CONNECTING ,2) : # 2 STAT_NOIP https://github.com/orgs/micropython/discussions/10746
        retries -= 1
        if verbose: print('.', end='')
        time.sleep(1)    
    # wifi status https://docs.micropython.org/en/latest/library/network.WLAN.html    
    if not is_connected():
        if verbose:
            if wlan.status() == network.STAT_CONNECTING :
                print('\nStill connecting, try later')
            elif wlan.status() == network.STAT_WRONG_PASSWORD:
                print('\nConnection failed. Check password')
            elif wlan.status() == network.STAT_NO_AP_FOUND:  
                print('\nConnection failed. Check ssid')
                print('Available networks:')
                for red in wlan.scan():
                    print(red[0])
            elif wlan.status() == network.STAT_CONNECT_FAIL:
                print('\nConnection failed. Unkown error')
            else :
                print(f'\nStatus:{wlan.status()}')
        raise RuntimeError('WLAN connection failed')
    else:
        if verbose: print('\nConnected. IP Address = ' + get_ip())

def get_ip():
    if is_connected():
        return wlan.ifconfig()[0]
    else:
        if verbose: print('\nNot connected')
        return None
        
def is_connected():
    return wlan.status() == network.STAT_GOT_IP


