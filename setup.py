#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from codecs import open
with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

__version__ = '0.0.7'

setup(
    name='anchorman',
    version=__version__,
    description='Markup terms in text',
    long_description=readme,
    author='Tarn Barford, Matthias Rebel',
    author_email='tarn@tarnbarford.net',
    url='https://github.com/rebeling/anchorman.git',
    license='Apache 2.0',
    packages=['anchorman'],
    package_data={'': ['LICENSE', 'NOTICE']},
    package_dir={'anchorman': 'anchorman'},
    include_package_data=True,
    install_requires=['lxml'],
    tests_require=['pytest', 'pytest-cov']
)
