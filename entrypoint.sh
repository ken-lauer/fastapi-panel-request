#!/bin/bash --login

conda activate panel

cd /app/src

ROOT_PATH=${ROOT_PATH:-}

echo "Root path: $ROOT_PATH"

fastapi run --port 8080 --root-path="${ROOT_PATH}" main.py
