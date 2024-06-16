from PIL import Image, ImageDraw
import random
import math

# Function to read values from 'Emotional.txt'
def read_values_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        # Assuming the first line is headers and the second line contains the data
        if len(lines) < 2:
            print("File does not contain enough data.")
            return []
        
        input_line = lines[1].strip()  # Read the second line
        print(f"Raw input line: {input_line}")  # Debug: Display raw input line
        
        values = []
        for value in input_line.split(';'):
            try:
                values.append(float(value))
            except ValueError:
                # Skip non-numeric values
                print(f"Skipping non-numeric value: {value}")  # Debug: Display skipped values
                continue
        return values

# Function to draw a circle
def draw_circle(draw, center_x, center_y, radius, color):
    left = center_x - radius
    top = center_y - radius
    right = center_x + radius
    bottom = center_y + radius
    draw.ellipse([left, top, right, bottom], outline='black', fill=color)

# Function to draw a square
def draw_square(draw, center_x, center_y, size, color):
    left = center_x - size // 2
    top = center_y - size // 2
    right = center_x + size // 2
    bottom = center_y + size // 2
    draw.rectangle([left, top, right, bottom], outline='black', fill=color)

# Function to draw a line
def draw_line(draw, start_x, start_y, end_x, end_y, color):
    draw.line([start_x, start_y, end_x, end_y], fill=color, width=3)

# Function to draw a triangle
def draw_triangle(draw, center_x, center_y, size, color):
    half_size = size / 2
    points = [
        (center_x, center_y - half_size),
        (center_x - half_size, center_y + half_size),
        (center_x + half_size, center_y + half_size)
    ]
    draw.polygon(points, outline='black', fill=color)

# Function to draw a polygon
def draw_polygon(draw, center_x, center_y, size, color, sides=5):
    angle = 360 / sides
    points = [
        (
            center_x + size * math.cos(math.radians(i * angle)),
            center_y + size * math.sin(math.radians(i * angle))
        )
        for i in range(sides)
    ]
    draw.polygon(points, outline='black', fill=color)

# Read values from the file
filename = '/workspaces/EEG-Brainwave-Analysis/Emotional.txt'
values = read_values_from_file(filename)

# Print values for debugging
print("Parsed values:", values)

# Check if there are any valid values to process
if not values:
    print("No valid numeric values found in the file.")
else:
    # Create a blank image
    width, height = 800, 800
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # Define a center point
    center_x, center_y = width // 2, height // 2

    # Define scaling factors to map values to drawing parameters
    radius_scale = 1e3  # Scaling factor for the radius
    position_scale = 1e2  # Scaling factor for positions
    size_scale = 1e2  # Scaling factor for size

    # Define shapes and colors for different brainwave types
    shapes = ['circle', 'square', 'triangle']
    colors = ['blue', 'green', 'red']

    # Assign specific shapes and colors to Theta, Alpha, Beta
    brainwave_types = {
        'Theta': {'shape': 'circle', 'color': 'blue'},
        'Alpha': {'shape': 'square', 'color': 'green'},
        'Beta': {'shape': 'triangle', 'color': 'red'}
    }

    # Draw shapes based on the values
    for i in range(0, len(values), 3):
        if i + 2 < len(values):
            # Determine brainwave type based on position
            brainwave_type = list(brainwave_types.keys())[i // 3 % len(brainwave_types)]
            shape_type = brainwave_types[brainwave_type]['shape']
            color = brainwave_types[brainwave_type]['color']

            offset_x = int(values[i] * position_scale)
            offset_y = int(values[i + 1] * position_scale)
            size_or_radius = abs(values[i + 2]) * size_scale

            # Add randomness to avoid overlapping and increase distribution
            offset_x += random.randint(-100, 100)
            offset_y += random.randint(-100, 100)
            size_or_radius = max(10, size_or_radius + random.randint(-20, 20))

            # Print parameters for debugging
            print(f"Drawing {brainwave_type} shape {i // 3}: shape={shape_type}, offset_x={offset_x}, offset_y={offset_y}, size_or_radius={size_or_radius}")

            # Draw the shape
            if shape_type == 'circle':
                draw_circle(draw, center_x + offset_x, center_y + offset_y, size_or_radius, color)
            elif shape_type == 'square':
                draw_square(draw, center_x + offset_x, center_y + offset_y, size_or_radius, color)
            elif shape_type == 'triangle':
                draw_triangle(draw, center_x + offset_x, center_y + offset_y, size_or_radius, color)

    # Save the image
    output_file = '/workspaces/EEG-Brainwave-Analysis/visualization_improved3.png'
    image.save(output_file)
    print(f"Drawing saved to {output_file}")
