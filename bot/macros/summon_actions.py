# """Summon-related actions"""

# import time
# # from template_matching import is_template_present_only, has_no_scrolls
# from .basic_actions import tap_macro
# from bot.utils.screenshot_utils import is_template_present_only, has_no_scrolls

# MAIN_PATH = "D:/Silver_Blood_Bot/"


# def perform_10x_summon(instance_name):
#     """Perform a 10x summon with skip automation
    
#     Args:
#         instance_name: Name of the LDPlayer instance
#     """
#     back_template = f"{MAIN_PATH}templates/back_button.png"
#     tap_template = f"{MAIN_PATH}templates/tap_here.png"
#     max_attempts = 10

#     print(f"[{instance_name}] 🚀 Starting 10x summon skip loop...")

#     for attempt in range(max_attempts):
#         print(f"[{instance_name}] ⏩ Skip tap #{attempt+1}")
#         tap_macro(instance_name, 1212, 53)
#         time.sleep(2)

#         # Check with template matching
#         back_present = is_template_present_only(instance_name, back_template, threshold=0.8)
#         time.sleep(0.3)
        
#         tap_present = is_template_present_only(instance_name, tap_template, threshold=0.8)
        
#         if back_present or tap_present:
#             reason = "back button" if back_present else "tap_here"
#             print(f"[{instance_name}] ✅ Summon finished — {reason} detected.")
#             break
#     else:
#         print(f"[{instance_name}] ⚠️ Max skip attempts reached without detecting completion.")


# def summon_until_empty(instance_name):
#     """Keep summoning until scrolls are depleted
    
#     Args:
#         instance_name: Name of the LDPlayer instance
#     """
#     zero_regular_template = f"{MAIN_PATH}templates/zero_regular_scrolls.png"
#     zero_rare_template = f"{MAIN_PATH}templates/zero_rare_scrolls.png"

#     for i in range(8):
#         # Check if we have no scrolls left
#         has_no_regular = has_no_scrolls(instance_name, zero_regular_template)
#         has_no_rare = has_no_scrolls(instance_name, zero_rare_template)
        
#         if has_no_regular or has_no_rare:
#             print(f"[{instance_name}] ✅ No scrolls left — stopping.")
#             break

#         # Perform 10x summon
#         print(f"[{instance_name}] ✨ Performing 10x summon #{i+1}")
#         tap_macro(instance_name, 815, 630)
#         time.sleep(2)
#         perform_10x_summon(instance_name)