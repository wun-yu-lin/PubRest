
#!/usr/bin/env python

import os
from setuptools import setup


if os.path.exists('README.rst'):
    long_description = open('README.rst').read()
else:
    long_description = '''This package on testing'''

setup(
    name='PubRest',
    version='1.0.0',
    author='Wun-yu lin',
    author_email='',
    license='',
    url='',
    py_modules=['PubRest'],
    description='A simple Python wrapper around the PubChem PUG REST API.',
    long_description=long_description,
    keywords='pubchem python rest api chemistry cheminformatics',
    extras_require={'pandas': ['pandas']},
    test_suite='pubRest_test',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Database :: Front-Ends',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)