import os
import shutil

from pydantic import Field, FilePath, BaseModel, model_validator
from setuptools import setup
from Cython.Build import cythonize


class Py2C(BaseModel):
    input_path: FilePath = Field(
        ...,
        title="Python File Path",
        description="enter the filepath of your python file, better be abs path.",
        example="/home/mai/Py2C/test.py",
    )

    @model_validator(mode="before")
    def check_if_no_input(cls, values):
        if values.get("input_path") is None:
            raise ValueError("input_path is required")

    def py_to_cython(self):
        root_dir, filename = os.path.split(self.input_path)
        basename, suffix = os.path.splitext(filename)
        cython_file_path = f"{root_dir}/{basename}.pyx"
        with open(self.input_path) as py_file:
            py_content = py_file.read()
        with open(cython_file_path, "w") as cython_file:
            cython_file.write(py_content)
        setup(
            ext_modules=cythonize(cython_file_path, language_level="3", build_dir="build"),
            script_args=["build_ext", "--inplace"],
        )
        print(f"{self.input_path} has been compiled to {cython_file_path}")  # noqa: T201
        os.remove(cython_file_path)
        shutil.rmtree("build")


if __name__ == "__main__":
    Py2C(input_path="/home/mai/Py2C/test.py").py_to_cython()
