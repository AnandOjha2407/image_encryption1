import cv2
import numpy as np
import os

def generate_sirds(depth_map_paths, output_dir, width=300, height=300):
    """
    Generates 3 SIRDS images from depth maps by creating random dot stereograms.
    
    Args:
        depth_map_paths (list): List of file paths to the depth maps.
        output_dir (str): Folder to save the generated SIRDS images.
        width (int): Width of the SIRDS images.
        height (int): Height of the SIRDS images.
        
    Returns:
        list: Paths to the saved SIRDS images.
    """
    sirds_paths = []
    
    for i, depth_map_path in enumerate(depth_map_paths):
        # Load the depth map
        depth_map = cv2.imread(depth_map_path, cv2.IMREAD_GRAYSCALE)
        
        # Resize depth map to target dimensions
        depth_map = cv2.resize(depth_map, (width, height))

        # Create random dot background for stereogram (simulating SIRDS)
        sirds_image = np.random.randint(0, 256, (height, width), dtype=np.uint8)

        # Create stereogram effect based on depth map
        for row in range(height):
            for col in range(width):
                depth_value = depth_map[row, col]
                if depth_value > 128:  # Simulate depth with higher values
                    sirds_image[row, col] = 255
                else:
                    sirds_image[row, col] = 0

        # Save the SIRDS image
        filename = f"sirds_{i+1}.png"
        filepath = os.path.join(output_dir, filename)
        cv2.imwrite(filepath, sirds_image)
        sirds_paths.append(filepath)
    
    return sirds_paths
