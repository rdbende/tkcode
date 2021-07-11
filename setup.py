from setuptools import setup
import subprocess

version = subprocess.check_output(["git", "describe", "--abbrev=0", "--tags"]).strip().decode()

assert version[0] == "v"  # Something went wrong

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="tkcode",
    version=version,
    description="A code editor and code block widget for tkinter with syntax highlighting, and some other useful stuff",
    long_description=long_description,
    author="rdbende",
    author_email="rdbende@gmail.com",
    url="https://github.com/rdbende/tkcode",
    install_requires=['pygments'],
    python_requires='>=3.6',
    packages=["tkcode"],
    package_data={"tkcode": ["schemes/*"]},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
