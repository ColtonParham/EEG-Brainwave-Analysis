from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
import random
import math
import os

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
def draw_circle(draw, center_x, center_y, radius, color, transparency):
    left = center_x - radius
    top = center_y - radius
    right = center_x + radius
    bottom = center_y + radius
    draw.ellipse([left, top, right, bottom], outline='black', fill=color + (transparency,))

# Function to draw a square
def draw_square(draw, center_x, center_y, size, color, transparency):
    left = center_x - size // 2
    top = center_y - size // 2
    right = center_x + size // 2
    bottom = center_y + size // 2
    draw.rectangle([left, top, right, bottom], outline='black', fill=color + (transparency,))

# Function to draw a line
def draw_line(draw, start_x, start_y, end_x, end_y, color, transparency):
    draw.line([start_x, start_y, end_x, end_y], fill=color + (transparency,), width=3)

# Function to draw a triangle
def draw_triangle(draw, center_x, center_y, size, color, transparency):
    half_size = size / 2
    points = [
        (center_x, center_y - half_size),
        (center_x - half_size, center_y + half_size),
        (center_x + half_size, center_y + half_size)
    ]
    draw.polygon(points, outline='black', fill=color + (transparency,))

# Function to draw a polygon
def draw_polygon(draw, center_x, center_y, size, color, transparency, sides=5):
    angle = 360 / sides
    points = [
        (
            center_x + size * math.cos(math.radians(i * angle)),
            center_y + size * math.sin(math.radians(i * angle))
        )
        for i in range(sides)
    ]
    draw.polygon(points, outline='black', fill=color + (transparency,))

# Function to draw a star
def draw_star(draw, center_x, center_y, size, color, transparency, points=5):
    angle = 360 / points
    radius_inner = size / 2
    radius_outer = size
    vertices = []
    for i in range(points * 2):
        radius = radius_outer if i % 2 == 0 else radius_inner
        x = center_x + radius * math.cos(math.radians(i * angle / 2))
        y = center_y + radius * math.sin(math.radians(i * angle / 2))
        vertices.append((x, y))
    draw.polygon(vertices, outline='black', fill=color + (transparency,))

# Function to generate a unique file name
def generate_unique_filename(base_path, base_name, extension):
    i = 1
    while True:
        filename = f"{base_name}_{i}.{extension}"
        if not os.path.exists(os.path.join(base_path, filename)):
            return filename
        i += 1

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
    width, height = 500, 500
    image = Image.new('RGBA', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # Define a center point
    center_x, center_y = width // 2, height // 2

    # Define scaling factors to map values to drawing parameters
    radius_scale = 1e2  # Scaling factor for the radius
    position_scale = 50  # Scaling factor for positions
    size_scale = 50  # Scaling factor for size

    # Define shapes and colors for different brainwave types
    shapes = ['circle', 'square', 'triangle', 'line', 'polygon', 'star']
    colors = {
        'Theta': (0, 0, 255),  # Blue
        'Alpha': (0, 255, 0),  # Green
        'Beta': (255, 0, 0),   # Red
        'Gamma': (255, 255, 0), # Yellow
        'Delta': (255, 0, 255), # Magenta
        'Epsilon': (0, 255, 255), # Cyan
        'Zeta': (255, 165, 0), # Orange
        'Eta': (128, 0, 128), # Purple
        'ThetaAlpha': (75, 0, 130), # Indigo
        'AlphaBeta': (240, 128, 128), # Light Coral
        'BetaGamma': (255, 20, 147), # Deep Pink
        'GammaDelta': (255, 105, 180), # Hot Pink
        'DeltaTheta': (0, 128, 128), # Teal
        'EpsilonZeta': (123, 104, 238) # Medium Slate Blue
    }
    brainwave_types = list(colors.keys())

    # Draw shapes based on the values
    for i in range(0, len(values), 3):
        if i + 2 < len(values):
            for _ in range(random.randint(5, 15)):  # Draw multiple shapes per value set for more excitement
                # Determine brainwave type based on position
                brainwave_type = brainwave_types[i // 3 % len(brainwave_types)]
                shape_type = shapes[random.randint(0, len(shapes) - 1)]
                color = colors[brainwave_type]

                offset_x = int(values[i] * position_scale)
                offset_y = int(values[i + 1] * position_scale)
                size_or_radius = abs(values[i + 2]) * size_scale

                # Add randomness to avoid overlapping and increase distribution
                offset_x += random.randint(-150, 150)
                offset_y += random.randint(-150, 150)
                size_or_radius = max(10, size_or_radius + random.randint(-20, 20))

                # Add transparency
                transparency = random.randint(100, 255)

                # Print parameters for debugging
                print(f"Drawing {brainwave_type} shape {i // 3}: shape={shape_type}, offset_x={offset_x}, offset_y={offset_y}, size_or_radius={size_or_radius}")

                # Draw the shape
                if shape_type == 'circle':
                    draw_circle(draw, center_x + offset_x, center_y + offset_y, size_or_radius, color, transparency)
                elif shape_type == 'square':
                    draw_square(draw, center_x + offset_x, center_y + offset_y, size_or_radius, color, transparency)
                elif shape_type == 'line':
                    end_x = center_x + offset_x + size_or_radius
                    end_y = center_y + offset_y + size_or_radius
                    draw_line(draw, center_x + offset_x, center_y + offset_y, end_x, end_y, color, transparency)
                elif shape_type == 'triangle':
                    draw_triangle(draw, center_x + offset_x, center_y + offset_y, size_or_radius, color, transparency)
                elif shape_type == 'polygon':
                    draw_polygon(draw, center_x + offset_x, center_y + offset_y, size_or_radius, color, transparency, sides=random.randint(3, 6))
                elif shape_type == 'star':
                    draw_star(draw, center_x + offset_x, center_y + offset_y, size_or_radius, color, transparency, points=random.randint(5, 8))

    # Enhance the image for better visual effect
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)

    # Apply additional filters for more dynamic effects
    image = image.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.5, 2.0)))

    # Generate a unique filename and save the image
    base_path = '/workspaces/EEG-Brainwave-Analysis/'
    base_name = 'brainwaves_drawing'
    extension = 'png'
    output_file = generate_unique_filename(base_path, base_name, extension)
    image.save(os.path.join(base_path, output_file))
    print(f"Drawing saved to {output_file}")
