from time import sleep
from gc import collect

# start text web-server
def server_start():
    SSID = "TvHead"                     # Enter your WiFi name
    PASSWORD = "TransRights"            # Your WiFi password

    from network import WLAN, AP_IF
    
    wlan = WLAN(AP_IF)
    wlan.active(True)
    wlan.config(essid = SSID, password = PASSWORD)
    
    conf = wlan.ifconfig()
    print('Connected, IP address:', conf)
    return wlan


# Get current ip address
def get_ip() -> str:
    from socket import socket, AF_INET, SOCK_DGRAM
    s = socket(AF_INET, SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'


from socket import socket, SOL_SOCKET, SO_REUSEADDR


def listen(s: socket):
    from encoder import Encoder
    while True:
        print("Listening")
        c,a = s.accept()
        with Encoder(c) as l:
            print('Connection from {0}'.format(str(a)))
            print("Receiving Text..")

            try:
                data = l.get()
                if not data:
                    print("No data received")
                else:
                    print(f"Received {data.decode('utf-8')}")
            except Exception as e:
                print(e)

s = socket()

wlan = server_start()
try:
    # Try to let the socket address be reusable
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    try:
        # Try to bind the socket to an address and port
        s.bind(('',1312))
        s.listen(100)
        # Listen, looping repeatedly
        listen(s)
    except Exception as e:
        print(e)
except Exception as e:
    print(e)
    if s:
        s.close()
    if wlan:
        wlan.disconnect()