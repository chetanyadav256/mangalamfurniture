#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/home/ubuntu/chetanshop"
VENV_DIR="$APP_DIR/.venv"

cd "$APP_DIR"

git fetch --all
if git rev-parse --verify main >/dev/null 2>&1; then
  git checkout main
  git pull --ff-only origin main
else
  git pull --ff-only origin master
fi

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
pm2 startOrReload ecosystem.config.js --update-env
pm2 save
