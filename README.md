# TV Head

## What it is

This is the software behind my Tv Head cosplay made for 2023 Winter NarconS using ws2812 LED strips as a dot-matrix display to show various animations and images on the face.

While I had wanted to do this cosplay for a while, the technical details were modified from [Vivian Thomas'](https://rose.systems) implementation found [here](https://rose.systems/tv_head/).

My implementation aims more to be an alternate version of their mk1 design.

- Rather than use diagonal strips, simply using thinner strips.
- Making the design more user servicable and beginner friendly by including fewer parts and being written in MicroPython.
- Rather than focusing on displaying text, this design aims more to display pre-loaded images and animations.



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

If images filenames are not zero-padded, they may not be iterated through in the right order. A quick fix for mass-renaming files to be zero-padded is the [padded_rename script](dev/padded_rename.py) 

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

### Adjusting for Wiring Format

To allow for wiring similar to Vivan's implementation , we must adjust the conversion to account for the reversal of every other row in the display.
My wiring can be seen below against the 3D printed frame and light diffuser:

![wiring](media/wiring.jpg)

Every other row in the display is upside-down, which is the same as it simply being backwards. To account for this, we simply iterate through each row of the image during conversion, flipping every other row:

```python
# flatten image to 2d array
img_vector = img.reshape(-1, img.shape[-1])

# Flip every odd row in the array.
# "Row" as in row of pixels on the tv head.
# Assuming the wiring is as simple as possible.

# Image is sized to our dimensions so we use them
  for i in range(width, (height*width), width*2):
      # Start iterating at the first odd row
      # Skip to every other odd row afterward.
      # Flip the odd row and insert it in-place
      img_vector[i:(i+width)] = np.flip(img_vector[i:(i+width)], axis=1)
```

This however, also  flips the rgb tuples within the image vector. While there is possibly a better way to flip these back, this was the chosen solution due to time constraints:

```python
pixels = []

reverse = False
for i in range(img_vector.shape[0]):
    if i%(width) == 0:
        reverse = not reverse
    if np.any(img_vector[i]):
        if reverse:
            pixels.append([i, img_vector[i][2], img_vector[i][1], img_vector[i][0]])
        else:
            pixels.append([i, img_vector[i][0], img_vector[i][1], img_vector[i][2]])

```


### Addressing a WS2812 LED Dot-Matrix

To address the LEDS, we use the [NeoPixel](https://docs.micropython.org/en/latest/esp8266/tutorial/neopixel.html) library:

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

#### Addressing Individual LEDs

Individual LEDs are addressed by their index in the strip, and can be set to a specified RGB value with each colour channel as an element in a tuple:

```python
# To set LED i to (0, 0, 0):
display[i] = (0, 0, 0)  
```

#### Displaying an Image

To display an image, we simply loop through a csv file of flattened pixel values.

First we read a folder of csv files:

```python
def read_frames(folder_path:str) -> list[list[int]]:
  frames = []
  for filename in listdir(folder_path):
    if filename.endswith('.csv'):
      frame = []
      with open("/".join([folder_path, filename]), 'r', encoding = "utf-8") as csvfile:
        for line in csvfile:
          frame.append(line.rstrip('\n').rstrip('\r').split(","))
      frames.append(frame)
  return frames
```

This will give us a 3D array of pixel values.

##### Simple display

To display an image, we would simply loop through a list of these pixel values and assign them to the corresponding pixel.
We skip the first item in the list because it's the header for the csv file:

```python
for p in frame[1:]:
      display[p[0]] = (p[1], p[2], p[3])
      # To have the change made, we call:
      display.write()
```

To cycle through an animation, we loop through a list of frames and do the same as above, sleeping for a specified time between each:

```python
for frame in frames:
    for p in frame[1:]:
      display[p[0]] = (p[1], p[2], p[3])
    display.write()
    sleep_ms(sleep)
```

The problem with this however, is that unless an LED is explicitly turned off, it will persist to the next frame. We must be able to  clear our frame before drawing the next one.
While setting the display to a single value can be done iteratively, the Neopixel library provides the **.fill()** for this. This allows us an easy way to clear the display:

**NOTE:** This is fine for relatively low resolutions, however, for larger screen sizes it may be better to clear the pixels of the last frame specifically.

```python
display.fill((0, 0, 0,))
display.write()
```

Drawing can therefore be done via a funtion similar to:

```python
# Play frames with a set time interval in ms.
def animate(frames_path:str, sleep:int = 300) -> None:
    frames = read_frames(frames_path)

    for frame in frames:
        display.fill((0, 0, 0))
        for p in frame[1:]:
            display[int(p[0])] = (int(p[1]), int(p[2]), int(p[3]))
        display.write()
        sleep_ms(sleep)
```

**NOTE**: This is fine for short animations and small images, but due to memory constraints on microcontrollers, this is not an advised general solution.  A better solution would be that of a thrreaded queue of frames, or even simply rendering the frames as they are read.

##### Brightness

For LEDs which do not use RGBW but RGB, brightness is controlled by the colour value of the respective channels. (25,25,25) and (250,250,250) are the same colour, however the second one is brighter.  Remember also that light intensity is logarithmic, not linear.
Due to the brightness of the LEDS, I turned their brightness down a considerable amount via the following:


##### Debuggging

The main error when constructing this was incorrect wiring/addressing LED indexes. The [debuger script](upload/debugger.py) was constructed to check this by showing the wiring configuration with a small light bar of variable size and colour bouncin back and forth along the rows.


