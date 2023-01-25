import os
import subprocess
path = 'py2c'
if not os.path.exists(path):
    os.mkdir(path)
filename = [f for f in os.listdir(path) if f.endswith('.py')]
file_paths = [f"{path}/{f}" for f in filename]

with open('setup.py', 'w') as f:
    f.write(str('from distutils.core import setup') + '\n')
    f.write(str('from Cython.Build import cythonize') + '\n')
    f.write(str('') + '\n')
    f.write(str('setup(') + '\n')
    f.write(f"  ext_modules = cythonize({file_paths})" + '\n')
    f.write(str('   )') + '\n')


try:
    subprocess.check_call('python setup.py build_ext --inplace', shell=True)
    print("Command executed successfully!")
except subprocess.CalledProcessError as e:
    print("Command failed with return code:", e.returncode)

import shutil
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
    os.remove(f"{path}/{f}")
    print(f"{f} has been removed")
    print('---------------------')
print("All done!")
# call python quickstart.py