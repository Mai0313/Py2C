import customtkinter as ctk
from customtkinter import filedialog
import os
import subprocess
import shutil

def select_file():
    file_path = filedialog.askopenfilename()
    convert_to_c(file_path)

def convert_to_c(file_path):
    # create py2c directory if it doesn't exist
    path = 'py2c'
    if not os.path.exists(path):
        os.mkdir(path)
    # get filename and file path
    filename = os.path.basename(file_path)
    file_paths = [os.path.join(path, filename)]
    # copy file to py2c directory
    shutil.copy(file_path, os.path.join(path, filename))
    # generate C code from Python code using Cython
    with open('setup.py', 'w') as f:
        f.write(str('from distutils.core import setup') + '\n')
        f.write(str('from Cython.Build import cythonize') + '\n')
        f.write(str('') + '\n')
        f.write(str('setup(') + '\n')
        f.write(f"  ext_modules = cythonize({file_paths})" + '\n')
        f.write(str('   )') + '\n')
    try:
        subprocess.check_call('python setup.py build_ext --inplace', shell=True)
        print("Conversion executed successfully!")
    except subprocess.CalledProcessError as e:
        print("Conversion failed with return code:", e.returncode)
    # clean up files
    if os.path.exists("setup.py"):
        os.remove("setup.py")
        print("setup.py has been removed")
        print('---------------------')
    if os.path.exists('build'):
        shutil.rmtree('build')
        print("build has been removed")
        print('---------------------')
    cfile = [f for f in os.listdir(path) if f.endswith('.c')]
    for f in cfile:
        os.remove(os.path.join(path, f))
        print(f"{f} has been removed")
        print('---------------------')
    # print completion message
    print("All done!")

window = ctk.CTk()
window.title("Python To C")
window.geometry("600x400")

# widgets
label = ctk.CTkLabel(window, text="Select your file", width=20, height=2, font=("Helvetica", 16))
label.pack()

button = ctk.CTkButton(window, text="Select", width=20, height=2, font=("Helvetica", 16), command=select_file)
button.pack()

window.mainloop()
