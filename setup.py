from os import path
from setuptools import setup, find_packages

README = f'{path.abspath(path.dirname(__file__))}/README.md'

with open(README, 'r') as readme_file:
    README_CONTENT = readme_file.read()

setup(
    name='adafruit-fingerprint',
    version='1.0.2',
    packages=find_packages(),

    # meta
    author='Faith Odonghanro, Promise Nwanozie, Joshua Adegoke',
    author_email='toriboi.fo@gmail.com',
    description='Interface with the adafruit fingerprint r305 module from upper computer over serial connection',
    long_description_content_type='text/markdown',
    long_description=README_CONTENT,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6'
    ],
    url='https://github.com/cerebrohivetech/adafruit-fingerprint',
    project_urls={
        'Documentation': 'https://adafruit-fingerprint.readthedocs',
        'Repository': 'https://github.com/cerebrohivetech/adafruit-fingerprint'
    },
    install_requires=['pyserial==3.4.0']
)
