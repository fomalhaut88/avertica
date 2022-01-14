from setuptools import setup, find_packages

from avertica import __version__


# Extract dependencies from requirements.txt
with open('requirements.txt') as f:
    install_requires = f.readlines()

# Get description
with open('README.md') as f:
    description = f.read()


setup(
    name='avertica',
    version=__version__,
    description=description,
    author='Alexander Khlebushchev',
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires,
)
