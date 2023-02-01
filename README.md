# What it is
This is the software behind my Tv Head cosplay made for 2023 Winter NarconS using ws2812 LED strips as a dot-matrix display to show various animations and images on the face.

While I had wanted to do this cosplay for a while, the technical details were modified from [Vivian Thomas'](https://rose.systems) implementation found [here](https://rose.systems/tv_head/).

My implementation aims more to be an alternate version of their mk1 design. 
- Rather than use diagonal strips, simply using thinner strips.
- Making the design more user servicable and beginner friendly by including fewer parts and being written in MicroPython.
- Rather than focusing on displaying text, this design aims more to display pre-loaded images and animations. 

## Structure

Files within the [upload](/upload/) folder are meant to be uploaded to the board.
Files within [dev](/dev/) are to remain on the computer. These hold the images and image-csv [converter](/dev/converter.py).
Files within [utility](/utility/) are utility scripts for easy use of the ESP32 board. These are [clearing the board's memory](/utility/clear_all.py), [uploading all files](/utility/update_all.py), [updating the csvs](/utility/update_csvs.py) and [viewing the board's file structure](/utility/view_files.py).


## Materials
Rather than the Circuit Playground Express microcontroller used by Vivan in their implementation, I opted to use a [Freenove ESP32-WROVER](https://www.amazon.se/-/en/Freenove-ESP32-WROVER-Compatible-Wireless-Detailed/dp/B09BC5CNHM/ref=sr_1_25?crid=2F3ZES5T9PUGN&keywords=esp32&qid=1675219924&sprefix=esp32%2Caps%2C376&sr=8-25) because of my previous experience with one; a cloud tracking computer vision project which can be viewed [here](https://github.com/sudoDeVinci/Colour-Based-Cloud-Detection).

Listed items which are ticked indicate that they have been bought already.

- [x] [Freenove ESP32-WROVER CAM](https://www.amazon.se/-/en/Freenove-ESP32-WROVER-Compatible-Wireless-Detailed/dp/B09BC5CNHM/ref=sr_1_25?crid=2F3ZES5T9PUGN&keywords=esp32&qid=1675219924&sprefix=esp32%2Caps%2C376&sr=8-25).
- [x] [3 mm width WS2812B-2020 LED Strip](https://shop-nl.blinkinlabs.com/collections/leds/products/3mm-ultra-thin-digital-led-strip-with-ws2812b-2020-100leds-strip)
- [ ] [10 000 mAh Battery bank](https://www.amazon.se/-/en/Varta-5797610111-Power-Bank-Silver/dp/B08G91WFQR/ref=sr_1_10?crid=3BJ4IKJVQS9UX&keywords=powerbank&qid=1675220403&sprefix=power%2Bban%2Caps%2C373&sr=8-10&th=1)
- [x] [Micro USB Extension Cable](https://www.amazon.se/-/en/gp/product/B012S0ZQNU/ref=ox_sc_act_title_1?smid=ANU9KP01APNAG&psc=1)


# What it does
Images (either pixel art or other) are converted via the [open-cv](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) library into csv files containing the flattened pixel index and rgb values. These csvs are loaded onto the esp32 board where they can now be mapped onto the LED strip pixels. In this way, we retain the pixel data but save on memory.

This implementation allows having folders of sequential csv files which can be made into animations, with each file as a single frame.


## Converting images
We move through all sub-directories in [dev/images](/dev/images), converting each into a csv with a corresponding path within [upload/csvs](/upload/csvs) to the form:
```csv
index,red,green,blue
13,153,217,234
14,153,217,234
20,153,217,234
```
Where **index** here is that of the pixel the value is read from. Images are resized according to the resolution stored in [res.txt](/upload/res.txt) if needed.


## Addressing WS2812 LED Dot-Matrix
To address the LEDS, we use the [NeoPixel](https://docs.micropython.org/en/latest/esp8266/tutorial/neopixel.html) library.

```python
from machine import Pin
from neopixel import NeoPixel

# Pin numbers to address
p = 5
# Number of leds to address
n = 96
# Define display to draw to
# Display is our array of leds.
display = NeoPixel(Pin(p), n)
```

