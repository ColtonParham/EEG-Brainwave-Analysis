from PIL import Image, ImageDraw

# Function to read values from 'emotional.txt'
def read_values_from_file(filename):
    with open(filename, 'r') as file:
        input_line = file.readline().strip()
        values = []
        for value in input_line.split(';'):
            try:
                values.append(float(value))
            except ValueError:
                # Skip non-numeric values
                continue
        return values

# Read values from the file
filename = 'Emotional.txt'
values = read_values_from_file(filename)

# Create a blank image
width, height = 400, 400
image = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(image)

# Define a center point
center_x, center_y = width // 2, height // 2

# Define scaling factors to map values to drawing parameters
radius_scale = 1e6  # Scaling factor for the radius
position_scale = 1e5  # Scaling factor for positions

# Define colors for different brainwave types
colors = ['blue', 'green', 'red']
brainwave_types = ['Theta', 'Alpha', 'Beta']

# Draw circles based on the values
for i in range(0, len(values), 2):
    if i + 1 < len(values):
        radius = abs(values[i]) * radius_scale
        offset_x = int(values[i] * position_scale)
        offset_y = int(values[i + 1] * position_scale)

        # Determine the color based on the brainwave type
        color_index = (i // 2) % len(colors)
        color = colors[color_index]
        
        # Calculate the circle's bounding box
        left = center_x + offset_x - radius
        top = center_y + offset_y - radius
        right = center_x + offset_x + radius
        bottom = center_y + offset_y + radius
        
        # Draw the circle
        draw.ellipse([left, top, right, bottom], outline='black', fill=color)

# Save and show the image
image.save('brainwaves_drawing1.png')
image.show()
