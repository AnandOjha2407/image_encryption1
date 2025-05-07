import cv2
import numpy as np
import os

def generate_depth_maps(image_path, output_dir):
    """
    Generate 3 depth maps from the uploaded image by simulating depth effect.
    Args:
        image_path (str): Path to the uploaded image.
        output_dir (str): Directory to save the generated depth maps.
    
    Returns:
        List of paths to the generated depth maps.
    """
    # Load the original image
    img = cv2.imread(image_path)

    # Make sure the image is not empty
    if img is None:
        raise ValueError("Image not loaded properly")

    depth_map_paths = []
    for i in range(3):  # Simulate 3 depth maps
        # In reality, you'd use a depth generation model here
        depth_map = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Simulated grayscale depth map
        depth_map_path = os.path.join(output_dir, f"depth_map_{i+1}.png")
        cv2.imwrite(depth_map_path, depth_map)
        depth_map_paths.append(depth_map_path)

    return depth_map_paths
