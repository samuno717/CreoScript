import os
import sys
import time
from PIL import ImageGrab

def get_bbox(resolution):
    bbox_dimensions = {(3200, 2000): (280, 350, 3200, 1950), (2560, 1440): (350, 230, 2560, 1400), (1920, 1080): (280, 190, 1920, 1050), (3840, 2160): (560, 380, 3840, 2160)}
    return bbox_dimensions.get(resolution)

def dir_exists(dir_path, dir_name):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        print(f"'{dir_name}' directory not found. Created a new one.")
    return dir_path

def screenshot(file, bbox, path):
    time.sleep(5)
    model_screenshot = ImageGrab.grab(bbox=bbox)
    model_screenshot.save(path)
    print(f'Screenshot of file {file} saved.')

def main():
    path = os.getcwd()
    models_dir_path = dir_exists(os.path.join(path, 'models'), 'models')
    screenshots_dir_path = dir_exists(os.path.join(path, 'screenshots'), 'screenshots')
    models = os.listdir(models_dir_path)

    if not models:
        print("Error: 'models' directory is empty - no models available.\nPut .pvz files inside models directory and run the script again.")
        input('Press Enter to quit.')
        sys.exit(1)
    screen_resolution = ImageGrab.grab().size
    bbox = get_bbox(screen_resolution)
    if bbox:
        print(f'Detected resolution: {screen_resolution[0]}x{screen_resolution[1]}\n')
    else:
        print('Unsupported resolution!')
        input('Press Enter to quit.')
        sys.exit(1)
    screenshot_count = 0
    testrun = True
    for file in models:
        filepath = os.path.join(models_dir_path, file)
        screen_path = os.path.join(screenshots_dir_path, file.replace('.pvz', '.png'))
        if file.endswith('.pvz'):
            if os.path.isfile(screen_path):
                print(f'Screenshot of model {file} already exists.')
                screenshot_count += 1
                if screenshot_count == len(models):
                    print('All screenshots taken!')
                    input('Press Enter to quit.')
                    sys.exit(1)
                continue
            if testrun:
                try:
                    os.startfile(filepath)
                    print('[Test run]')
                    print('Opening Creo View Express...')
                    time.sleep(10)
                    os.system('taskkill /f /im productview.exe')
                    print('[Closed test run]\n')
                    testrun = False
                except PermissionError as error:
                    pass
            else:
                try:
                    os.startfile(filepath)
                    print(f'Opened file: {file}')
                    screenshot(file, bbox, screen_path)
                    os.system('taskkill /f /im productview.exe')
                    print(f'Closed file: {file}\n')
                except PermissionError as error:
                    pass
        else:
            print('\nEND')
            input('Press Enter to quit.')
            print(f'Error: {error}')
            input('Press Enter to quit.')
            print(f'Error: {error}')
            input('Press Enter to quit.')
if __name__ == '__main__':
    main()