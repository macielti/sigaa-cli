from setuptools import find_packages, setup
import poetry_version

with open('README.md','r') as fh:
    long_description = fh.read()

setup(
    name='sigaa-cli',
    version=poetry_version.extract(source_file="pyproject.toml"), 
    description='A uniffical Comand Line Interface that enable developers to execute some actions inside the SIGAA platform using python code. Independent of the university.',
    long_description=long_description,
    long_description_content_type='text/markdown',
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
    install_requires=[
        "requests"
    ]
)