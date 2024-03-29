# TV Head

## What it is

This is the software behind my Tv Head cosplay made for 2023 Winter NarconS using ws2812 LED strips as a dot-matrix display to show various animations and images on the face.

While I had wanted to do this cosplay for a while, the technical details were modified from [Vivian Thomas'](https://rose.systems) implementation found [here](https://rose.systems/tv_head/).

My implementation aims more to be an alternate version of their mk1 design.

- Rather than use diagonal strips, simply using thinner strips.
- Making the design more user servicable and beginner friendly by:
  - Including fewer parts
  - Being written in MicroPython.
- Rather than focusing on displaying text, this design aims to display pre-loaded images and animations.
- Rather than adjusting settings via a physical keyboard connection, a webserver can be used to control animations with a threaded handler.

### Structure

Files within the [upload](/upload/) folder are meant to be uploaded to the board.
Files within [dev](/dev/) are to remain on the computer. These hold the images and image-csv [converter](/dev/image_converter.py).
Files within [utility](/utility/) are utility scripts for easy use of any ESP32 board if you prefer that. These are: 
- [clearing the board's memory](/utility/clear_all.py) 
- [uploading all files](/utility/update_all.py) 
- [updating the csvs](/utility/update_csvs.py) 
- [viewing the board's file structure](/utility/view_files.py)

### Materials

Rather than the Circuit Playground Express microcontroller used by Vivan in their implementation, I opted to use a [Rasberry Pi Pico](https://www.amazon.se/-/en/SC0915-Raspberry-Pi-Pico/dp/B09KVB8LVR/ref=sr_1_5?crid=DJA3JLK27B3X&keywords=pi+pico&qid=1677125232&sprefix=pi+pico%2Caps%2C171&sr=8-5) because of my previous experience with micropython; a cloud tracking computer vision project which can be viewed [here](https://github.com/sudoDeVinci/Colour-Based-Cloud-Detection).

Listed items which are ticked indicate that they have been bought already.

- [x] [Rasberry Pi Pico](https://www.amazon.se/-/en/SC0915-Raspberry-Pi-Pico/dp/B09KVB8LVR/ref=sr_1_5?crid=DJA3JLK27B3X&keywords=pi+pico&qid=1677125232&sprefix=pi+pico%2Caps%2C171&sr=8-5)
- [x] [60 LED/m | 5m Length | 10mm width WS2812B LED Strip](https://www.amazon.se/-/en/dp/B08L8X7Z4P?psc=1&ref=ppx_yo2ov_dt_b_product_details)
- [x] [10 000 mAh Battery bank](https://www.amazon.se/-/en/Varta-5797610111-Power-Bank-Silver/dp/B08G91WFQR/ref=sr_1_10?crid=3BJ4IKJVQS9UX&keywords=powerbank&qid=1675220403&sprefix=power%2Bban%2Caps%2C373&sr=8-10&th=1)
- [x] [Micro USB Extension Cable](https://www.amazon.se/-/en/gp/product/B012S0ZQNU/ref=ox_sc_act_title_1?smid=ANU9KP01APNAG&psc=1)

## How it Works 

Images (either pixel art or other) are converted via the [open-cv](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) library into csv files containing the flattened (2D) pixel index and rgb values. These csvs are loaded onto the board where they can now be mapped onto the LED strip pixels. In this way, we retain the pixel data but save on memory.

This implementation allows having folders of sequential csv files which can be made into animations, with each file as a single frame.

**If images filenames are not zero-padded, they may not be iterated through in the right order. A quick fix for mass-renaming files to be zero-padded is the [padded_rename script](dev/padded_rename.py)**

### Converting images

We move through all sub-directories in [dev/images](/dev/images), converting each into a csv with a corresponding path within [upload/csvs](/upload/csvs) to the form:

```csv
index,red,green,blue
13,153,217,234
14,153,217,234
20,153,217,234
```

Where **index** here is that of the pixel the value is read from. Images are resized according to the resolution stored in [res.txt](/upload/res.txt) if needed.

Alike images and frames of animations are kept within the same folder. Eg: The [upload](upload/csvs/blink) folder contains frames of a blinking animation.

Csvs are created as either the change in pixels from the last frame via [Image Comparator](/dev/image_comparator.py) *(Recommended)*, or directly converted to csvs using [Image Converter](/dev/image_converter.py). The difference is in the first case, only the pixels changed between frames are rendered, whereas the second case requires clearing the screen and re-rendering the entire image regardless of frame-to-frame similarity. 
The first case therefore saves memory, disk space, and CPU cycles, as well as reducing flicker on larger disaplays from clearing, and is the default for operation.

#### Adjusting for Wiring Format

To allow for wiring similar to Vivan's implementation , we must adjust the conversion to account for the reversal of every other row in the display.
My wiring can be seen below against the 3D printed frame and light diffuser:

![wiring](media/wiring.jpg)

Every other row in the display is upside-down, which is the same as it simply being backwards. To account for this, we simply iterate through every other row of the image array, calling np.flip() along the row axis.

```python
# Reverse the order of pixels in every second row
for i in range(1, height, 2):
    img[i, :] = flip(img[i, :], axis=0)  # Flip the row
```
Now we flatten the array for easier comparison/iteration later on.

```python
img.reshape(-1, img.shape[-1])
```

### Addressing a WS2812 LED Dot-Matrix

To address the LEDS, we use the [NeoPixel](https://docs.micropython.org/en/latest/esp8266/tutorial/neopixel.html) library:

```python
from machine import Pin
from neopixel import NeoPixel

# Pin numbers to address
p = 16
# Number of leds to address
n = 100
# Define display to draw to
# Display is our array of leds.
display = NeoPixel(Pin(p), n, timing = 1)
```

#### Addressing Individual LEDs

Individual LEDs are addressed by their index in the strip, and can be set to a specified RGB value with each colour channel as an element in a tuple:

```python
# To set LED i to (0, 0, 0):
display[i] = (0, 0, 0)  
```

#### Displaying an Image

To display an image, we build the frame as a tuple of the pixel information, then send it to **animate()**.
**NOTE:** A threaded queue of frames would be preferred here, but that's for future implementation.

```python
from os import listdir

def read_frames(folder_path:str) -> list[list[int]]:
  for filename in listdir(folder_path):
    if filename.endswith('.csv'):
      with open("/".join([folder_path, filename]), 'r', encoding = "utf-8") as csvfile:
        frame = tuple((line.rstrip('\n').rstrip('\r').split(",")) for line in csvfile)
      animate(frame[1:])
```

This will give us a 3D array of pixel values.

##### Simple display

To display an image, we would simply loop through a list of these pixel values and assign them to the corresponding pixel.
We skip the first item in the list because it's the header for the csv file (above):

```python
# Play frames with a set time interval in ms.
def animate(frame, sleep:int = 25) -> None:
    for p in frame:
      display[int(p[0])] = (int(p[3]), int(p[2]), int(p[1]))
    display.write()
    # sleep_ms(sleep)
```

The problem with this however, is that unless an LED is explicitly turned off, it will persist to the next frame. We must be able to  clear our frame before drawing the next one.
While setting the display to a single value can be done iteratively, the Neopixel library provides the **.fill()** for this. This allows us an easy way to clear the display:

```python
display.fill((0, 0, 0,))
display.write()
```


##### Brightness

For LEDs which do not use RGBW but RGB, brightness is controlled by the colour value of the respective channels. (25,25,25) and (250,250,250) are the same colour, however the second one is brighter.  Remember also that light intensity is logarithmic, not linear.
Due to the brightness of the LEDS, I turned their brightness down a considerable amount via the following:


##### Debuggging

The main error when constructing this was incorrect wiring/addressing LED indexes. The [debuger script](upload/debugger.py) was constructed to check this by showing the wiring configuration with a small light bar of variable size and colour bouncin back and forth along the rows.


