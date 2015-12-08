#!/bin/bash
if [ ! -f ./setup.py ]; then
  echo "This script is meant to be run in the top-level source directory."
  exit 1
fi

if [ -d dist ]; then
  echo "Please remove the dist/ directory before running the script."
  exit 1
fi

echo "==="
echo "BUILDING"
echo "==="
./setup.py sdist bdist_wheel

if [ $? -eq 0 ]; then
  echo "==="
  echo "UPLOADING"
  echo "==="
  twine upload dist/*.tar.gz dist/*.whl
else
  echo "Build did not complete successfully. Not uploading."
  exit 1
fi
