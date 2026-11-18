#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -d "$SCRIPT_DIR/../webapp" ]; then
  WEBAPP_DIR="$SCRIPT_DIR/../webapp"
elif [ -f "$SCRIPT_DIR/../package.json" ]; then
  WEBAPP_DIR="$SCRIPT_DIR/.."
else
  WEBAPP_DIR="$SCRIPT_DIR/../webapp"
fi
WEBAPP_DIR="$(cd "$WEBAPP_DIR" && pwd)"

usage() {
  cat <<USAGE
Usage: $(basename "$0") [-b] [-h]

Options:
  -b    Build the webapp (npm run build)
  -h    Show this help message

With no options, runs the dev server (npm run dev).
USAGE
}

MODE="dev"
while getopts ":bh" opt; do
  case "$opt" in
    b) MODE="build" ;;
    h) usage; exit 0 ;;
    \?) echo "Unknown option: -$OPTARG" >&2; usage; exit 1 ;;
  esac
done

if command -v npm >/dev/null 2>&1; then
  RUNNER="npm"
elif [ -x "$WEBAPP_DIR/node_modules/.bin/vite" ]; then
  RUNNER="local"
else
  echo "npm not found and local Vite not installed. Please install dependencies first." >&2
  exit 1
fi

cd "$WEBAPP_DIR"
case "$MODE" in
  dev)
    if [ "$RUNNER" = "npm" ]; then npm run dev; else ./node_modules/.bin/vite; fi
    ;;
  build)
    if [ "$RUNNER" = "npm" ]; then npm run build; else ./node_modules/.bin/vite build; fi
    ;;
esac
