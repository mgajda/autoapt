#!/bin/bash

set -o xtrace
VERSION="$(grep version setup.cfg |cut -f2 -d=|tr -d ' ')"

rm -rf dist/ __pycache__ &&
python3 -m build &&
python3 -m twine upload --repository pypi dist/autoapt-${VERSION}* \
                        --verbose &&
sync &&
echo "VERSION='${VERSION}'" &&
sensible-browser "https://pypi.org/project/autoapt/${VERSION}/" &&
sleep 20 && # time for index update
eval python3 -m pip install  --index-url "https://pypi.org/simple/" \
                             --force-reinstall \
                             --no-cache-dir    \
                             --no-deps "autoapt==${VERSION}" &&
python3 test/test.py
