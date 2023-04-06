## Display 
Drawing to the display is slow and inefficient. The current method is to: 
Draw an image -> wait x ms -> clear the entire diplay -> Draw Next image.

Modern rendering relies on rendering only parts of a scene which have changed. With a scaled up number of LEDS, we too will need this for reliable framerates.
To do this, we take the concept from before of representing each frame as a csv file in the form [index, blue, green, red]. We represent the first frame this way, after which we represent the changes in pixels between frames. If a pixel changes state, we represent its new state as well as it's index. Since a majority of animations capapble of being rendered on the esp32 would have little change between frames, this improves both framerate and frame pacing.

so now:
Draw first frame -> wait x ms -> Draw pixels changed for next frame

If we are able to keep the actual time rendered down, we can keep a more consistent frame rate with our wait between frames. If rendering takes less then 50% x ms, frame pacing should not acceptable from a distance. 