from PIL import Image
import numpy as np

# Define the 5 Rubik's Cube colors in RGB format
rubiks_colors = {
    'white': (255, 255, 255),
    'yellow': (255, 255, 0),
    'red': (255, 0, 0),
    'orange': (255, 165, 0),
    'blue': (0, 0, 255)
}

# Convert color values to a NumPy array for processing
color_values = np.array(list(rubiks_colors.values()))

def closest_color(pixel):
    """
    Find the closest Rubik's Cube color to a given pixel using Euclidean distance.
    """
    distances = np.linalg.norm(color_values - pixel, axis=1)
    index = np.argmin(distances)
    return tuple(color_values[index])

def process_image(image_path, output_path, grid_size=(77, 77)):
    """
    Process the image by resizing it to the specified grid size and limiting colors.
    """
    # Load and resize the image
    img = Image.open(image_path)
    img = img.resize(grid_size)  # Resize to grid size
    img = img.convert('RGB')     # Ensure it's in RGB format
    
    # Process each pixel
    pixels = np.array(img)
    height, width, _ = pixels.shape
    
    for i in range(height):
        for j in range(width):
            pixels[i, j] = closest_color(pixels[i, j])
    
    # Save the processed image
    output_img = Image.fromarray(pixels)
    output_img.save(output_path)  # Save at the exact grid size

# Input and output file paths
input_image = 'input_image.jpg'   # Replace with your image path
output_image = 'output_image.png' # Replace with desired output path

# Process the image
process_image(input_image, output_image, grid_size=(189, 189))
print("Image processing complete. Saved as:", output_image)
