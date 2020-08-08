#! /bin/bash
pip3 install requirements
service mysql start
source venv/bin/activate
python3 main.py