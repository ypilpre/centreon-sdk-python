# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='centreonapi',
    version='0.0.3',
    description='Centreon Api for use Webservice in Centreon Web 2.8.0 or later',
    author='Centreon Team',
    author_email='contact@centreon.com',
    license='Apache-2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages(),
    install_requires=['requests', 'bs4']
)
