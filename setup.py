
# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


import os.path

readme = ''
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, 'README.rst')
if os.path.exists(readme_path):
    with open(readme_path, 'rb') as stream:
        readme = stream.read().decode('utf8')


setup(
    long_description=readme,
    name='gcspypi2',
    version='0.1.11',
    description='CLI for creating a Python Package Repository in a GCS bucket',
    python_requires='!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,<4.0,>=2.7',
    author='Tonye Jack',
    author_email='jtonye@ymail.com',
    entry_points={"console_scripts": ["gcspypi = gcspypi2.__main__:main"]},
    packages=['gcspypi2'],
    package_dir={"": "."},
    package_data={"gcspypi2": ["templates/*.j2"]},
    install_requires=['futures==3.*,>=3.3.0; python_version == "2.7.*" and python_version >= "2.7.0"', 'google-api-core==1.*,>=1.17.0', 'google-cloud-core==1.*,>=1.3.0', 'google-cloud-storage==1.*,>=1.28.0', 'jinja2==2.*,>=2.10.1', 'wheel==0.*,>=0.33.6'],
    extras_require={"dev": ["black==19.*,>=19.3.0.b0; python_version == \"3.*\" and python_version >= \"3.6.0\"", "dephell==0.*,>=0.8.3; python_version == \"3.*\" and python_version >= \"3.6.0\"", "flake8==3.*,>=3.7.8", "ipdb==0.*,>=0.13.2", "isort==4.*,>=4.3.21", "mock==3.0.5", "pytest>=4.6.5", "pytest-cov==2.*,>=2.7.1"]},
)
