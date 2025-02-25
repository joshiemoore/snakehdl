#!/usr/bin/env python3

from pathlib import Path
from setuptools import setup

directory = Path(__file__).resolve().parent
with open(directory / 'README.md', encoding='utf-8') as f:
  long_description = f.read()

setup(
  name='snakehdl',
  version='0.1.0',
  description='A simple, purely-functional HDL for Python',
  author='Josh Moore',
  license='MIT',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://github.com/joshiemoore/snakehdl',
  packages=[
    'snakehdl',
    'snakehdl.compilers',
    'snakehdl.components',
  ],
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Development Status :: 3 - Alpha',
  ],
  install_requires=[
    'numpy',
    'dill',
  ],
  extras_require={
    'testing': [
      'pytest',
      'cocotb',
    ],
  },
  python_requires='>=3.10'
)
