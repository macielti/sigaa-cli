from setuptools import find_packages, setup

with open('README.md','r') as fh:
    long_description = fh.read()

setup(
    name='sigaa-cli',
    version='0.1.0',
    description='A uniffical Comand Line Interface that enable developers to execute some actions inside the SIGAA platform using python code. Independent of the university.',
    long_description=long_description,
    packages=find_packages(),
    url="https://github.com/macielti/sigaa-cli",
    author="Bruno do Nascimento Maciel",
    author_email="brunodonascimentomaciel@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)