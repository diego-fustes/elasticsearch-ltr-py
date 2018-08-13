# -*- coding: utf-8 -*-
from os.path import join, dirname

from setuptools import setup, find_packages

VERSION = (0, 0, 2)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

f = open(join(dirname(__file__), 'README'))
long_description = f.read().strip()
f.close()

install_requires = [
    'elasticsearch',
]

setup(
    name='elasticsearch_ltr',
    description="Python client for Elasticsearch with LTR plugin",
    license="Apache License, Version 2.0",
    url="https://github.com/diego-fustes/elasticsearch_ltr-py",
    long_description=long_description,
    version=__versionstr__,
    author="Diego Fustes",
    author_email="diegofustesfic@gmail.com",
    packages=find_packages(
        where='.',
        exclude=('test_elasticsearch_ltr*',)
    ),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6"
    ],
    install_requires=install_requires,
)
