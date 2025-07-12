# TV Head Animation JSON Format

This document describes the optimized JSON format used for storing LED matrix animations for microcontrollers.

## Format Overview

The JSON format is designed to be:
- **Compact**: Minimal file size for storage constraints
- **Efficient**: Fast parsing on resource-limited devices
- **Meta-data Efficient**: It's great for storing the metadata easily.

## JSON Structure

```json
{
  "metadata": {
    "name": "animation_name",
    "width": 10,
    "height": 10, 
    "total_pixels": 100,
    "frame_count": 5,
    "format": "bgr",
    "type": "diff"
  },
  "frames": [
        [
            [0, 255, 0, 0],
            [1, 0, 255, 0],
            [5, 0, 0, 255]
        ],
        [
            [1, 128, 255, 64],
            [5, 0, 128, 255]
        ]
    ]
}
```

## Animation Types

### Full Frames (`"type": "full"`)
- Contains all non-black/blank pixels for the frames
- The display is fully written to in each frame.
- `pixels` array contains `[index, blue, green, red]` values

### Differential Frame (`"type": "diff"`)
- Contains only pixels that changed from the previous frame
- Frames may be empty if nothing changes.

## Pixel Format

Each pixel is represented as:
```
[pixel_index, blue_value, green_value, red_value]
```

- `pixel_index`: 0-based index in the flattened LED strip
- Color values: 0-255 (BGR format to match OpenCV)
- Black pixels (0,0,0) are omitted to save space

## Pixel Index Mapping

For a 10x10 matrix with serpentine wiring:
```
Row 0: 0  →  1  →  2  →  3  → ... →  9
Row 1: 19 ← 18 ← 17 ← 16 ← ... ← 10  
Row 2: 20 → 21 → 22 → 23 → ... → 29
...
```
