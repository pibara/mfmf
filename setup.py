"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mfmf',
    version='1.1.0',
    description='A Mediocre Forensic Module Framework. Meant as a fork-off point for real MattockFS based framework.',
    long_description=long_description,
    url='https://github.com/pibara/mfmf',
    author='Rob J Meijer',
    author_email='pibara@gmail.com',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: System :: Filesystems',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Operating System :: POSIX :: Linux',
        'Environment :: No Input/Output (Daemon)'
    ],
    keywords='computer forensics',
    install_requires=['mattock',"pytsk3","xattr"],
    packages=find_packages(exclude=['modules']),
)
