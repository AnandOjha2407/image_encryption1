import os
import cv2
import numpy as np

def generate_depth_maps(upload_path, output_folder, count=3):
    """
    Simulates generation of depth maps from the uploaded image.
    Saves identical grayscale versions as stand-ins for actual depth maps.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Read the original image and convert to grayscale
    image = cv2.imread(upload_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    depth_map_paths = []

    for i in range(count):
        filename = f"depth_map_{i+1}.png"
        path = os.path.join(output_folder, filename)
        cv2.imwrite(path, gray)
        depth_map_paths.append(path)

    return depth_map_paths

def generate_sirds_images(depth_map_paths, output_folder):
    """
    Generates SIRDS (Single Image Random Dot Stereograms) from grayscale depth maps.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    sirds_paths = []

    for i, path in enumerate(depth_map_paths):
        depth_map = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        height, width = depth_map.shape
        sirds = np.random.randint(0, 256, (height, width), dtype=np.uint8)

        for y in range(height):
            for x in range(width):
                if depth_map[y, x] > 128:
                    sirds[y, x] = 255
                else:
                    sirds[y, x] = 0

        sirds_path = os.path.join(output_folder, f"sirds_{i+1}.png")
        cv2.imwrite(sirds_path, sirds)
        sirds_paths.append(sirds_path)

    return sirds_paths
