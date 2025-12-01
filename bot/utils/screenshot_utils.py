import time
import os
import subprocess
import cv2
import numpy as np

import random

from utils.paths import SCREENSHOT_DIR

def take_screenshot(adb_address, DIR=SCREENSHOT_DIR, filename=None):
    if filename is None:
        filename = f"screenshot_{random.randint(1000, 9999)}.png"

    remote_path = f"/sdcard/{filename}"
    local_path = os.path.join(DIR, filename)

    # Step 1: screencap on device
    screencap_cmd = ["adb", "-s", adb_address, "shell", "screencap", "-p", remote_path]
    result1 = subprocess.run(screencap_cmd, capture_output=True, text=True)
    if result1.returncode != 0:
        print(f"[{adb_address}] ❌ Error during screencap: {result1.stderr.strip()}")
        return None

    # Step 2: Pull file
    pull_cmd = ["adb", "-s", adb_address, "pull", remote_path, local_path]
    result2 = subprocess.run(pull_cmd, capture_output=True, text=True)
    if result2.returncode != 0:
        print(f"[{adb_address}] ❌ Error during pull: {result2.stderr.strip()}")
        return None

    return local_path


def check_template(adb_address, template_path, DIR=None, threshold=0.8):
    if DIR is None:
        DIR = SCREENSHOT_DIR
    
    screenshot_path = take_screenshot(adb_address, DIR=DIR)
    if not screenshot_path:
        return False

    img = cv2.imread(screenshot_path, 0)
    template = cv2.imread(template_path, 0)

    if img is None or template is None:
        return False

    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    
    print(f"Template match value: {max_val} for template {template_path}")
    
    time.sleep(random.uniform(0.05, 0.15))

    # try:
    #     if os.path.exists(screenshot_path):
    #         os.remove(screenshot_path)
    # except PermissionError:
    #     pass  # File is locked or already deleted by another thread
    # except Exception as e:
    #     print(f"Warning: Could not delete {screenshot_path}: {e}")

    return max_val >= threshold

def find_coordinates(adb_address, template_path, threshold=0.8):
    screenshot_path = take_screenshot(adb_address)
    img = cv2.imread(screenshot_path)
    template = cv2.imread(template_path)

    if img is None:
        print(f"❌ Failed to read screenshot: {screenshot_path}")
        return None

    if template is None:
        print(f"❌ Failed to read template: {template_path}")
        return None

    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    print(f"Template match value: {max_val} for template {template_path}")

    time.sleep(random.uniform(0.05, 0.15))

    try:
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
    except PermissionError:
        pass  # File is locked or already deleted by another thread
    except Exception as e:
        print(f"Warning: Could not delete {screenshot_path}: {e}")

    if max_val >= threshold:
        center_x = max_loc[0] + template.shape[1] // 2
        center_y = max_loc[1] + template.shape[0] // 2  
        return center_x, center_y
    else:
        return None
    
def find_all_coordinates(adb_address, template_path, threshold=0.8):
    screenshot_path = take_screenshot(adb_address)
    img = cv2.imread(screenshot_path)
    template = cv2.imread(template_path)

    if img is None:
        print(f"❌ Failed to read screenshot: {screenshot_path}")
        return []
    if template is None:
        print(f"❌ Failed to read template: {template_path}")
        return []

    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    time.sleep(random.uniform(0.05, 0.15))
    
    try:
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
    except PermissionError:
        pass  # File is locked or already deleted by another thread
    except Exception as e:
        print(f"Warning: Could not delete {screenshot_path}: {e}")

    # Find all positions above threshold
    y_coords, x_coords = np.where(result >= threshold)

    coords = []
    w = template.shape[1]
    h = template.shape[0]

    for (x, y) in zip(x_coords, y_coords):
        center_x = x + w // 2
        center_y = y + h // 2
        coords.append((center_x, center_y))

    return coords

def match_in_roi(adb_address, template_path, roi):
    """
    screenshot_path: full screenshot file
    template_path: the number/icon you want to find
    roi: (x1, y1, x2, y2) bounding box where we allow matching
    """
    x1, y1, x2, y2 = roi

    screenshot_path = take_screenshot(adb_address)

    screenshot = cv2.imread(screenshot_path)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    if screenshot is None or template is None:
        return None

    # Crop the image to your region
    cropped = screenshot[y1:y2, x1:x2]
    cropped_gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

    # Template matching only inside the ROI
    result = cv2.matchTemplate(cropped_gray, template, cv2.TM_CCOEFF_NORMED)

    # Get match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Confidence check
    if max_val > 0.8:  
        return True

    # Found inside ROI → convert to global coordinates
    # h, w = template.shape
    # global_x = max_loc[0] + x1 + w // 2
    # global_y = max_loc[1] + y1 + h // 2

    # return (global_x, global_y)

