from setuptools import setup
from Cython.Build import cythonize
from setuptools.extension import Extension
import os

dirname = os.path.dirname(os.path.abspath(__file__))

ext_modules = [
    Extension(
        "cpp_vm",
        sources=["cpp_vm.pyx"],
        language="c++",
        extra_compile_args=["-std=c++11"],
        include_dirs=[os.path.join(dirname, "RandomX-master/src")],
        libraries=["randomx"],
        library_dirs=[os.path.join(dirname, "RandomX-master/build")],
        extra_link_args=["-Wl,-rpath," + os.path.join(dirname, "RandomX-master/build")],
    )
]

setup(
    ext_modules=cythonize(ext_modules),
)

