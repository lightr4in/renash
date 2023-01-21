from setuptools import find_packages, setup

with open("../README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='renash',
    version='1.1.0',
    author='lightrain',
    author_email='lightrain@storstad.net',
    description='A package that renames files to their hash value',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://codeberg.org/lightrain/renash',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["renash"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "renash = renash.__main__:main"
        ]
    },
)
