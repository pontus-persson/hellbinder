import os
# import winreg
# import win32api
import glob
import shutil
from pprint import pprint
import config


def get_settings_file(try_path=None):
    # TODO: actually get steam path
    # settings_file = os.path.join("D:", "Games", "Steam", "userdata", "*", "553850", "remote", "input_settings.config") # 553850 is the helldivers 2 steam game id

    # 553850 is the helldivers 2 steam game id
    possible_paths = [
        os.path.join("C:", "Program Files (x86)", "Steam", "userdata", "*", "553850", "remote", "input_settings.config"),
        os.path.join("C:", "Program Files", "Steam", "userdata", "*", "553850", "remote", "input_settings.config"),
        os.path.join("C:", "Steam", "userdata", "*", "553850", "remote", "input_settings.config"),
        os.path.join("C:", "Games", "Steam", "userdata", "*", "553850", "remote", "input_settings.config"),
        os.path.join("D:", "Steam", "userdata", "*", "553850", "remote", "input_settings.config"),
        os.path.join("D:", "Games", "Steam", "userdata", "*", "553850", "remote", "input_settings.config"),
    ]
    if try_path:
        parts = os.path.split(os.path.dirname(try_path))
        possible_paths.append(os.path.join(*parts, "userdata", "*", "553850", "remote", "input_settings.config"))

    found_file = False

    for path in possible_paths:
        # print(path)
        # pprint(path)
        filename = glob.glob(path)
        #  = os.path.join("D:\Games\Steam", "File")
        if len(filename) == 0:
            continue
        if not os.path.isfile(filename[0]):
            continue
        print("Found file! " + filename[0])
        found_file = filename[0]
        break

    config.settings_file = found_file

    return found_file

def make_config_backup():
    if config.settings_file:
        shutil.copy2(config.settings_file, config.settings_file+".bak")
        return config.settings_file+".bak"
    return False

def get_settings_obj():
    # symbols = ['{', '}', '(', ')', '[', ']', '"', '*', ':', ',']
    symbols = ['{', '}', '(', ')', '[', ']', '"', ':', ',', '=']
    other_symbols = ['\\', '/*', '*/']
    # sections = ['Menu', 'Player', 'settings', 'Avatar', 'Stratagem']
    # keybinds = [
    #     # Menu

    #     # Player
    #     'OpenChat', 'CommunicationSpot', 'CommunicationWheelOpenBasic', 'VoicePushToTalk',
    #     # Avatar
    #     'String', 'Prone', 'CameraSwitchSide', 'WeaponFunctionDown', 'MoveForward', 'SwitchAimMode', 'ChangeEquipmentPrimary', 'MoveLeft',
    #     'ChangeEquipmentGrenade', 'Use', 'Dodge', 'Melee', 'Crouch', 'ChangeEquipmentQuickGrenade', 'MoveRight', 'WeaponFunctionLeft',
    #     'MoveBack', 'Climb', 'JumpPack', 'Sprint', 'Map', 'WeaponFunctionUp', 'WeaponFunctionRight', 'BackpackFunction', 'QuickStim',
    #     # Stratagem
    #     'Start', 'Up', 'Right', 'Down', 'Left'
    # ]

    # get the available bindings from the config
    sections = []
    keybinds = []
    for section, binds in config.available_bindings.items():
        sections.append(section)
        for bind in binds:
            keybinds.append(bind)

    pprint(sections)
    pprint(keybinds)

    keybind_inner = ['trigger', 'device_type', 'input', 'threshold', 'input_type']
    keywords = symbols + other_symbols + sections + keybinds
    white_space = [' ', '\t', '\n', '\r\n']
    lexeme = ''
    section = ''
    keybind = ''
    current_keybind = ''
    inside_keybind = False
    assign_next = False
    inside_string = False
    completed_string = False

    settings_obj = {}

    with open(config.settings_file, "r+") as settings:
        lines = settings.readlines()
        for line in lines:
            # print(line)
            for i, char in enumerate(line):
                # print(i, char)
                if char == '"':
                    inside_string = not inside_string
                    if not inside_string:
                        completed_string = True

                if char not in white_space or inside_string:
                    lexeme += char # adding a char each time

                if (i+1 < len(line)): # prevents error
                    if section == 'Avatar' and keybind == 'MoveLeft':
                        print('\t', inside_string, inside_keybind, char)
                    if lexeme in sections:
                        # print(lexeme)
                        section = lexeme
                        settings_obj[section] = {}
                        keybind = ''
                        lexeme = ''
                    elif lexeme in keybinds:
                        # print(section + '\\' + lexeme)
                        keybind = lexeme
                        lexeme = ''
                        settings_obj[section][keybind] = []
                    elif completed_string or not inside_string and (line[i+1] in white_space or line[i+1] in keywords or lexeme in keywords):
                        if lexeme != '':
                            # print(lexeme.replace('\n', '<newline>'))
                            # print(lexeme)
                            if section and keybind:
                                # settings_obj[section][keybind].append(lexeme)
                                if lexeme == '{': # start of bind block
                                    inside_keybind = True
                                    keybind_object = {}
                                elif lexeme == '}':
                                    inside_keybind = False
                                    settings_obj[section][keybind].append(keybind_object)
                                else:
                                    if lexeme in keybind_inner:
                                        current_keybind = lexeme
                                        # print('\t\t' + current_keybind)
                                        keybind_object[current_keybind] = ""
                                    elif lexeme == '=':
                                        assign_next = True
                                    elif assign_next and lexeme not in keywords:
                                        # print('\t\t\t' + lexeme)
                                        keybind_object[current_keybind] = lexeme
                                        assign_next = False
                                    # else:
                                    #     print(lexeme)
                            elif section == 'settings': # special case for settings, just save lines for now
                                if line[i+1] == '\n':
                                    settings_obj[section][len(settings_obj[section])] = line
                            # else:
                            #     print('Unknown ' + lexeme)

                            lexeme = ''
                        completed_string = False


        # print("".join(settings.readlines()))
        # print(settings.readlines())
        pprint(settings_obj)
    return settings_obj

