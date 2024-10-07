#!/bin/bash --login

conda activate panel

cd /app/src

fastapi run --port 8080 main.py
