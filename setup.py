from setuptools import setup, find_packages

CREATED= "06.01.2023"
NAME = "CodeNet"
VERSION = "0.1.0"
DESCRIPTION = "-"

setup(name=NAME,
      version=VERSION,
      author="Mr.Tamil",
      author_email="mr.tamil003@gmail.com",
      description=DESCRIPTION,
      packages=find_packages(),
      install_requires=[],
      keywords=[],
      classifiers=[
                   "Development Status :: 1 - Testing",
                   "Programming Language :: Python :: 3",
                   "Operating System :: Unix"
                   "Operating System :: Microsoft :: Windows"],
      zip_safe=False
)

