#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python Backend/manage.py collectstatic --no-input
python Backend/manage.py migrate 