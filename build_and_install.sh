#!/bin/bash

# This script will: build / test and install srbtok python library

# create virtual environment
uv sync

# activate virtual environment
. .venv/bin/activate


# run tests
PYTHONPATH="src:$PYTHONPATH" pytest test

# build package
uv build

# install package
deactivate
pip3 install dist/srbtok-0.1.0-py3-none-any.whl
