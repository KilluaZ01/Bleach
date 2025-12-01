# Matching two image using cv2

import cv2
import numpy as np

def check_track(img_path1, img_path2, threshold=0.8):
    """
    Check if img_path2 is present in img_path1 using template matching.
    
    :param img_path1: Path to the main image.
    :param img_path2: Path to the template image to search for.
    :param threshold: Similarity threshold (default is 0.8).
    :return: True if template is found, False otherwise.
    """
    # Read the main image and template image
    img = cv2.imread(img_path2)
    template = cv2.imread(img_path1)

    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    
    print(f"Template match value: {max_val} for template {img_path2}")

    # Check if the maximum similarity exceeds the threshold
    if max_val >= threshold:
        return True
    else:
        return False

if __name__ == "__main__":
    # Example usage
    img_path1 = "C:\\Users\\Killua\\Desktop\\Bleach\\templates\\track_text.png"  # Path to the main image
    img_path2 = "C:\\Users\\Killua\\Desktop\\Bleach\\templates\\screenshot_9616.png"  # Path to the template image

    if check_track(img_path1, img_path2):
        print("Template found in the image.")
    else:
        print("Template not found in the image.")