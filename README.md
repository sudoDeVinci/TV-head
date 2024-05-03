# TV Head

## What it is

This is the software behind my Tv Head cosplay made for Närcon Summer 2023 using WS2812B LED strips as a dot matrix display to show various animations and images on the face.

While I had wanted to do this cosplay for a while, the technical details were modified from [Vivian Thomas'](https://rose.systems) implementation found [here](https://rose.systems/tv_head/).

My implementation aims more to be an alternate version of their mk1 design:
<br></br>
<img src='media/vivan.jpg' alt="MarineGEO circle logo" style="height: 300px; width:300px;"/>
<br></br>
- Rather than use diagonal strips, simply using thinner strips.
- Making the design more user serviceable and beginner friendly by:
  - Including fewer parts
  - Including a version written in MicroPython.
- Display pre-loaded images and animations, rather than text.
- Adjusting settings via knobs on the front of the face rather than a wired keyboard.

version 1.0 | version 2.0 | version 3.0
:-----------------------------------:|:------------------------------------:|:------------------------------------:|
<img src='media/pose.jpg' alt="MarineGEO circle logo" style="height:300px; width:200px;"/> | <img src='media/single_suit.jpg' alt="MarineGEO circle logo" style="height: 300px; width:200px;"/> | <img src='media/v3_34.PNG' alt="MarineGEO circle logo" style="height: 300px; width:200px;"/>

### Hardware structure

The wiring of the leds is the same as the original made by Vivian. Don't fix what's not broken. an example can be seen below:
<br></br>
<img src='media/wiring.jpg' alt="MarineGEO circle logo" style="height: 400px; width:300px;"/>
<br></br>


## How it Works 

Images (either pixel art or other) are converted via the [open-cv](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) library into csv files containing the flattened (2D) pixel index and rgb values. These csvs are loaded onto the board where they can now be mapped onto the LED strip pixels. In this way, we retain the pixel data but save on memory.

This implementation allows having folders of sequential csv files which can be made into animations, with each file as a single frame.

**If images filenames are not zero-padded, they may not be iterated through in the right order. A quick fix for mass-renaming files to be zero-padded is the [padded_rename script](tvlib/padder.py)**


### Converting images

We move through all sub-directories in the [animations folder](animations/), converting each into a csv with a corresponding path within the [csv folder](csvs/) to the form:

```csv
index,red,green,blue
13,153,217,234
14,153,217,234
20,153,217,234
```

Where **index** here is that of the pixel the value is read from. Images are resized according to the resolution stored in [conf.toml](conf.toml) if needed. 
Alike images and frames of animations are kept within the same folder. Eg: The [Blink](/csvs/blink/) folder contains frames of a blinking animation.

Csvs are created as the change in pixels from the last frame via [Image Comparator](/dev/image_comparator.py), such that only the pixels changed between frames are rendered. This saves memory, disk space, and CPU cycles, as well as reducing flicker on larger displays from clearing, and is the default for operation.


#### Adjusting for Wiring Format

To allow for wiring similar to Vivan's implementation , we must adjust the conversion to account for the reversal of every other row in the display.
Every other row in the display is upside-down, which is the same as it simply being backwards. To account for this, we simply iterate through every other row of the image array, calling np.flip() along the row axis.

```Python

  # Reverse the order of pixels in every second row
  img[1::2, :] = flip(img[1::2, :], axis=1)

```

Now we flatten the array for easier comparison/iteration later on.

```Python

  img.reshape(-1, img.shape[-1])

```