def save_settings_obj(settings):

    file = config.settings_file + '.new'

    with open(file, "w+") as settings_file:

        for section_name, section in settings.items():
            # print(section_name)
            if section_name == 'settings':
                for row,line in section.items():
                    settings_file.write(line)
                continue
            elif len(section):
                settings_file.write(section_name + " = {" + '\n')
                # pprint(section)
                for keybind_name, keybinds in section.items():
                    line = '\t' + keybind_name + " = [" + '\n'
                    settings_file.write(line)
                    # print(keybind_name)
                    # print(keybinds)
                    # print(settings[section][keybind_name])
                    for states in keybinds:
                        # pprint(states)
                        settings_file.write('\t\t' + '{' + '\n')
                        for state_name, state in states.items():
                            # pprint(state_name + ' = ' + state)
                            settings_file.write('\t\t\t' + state_name + ' = ' + state + '\n')
                            # if isinstance(state, (int, float, complex)):
                            #     settings_file.write('\t\t\t' + state_name + ' = ' + state + '\n')
                            # else:
                            #     settings_file.write('\t\t\t' + state_name + ' = "' + state + '"\n')

                        settings_file.write('\t\t' + '}' + '\n')

                    settings_file.write('\t' + "]" + '\n')

            settings_file.write("}" + '\n')

            # for
        # settings_file.write(str1)




# def read_reg(ep, p = r"", k = ''):
#     try:
#         key = winreg.OpenKeyEx(ep, p)
#         value = winreg.QueryValueEx(key,k)
#         if key:
#             winreg.CloseKey(key)
#         return value[0]
#     except Exception as e:
#         return None
#     return None


# def get_steam_path2():
#     Path1 = "{}\\Microsoft\\Windows\\Start Menu\\Programs\\Steam\\Steam.lnk".format(os.getenv('APPDATA'))
#     if os.path.exists(Path1):
#         import sys
#         import win32com.client
#         shell = win32com.client.Dispatch("WScript.Shell")
#         shortcut = shell.CreateShortCut(Path1)
#         Path1Res = shortcut.Targetpath
#     else:
#         Path1Res = False
#     Path2 = str(read_reg(ep = winreg.HKEY_LOCAL_MACHINE, p = r"SOFTWARE\Wow6432Node\Valve\Steam", k = 'InstallPath'))+r"\steam.exe"
#     Path3 = str(read_reg(ep = winreg.HKEY_LOCAL_MACHINE, p = r"SOFTWARE\Valve\Steam", k = 'InstallPath'))+r"\steam.exe"
#     if not os.path.exists(Path2):
#         Path2 = None
#     if not os.path.exists(Path3):
#         Path3 = None
#     PossiblePaths = [r"X:\Steam\steam.exe", r"X:\Program Files\Steam\steam.exe", r"X:\Program Files (x86)\Steam\steam.exe"]
#     ValidHardPaths = []
#     for Drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
#         Drive = Drive.replace(':\\', '')
#         for path in PossiblePaths:
#             path = path.replace("X", Drive)
#             if os.path.exists(path):
#                 ValidHardPaths.append(path)
#     if len(ValidHardPaths) == 0:
#         ValidHardPaths = ["None"]
#     print("Registry64: " + str(Path2)+"|"+ "Registry32: "+ str(Path3)+"|"+ "Start Menu Shortcut: "+ str(Path1Res)+"|"+ "Possible Locations: " + ', '.join(ValidHardPaths)+"|")

#     return "Registry64: " + str(Path2)+"|"+ "Registry32: "+ str(Path3)+"|"+ "Start Menu Shortcut: "+ str(Path1Res)+"|"+ "Possible Locations: " + ', '.join(ValidHardPaths)+"|"
#     # return ValidHardPaths