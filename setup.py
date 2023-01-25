from distutils.core import setup
from Cython.Build import cythonize

setup(
  ext_modules = cythonize(['py2c/lol.py', 'py2c/main.py'])
   )
