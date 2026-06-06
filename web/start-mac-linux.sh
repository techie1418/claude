#!/usr/bin/env bash
# One-click launcher for Mac/Linux:  double-click or run  ./web/start-mac-linux.sh
cd "$(dirname "$0")/.."
echo "Starting Off-Page SEO tool..."
echo "Open this in your browser:  http://localhost:8000"
python3 web/server.py
