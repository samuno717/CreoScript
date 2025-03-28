import os
import sys
import time
from PIL import ImageGrab
import subprocess


def screen_resolution():
    bbox_dimensions = {(3200, 2000): (280, 350, 3200, 1950),
                       (2560, 1440): (350, 230, 2560, 1400),
                       (1920, 1080): (280, 190, 1920, 1050),
                       (3840, 2160): (560, 380, 3840, 2160)}

    screen_res = ImageGrab.grab().size

    if screen_res in bbox_dimensions:
        print(f"Detected resolution: {screen_res}")
        return bbox_dimensions[screen_res]
    else:
        print("Unsupported resolution!")
        input("Press Enter to quit.")
        sys.exit(1)


def dir_exists(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        print(f"Created missing directory: {dir_path}")
    return dir_path


def take_screenshot(bbox, save_path):
    ImageGrab.grab(bbox).save(save_path)
    print(f'Screenshot saved: {save_path}')


def run_testrun(filepath):
    try:
        os.startfile(filepath)
        print('\n[Test run]')
        print('Opening Creo View Express...')
        time.sleep(15)
        os.system('taskkill /f /im productview.exe')
        print('[Closed test run]\n')
    except PermissionError as error:
        print(f"Permission error while opening {filepath}: {error}")


def main():
    path = os.getcwd()
    models_path = dir_exists(os.path.join(path, 'models'))
    screenshots_path = dir_exists(os.path.join(path, 'screenshots'))
    bbox = screen_resolution()

    pvz_files = [file for file in os.listdir(models_path) if file.endswith('.pvz')]
    if not pvz_files:
        print("Error: No .pvz files found in 'models' directory.\n"
              "Put .pvz files inside models directory and run the script again.")
        input('Press Enter to quit.')
        sys.exit(1)

    existing_screenshots = [screen for screen in os.listdir(screenshots_path) if screen.endswith('.png')]
    if existing_screenshots == [file.replace('.pvz', '.png') for file in pvz_files]:
        print("\nAll screenshots have already been taken.")
        input("Press Enter to quit.")
        sys.exit(1)

    testrun = True
    for file in pvz_files:
        filepath = os.path.join(models_path, file)
        screen_path = os.path.join(screenshots_path, file.replace('.pvz', '.png'))

        if testrun:
            run_testrun(filepath)
            testrun = False

        if file.replace('.pvz', '.png') in existing_screenshots:
            continue

        try:
            os.startfile(filepath)
            print(f'Opened file: {file}')
            time.sleep(5)
            take_screenshot(bbox, screen_path)
            os.system('taskkill /f /im productview.exe')
            print(f'Closed file: {file}\n')
        except PermissionError as error:
            print(f"Permission error while opening {filepath}: {error}")

    print("END")
    input("Press Enter to quit.")

if __name__ == '__main__':
    main()