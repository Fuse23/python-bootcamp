from distutils.core import setup, Extension
from Cython.Build import cythonize


def main():
    setup(ext_modules=cythonize(Extension(
        name="matrix",
        sources=["multiply.pyx"]
    )))


if __name__ == "__main__":
    main()
