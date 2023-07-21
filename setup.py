from setuptools import setup, find_packages
import os.path
import re

# reading package's version (same way sqlalchemy does)
#with open(
#    os.path.join(os.path.dirname(__file__), 'flasker', '__init__.py')
#) as v_file:
#    package_version = \
#        re.compile('.*__version__ = \'(.*?)\'', re.S)\
#        .match(v_file.read())\
#        .group(1)


dependencies = [
    'flask'
]


setup(
    name='flasker',
#    version=package_version,
    author='Mohamad Khajezade',
    author_email='khajezade.mohamad@gmail.com',
    description='Learning flask',
    install_requires=dependencies,
    packages=find_packages(),
)
