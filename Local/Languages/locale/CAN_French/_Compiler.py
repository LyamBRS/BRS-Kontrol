import os
import importlib

# Check if polib is installed
try:
    polib = importlib.import_module('polib')
except ModuleNotFoundError:
    # If polib is not installed, run pip to install it
    import subprocess
    subprocess.check_call(['pip', 'install', 'polib'])
    polib = importlib.import_module('polib')

print("===========[BRS Simple Language File Compiler]===========")

# Get the path to the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
folder = script_dir.split("\\")
folder = folder[len(folder)-1]
print(f"Compiling: {folder}")

print("START\n----------")
# Loop through all .po files in the script directory
for filename in os.listdir(script_dir):
    if filename.endswith('.po'):
        po_filepath = os.path.join(script_dir, filename)

        # Load the .po file and compile it to a .mo file
        # try:
        po = polib.pofile(po_filepath)
        mo_filepath = os.path.splitext(po_filepath)[0] + '.mo'
        mo_filepath = mo_filepath.replace(folder, folder+"\\LC_MESSAGES")
        po.save_as_mofile(mo_filepath)
        print(f"Compiled: {filename}")
        # except:
            # print(f"[-FAILED-]: {filename}")

print("----------\nDONE")