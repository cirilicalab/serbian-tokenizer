#!/bin/bash

# create virtual environment
uv sync

# activate virtual environment
. .venv/bin/activate

# run tests
PYTHONPATH="src:$PYTHONPATH" pytest test

# build package
uv build

deactivate
