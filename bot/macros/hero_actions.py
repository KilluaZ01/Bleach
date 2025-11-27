# """Hero management actions"""

# # from daily_claim_runner import take_screenshot_another
# # from template_matching import find_template_on_screen
# from .basic_actions import swipe_macro

# MAIN_PATH = "D:/Silver_Blood_Bot/"


# def swipe_tank(instance_name, *args):
#     """Find and swipe tank hero
    
#     Args:
#         instance_name: Name of the LDPlayer instance
#     """
#     tank_path = f"{MAIN_PATH}templates/tank.png"
#     print(f"[{instance_name}] Taking screenshot to find Tank...")
#     new_screenshot_path = take_screenshot_another(instance_name)

#     match_coords = find_template_on_screen(new_screenshot_path, tank_path)
#     if match_coords:
#         x1, y1 = match_coords
#         print(f"[{instance_name}] ✅ Swiping Tank")
#         swipe_macro(instance_name, x1, y1, 685, 440)
#     else:
#         print(f"[{instance_name}] ❌ Tank Not Found")


# def swipe_tank_1(instance_name, *args):
#     """Find and swipe tank hero (variant 1)
    
#     Args:
#         instance_name: Name of the LDPlayer instance
#     """
#     tank_path = f"{MAIN_PATH}templates/tank.png"
#     print(f"[{instance_name}] Taking screenshot to find Tank...")
#     new_screenshot_path = take_screenshot_another(instance_name)

#     match_coords = find_template_on_screen(new_screenshot_path, tank_path)
#     if match_coords:
#         x1, y1 = match_coords
#         print(f"[{instance_name}] ✅ Swiping Tank")
#         swipe_macro(instance_name, x1, y1, 733, 241)
#     else:
#         print(f"[{instance_name}] ❌ Tank Not Found")


# def swipe_tank_2(instance_name, *args):
#     """Find and swipe tank hero (variant 2)
    
#     Args:
#         instance_name: Name of the LDPlayer instance
#     """
#     tank_path = f"{MAIN_PATH}templates/tank.png"
#     print(f"[{instance_name}] Taking screenshot to find Tank...")
#     new_screenshot_path = take_screenshot_another(instance_name)

#     match_coords = find_template_on_screen(new_screenshot_path, tank_path)
#     if match_coords:
#         x1, y1 = match_coords
#         print(f"[{instance_name}] ✅ Swiping Tank")
#         swipe_macro(instance_name, x1, y1, 740, 241)
#     else:
#         print(f"[{instance_name}] ❌ Tank Not Found")