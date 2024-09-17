from microdot import Microdot, Response, redirect, send_file
from mm_wlan import connect_to_network
from micropython import const
from time import sleep_ms
import socket
import ujson as json
from time import sleep_ms
from neopixel import NeoPixel
from machine import freq, Pin
import uasyncio as asyncio

ssid = const('')
password = const('')
N = const(300)
display = NeoPixel(Pin(16), N, timing = 1)
app = Microdot()
color = const((200, 10, 10))

last_value = 0

@app.route('/favicon.ico')
async def favicon(request, path):
    return send_file('static/favicon.png')

@app.route('/static/<path:path>')
async def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('static/' + path)


@app.route('/', methods=['GET'])
async def index_get(request)-> Response:
    return send_file('static/index.html')

@app.route('/', methods = ['POST'])
async def index_post(request) -> None:
    global display
    global N
    global last_value
    
    lumins = int((int(request.json.get('luminance')) /600 ) * N)
    
    print(lumins)
    
    if abs(last_value - lumins) >= 5:
        last_value = lumins
        if last_value > lumins:
            for i in range(lumins, last_value):
                display[i] = (0, 0, 0)
        if last_value < lumins:
            for i in range(last_value, lumins):
                display[i] = color
        display.write()
        await asyncio.sleep_ms(150)
    
    await asyncio.sleep_ms(50)
        
        
    return '{ "Error": "None" }'

"""
An attempt to overclock the §Pi Pico for higher responsiveness.
Pi Pico to overclockable safely to 240MHz - 270MHz.
Base clock is 125MHz.
"""
try:
    freq(240000000)
except Exception as e:
    print("Core overclock not applied.")

print(f"-> Current speed is: {(freq()/1000000):.3f} MHZ")

for i in range(N): display[i] = (0,0,0)
display.write()
connect_to_network(ssid, password)
app.run(port=80)
