# Zone & Tripwire Tool

A Python-based tool for creating and managing zones and tripwires in video frames using OpenCV. This tool helps in defining regions of interest (zones) and virtual tripwires in video frames, which can be used for various computer vision applications like object tracking, people counting, or intrusion detection.

## Features

### Zone Creation (Zone.py)
- Create rectangular zones by clicking and dragging
- Visual feedback while drawing
- Saves zone coordinates to a text file
- Simple and intuitive interface

### Tripwire Creation (Trip_Wire.py)
- Create tripwires by clicking two points
- Visual feedback of the tripwire
- Saves tripwire coordinates to a text file
- Easy reset functionality

## Prerequisites

- Python 3.x
- OpenCV (cv2)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/zone-tripwire-tool.git
   cd zone-tripwire-tool
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Creating a Zone
1. Place your image (e.g., `Cam1.jpg`) in the project directory
2. Run the zone creation tool:
   ```bash
   python Zone.py
   ```
3. Click and drag to create a rectangle (zone)
4. The coordinates will be saved to `zone_coords.txt`
5. Press 'q' to quit

### Creating a Tripwire
1. Place your image (e.g., `Cam1.jpg`) in the project directory
2. Run the tripwire tool:
   ```bash
   python Trip_Wire.py
   ```
3. Click two points to create a tripwire
4. The coordinates will be saved to `tripwire_coords.txt`
5. Press 'r' to reset or 'q' to quit

## File Descriptions

- `Zone.py`: Script for creating rectangular zones
- `Trip_Wire.py`: Script for creating tripwires
- `zone_coords.txt`: Output file containing zone coordinates
- `tripwire_coords.txt`: Output file containing tripwire coordinates
- `requirements.txt`: Required Python packages

## Output Format

### Zone Coordinates
Format: `x1,y1,x2,y2`
- (x1, y1): Top-left corner
- (x2, y2): Bottom-right corner

### Tripwire Coordinates
Format: `x1,y1,x2,y2`
- (x1, y1): Starting point
- (x2, y2): Ending point

## Example

1. Run `Zone.py` and draw a rectangle on the image
2. Run `Trip_Wire.py` and draw a line across a path
3. Use the generated coordinates in your computer vision pipeline

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
