# In micropython, listen on port 1312 for text data
from socket import socket, error, AF_INET, SOCK_DGRAM
from time import sleep
from struct import pack

# Get current ip address
def get_ip() -> str:
    s = socket(AF_INET, SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'


s = socket()
try:
    # s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.connect(('127.0.0.1',1312))
except Exception as e:
    exit(1)

WAIT = 2

count = 0
while count < 3:
    count +=1
    data = input(">> Text To Send: ")
    data = data.encode('utf-8')
    length = len(data)

    while True:
        try:
            s.send(pack('<I',length))
            s.sendall(data)
            break
            
        except error as e:
            #print(e)
            s.close()
            s = socket()
            s.connect_ex((get_ip(), 1312))

    sleep(WAIT)

s.close()
