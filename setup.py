from setuptools import setup

setup(
    name="tkcode",
    version="0.1",
    description="A code editor and code block widget for tkinter with syntax highlighting, and some other useful stuff",
    author="rdbende",
    author_email="rdbende@gmail.com",
    url="https://github.com/rdbende/tkcode",
    install_requires=['pygments'],
    python_requires='>=3.6',
    packages=["tkcode"],
    package_data={"tkcode": ["schemes/*"]}
)
