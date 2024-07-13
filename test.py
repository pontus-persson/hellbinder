import os
import glob
from pprint import pprint

def get_settings_file():
    # TODO: actually get steam path
    settings_file = os.path.join("D:", "Games", "Steam", "userdata", "*", "553850", "remote", "input_settings.config") # 553850 is the helldivers 2 steam game id

    # 553850 is the helldivers 2 steam game id
    possible_paths = [
        os.path.join("C:", "Program Files (x86)", "Steam", "userdata", "*", "553850", "remote", "input_settings.config"),
        os.path.join("C:", "Program Files", "Steam", "userdata", "*", "553850", "remote", "input_settings.config"),
        os.path.join("C:", "Steam", "userdata", "*", "553850", "remote", "input_settings.config"),
        os.path.join("C:", "Games", "Steam", "userdata", "*", "553850", "remote", "input_settings.config"),
        os.path.join("D:", "Steam", "userdata", "*", "553850", "remote", "input_settings.config"),
        os.path.join("D:", "Games", "Steam", "userdata", "*", "553850", "remote", "input_settings.config"),
    ]
    found_file = False

    for path in possible_paths:
        print(path)
        # pprint(path)
        filename = glob.glob(path)
        #  = os.path.join("D:\Games\Steam", "File")

        if len(filename) == 0:
            continue

        if not os.path.isfile(filename[0]):
            continue

        print("Found file!")

        pprint(filename[0])

        found_file = filename[0]
        break

    return found_file


file = get_settings_file()
print(file)

# Open function to open the file "MyFile1.txt"
# (same directory) in read mode and
with open(file, "r+") as settings:
    print(settings.readline())
