import os
import subprocess
import shutil

class Py2CCompiler:
    def __init__(self, path='py2c'):
        self.path = path
        self.filename = []
        self.file_paths = []
        
    def create_directory(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
    
    def get_python_files(self):
        self.filename = [f for f in os.listdir(self.path) if f.endswith('.py')]
        self.file_paths = [f"{self.path}/{f}" for f in self.filename]
        
    def write_setup_file(self):
        with open('setup.py', 'w') as f:
            f.write(str('from distutils.core import setup') + '\n')
            f.write(str('from Cython.Build import cythonize') + '\n')
            f.write(str('') + '\n')
            f.write(str('setup(') + '\n')
            f.write(f"  ext_modules = cythonize({self.file_paths})" + '\n')
            f.write(str('   )') + '\n')
            
    def compile_files(self):
        try:
            subprocess.check_call('python setup.py build_ext --inplace', shell=True)
            print("Command executed successfully!")
        except subprocess.CalledProcessError as e:
            print("Command failed with return code:", e.returncode)
    
    def remove_files(self):
        if os.path.exists("setup.py"):
            os.remove("setup.py")
            print("setup.py has been removed")
            print('---------------------')
        if os.path.exists('build'):
            shutil.rmtree('build')
            print("build has been removed")
            print('---------------------')
        cfile = [f for f in os.listdir(self.path) if f.endswith('.c')]
        for f in cfile:
            os.remove(f"{self.path}/{f}")
            print(f"{f} has been removed")
            print('---------------------')
        print("All done!")
    
    def run(self):
        self.create_directory()
        self.get_python_files()
        self.write_setup_file()
        self.compile_files()
        self.remove_files() 

if __name__ == '__main__':
    compiler = Py2CCompiler()
    compiler.run()
