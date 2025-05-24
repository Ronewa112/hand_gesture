import os

def run_command(gesture):
    if gesture == 0:
        print("Fist: Pause media")
        os.system("pyautogui key space")
    elif gesture == 1:
        print("Open Palm: Next Slide")
        os.system("pyautogui key Right")
    elif gesture == 2:
        print("Peace: Previous Slide")
        os.system("pyautogui key Left")
    elif gesture == 3:
        print("Thumbs up: Volume up")
        os.system("pyautogui key XF86AudioRaiseVolume")
    elif gesture == 4:
        print("Thumbs down: Volume down")
        os.system("pyautogui key XF86AudioLowerVolume")
