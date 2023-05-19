# TV Head

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

The finished version one was done in time for Närcon Winter 2023 and can be seen here:
<br></br>
<img src='media/pose.jpg' alt="MarineGEO circle logo" style="height: 400px; width:300px;"/>
<br></br>

### Repo Structure

Files within the [upload](/upload/) folder are meant to be uploaded to the board.
Files within [dev](/dev/) are to remain on the computer. These hold the images and image-csv [converter](/dev/image_comparator.py).Files within [utility](/utility/) are utility scripts for easy use of any ESP32 board if you prefer that. These are: 
- [clearing the board's memory](/utility/clear_all.py) 
- [uploading all files](/utility/update_all.py) 
- [updating the csvs](/utility/update_csvs.py) 
- [viewing the board's file structure](/utility/view_files.py)

### Hardware structure

