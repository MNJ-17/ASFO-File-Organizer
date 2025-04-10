import os
import shutil
import sys
import subprocess
import winreg as reg

def clean_folder(folder_path):
    if os.path.isdir(folder_path):
        for file_name in os.listdir(folder_path):
            full_file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(full_file_path):
                file_extension = file_name.split('.')[-1].lower()
                subfolder_name = f"{file_extension.upper()} Files"
                subfolder_path = create_subfolder_if_needed(folder_path, subfolder_name)
                new_location = os.path.join(subfolder_path, file_name)
                if not os.path.exists(new_location):
                    shutil.move(full_file_path, new_location)
                    print(f"Moved {file_name} to {subfolder_name}")
    else:
        print("Invalid folder path.")

def create_subfolder_if_needed(folder_path, subfolder_name):
    subfolder_path = os.path.join(folder_path, subfolder_name)
    if not os.path.exists(subfolder_path):
        os.mkdir(subfolder_path)
    return subfolder_path

def add_to_registry():
    key_base = r"Software\Classes\Directory\shell\ASFO"
    command_key = r"Software\Classes\Directory\shell\ASFO\command"

    # Create the main ASFO key
    with reg.CreateKey(reg.HKEY_CURRENT_USER, key_base) as key:
        reg.SetValue(key, "", reg.REG_SZ, "ASFO")
        icon_path = r"C:\Users\Asus\OneDrive\Desktop\favicon.ico"  # Change if needed
        reg.SetValueEx(key, "Icon", 0, reg.REG_SZ, icon_path)

    # Create the command subkey
    with reg.CreateKey(reg.HKEY_CURRENT_USER, command_key) as command:
        executable_path = f'"{os.path.abspath(sys.argv[0])}" "%1"'
        reg.SetValue(command, "", reg.REG_SZ, executable_path)

def uninstall():
    # Call the uninstall script using the current script's directory
    current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
    subprocess.run([sys.executable, os.path.join(current_directory, "uninstall.py")])

def check_for_uninstall():
    current_executable = os.path.abspath(sys.argv[0])
    if not os.path.exists(current_executable):
        uninstall()  # Call the uninstall function to remove the registry entry
        return True
    return False

if __name__ == "__main__":
    if check_for_uninstall():
        sys.exit(0)  # Exit if the program was uninstalled

    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "uninstall":
            uninstall()
        else:
            folder_path = sys.argv[1]
            clean_folder(folder_path)
    else:
        add_to_registry()
        print("ASFO installed and added to right-click menu.")
