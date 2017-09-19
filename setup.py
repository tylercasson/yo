__version__ = '0.1'
from setuptools import setup, find_packages

import sys

version = sys.version_info
message = "yo needs Python>=3.5. Found {}".format(sys.version)

if version.major < 3 and version.minor < 5:
    sys.exit(message)

requires = []

setup(
    name='yo',
    version=__version__,
    description='Yo, a command runner',
    author='Tyler Casson',
    url='https://github.com/tylercasson/yo',
    packages=find_packages(),
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'yo = yo.yo:cli'
        ]
    },
    license=""
)
