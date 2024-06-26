# TV Head

## README IS NOT UP TO DATE - RENDERING CHANGES MADE
An updated version with Arduino support is [HERE](https://github.com/sudoDeVinci/ws2812b)

## What it is

This is the software behind my Tv Head coslay made for Närcon Summer 2023 using WS2812 LED strips as a dot matrix diplay to show various animations and images on the face.

While I had wanted to do this cosplay for a while, the technical details were modified from [Vivian Thomas'](https://rose.systems) implementation found [here](https://rose.systems/tv_head/).

My implementation aims more to be an alternate version of their mk1 design:
<br></br>
<img src='media/vivan.jpg' alt="MarineGEO circle logo" style="height: 300px; width:300px;"/>
<br></br>
- Rather than use diagonal strips, simply using thinner strips.
- Making the design more user servicable and beginner friendly by:
  - Including fewer parts
  - Being written in MicroPython.
- Rather than focusing on displaying text, this design aims to display pre-loaded images and animations.
- Rather than adjusting settings via a physical keyboard connection, a small webserver, as well as knobs on the front of the face can be used.

The finished version 1.0 was done in time for Närcon Winter 2023 and can be seen here:
<br></br>
<img src='media/pose.jpg' alt="MarineGEO circle logo" style="height: 400px; width:300px;"/>
<br></br>

The finished version 2.0 was done in time for Närcon Summer 2023 and can be seen here:
<br></br>
<img src='media/new_pose.jpg' alt="MarineGEO circle logo" style="height: 400px; width:300px;"/>
<br></br>

### Repo Structure

Files within the [upload](/upload/) folder are meant to be uploaded to the board.
Files within [dev](/dev/) are to remain on the computer. These hold the images and image-csv [converter](/dev/image_comparator.py).Files within [utility](/utility/) are utility scripts for easy use of any ESP32 board if you prefer that. These are: 
- [clearing the board's memory](/utility/clear_all.py) 
- [uploading all files](/utility/update_all.py) 
- [updating the csvs](/utility/update_csvs.py) 
- [viewing the board's file structure](/utility/view_files.py)

### Hardware structure

The wiring of the leds is the same as the original made by Vivian. Don't fix what's not broken. an example can be seen below:
<br></br>
<img src='media/wiring.jpg' alt="MarineGEO circle logo" style="height: 400px; width:300px;"/>
<br></br>

The basics of the entire system are shown here, with the only change being the use of linear encoders instead of potentiometers:
<br></br>
<img src='media/full_wiring.PNG' alt="MarineGEO circle logo" style="height: 300px; width:500px;"/>
<br></br>

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
The first case therefore saves memory, disk space, and CPU cycles, as well as reducing flicker on larger displays from clearing, and is the default for operation.

#### Adjusting for Wiring Format

To allow for wiring similar to Vivan's implementation , we must adjust the conversion to account for the reversal of every other row in the display.
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

### Global Rendering Variables
To be able to change global values such as the current brightness, channel, and speed, we keep them in a dictionary with their values.
```python
values = {
  "Brightness" : 0.10,
  "Speed" : 40,
  "Channel" : 4
  }
```
Each of these has an interrupt pin associated with it. These are kept in a Tuple of tuples
```python
pins = (
    (br_pin,"Brightness"),
    (sp_pin,"Speed"),
    (an_pin,"Channel")
)
```
These global values are changed via an interrupt on on of these pins. A packet containing the field changing and value is transmitted over UART from the other pico as a padded string. It's read and assigned accordingly in handle_interrupt(). Its is accessedin places such as animate() to calculate brightness.

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

Firstly we get a tuple of paths to our various animation folders.
```python
from os import listdir
def get_animations(folder_path = animation_folder) -> tuple[str]:
  folders = tuple(animation_folder+file[0] for file in ilistdir(folder_path) if file[1] == 0x4000)
  return folders
animations = get_animations()
animation_amount = len(animations)-1
```

We read the current animation index according to the value in the global dictionary. In main we call it like so:

```python
while running:
  read_frames(animations[values['Channel']])
  sleep_ms(values["Speed"]*10)
```

In read_frames(), we check the current animation index to the folder being iterated over, in case the interrupt was already called. Then we compile the current frame from the next csvfile in our folder.

```python
def read_frames(folder_path:str) -> list[list[int]]:
  global animations
  for filename in listdir(folder_path):
    if folder_path != animations[values['Channel']]:
      clear()
      return
    if filename.endswith('.csv'):
      with open("/".join([folder_path, filename]), 'r', encoding = "utf-8") as csvfile:
        frame = tuple((line.rstrip('\n').rstrip('\r').split(",")) for line in csvfile)
      animate(frame)
```
To display an image, we would simply loop through a list of these pixel values and assign them to the corresponding pixel.
We skip the first item in the list because it's the header for the csv file (above). For LEDs which do not use RGBW but RGB, brightness is controlled by the colour value of the respective channels. (25,25,25) and (250,250,250) are the same colour, however the second one is brighter.  Remember also that light intensity is logarithmic, not linear. So here, to turn down the brightness, we simply have a brightness coefficient from 0.0 to ~0.8 as our global value changed via interrupt. This way, our final brightness is gotten by a simple multiplication:

```python
def animate(frame) -> None:
    global dispaly
    b = values["Brightness"]
    for p in frame[1:]:
        display[int(p[0])] = (int(int(p[3])*b), int(int(p[2])*b), int(int(p[1])*b))
    display.write()
    sleep_ms(values["Speed"])
```

