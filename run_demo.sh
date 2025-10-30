#!/usr/bin/env bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export MOCK=true
python app.py
