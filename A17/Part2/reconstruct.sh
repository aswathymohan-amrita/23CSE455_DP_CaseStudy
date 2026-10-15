#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: bash Part2/reconstruct.sh /absolute/output/checkout" >&2
  exit 2
fi

case "$1" in
  /*) ;;
  *) echo "Use an absolute output path" >&2; exit 2 ;;
esac
if [ -e "$1" ]; then
  echo "Output path already exists: $1" >&2
  exit 2
fi

team_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
git clone --branch v1.2026.8 https://github.com/plantuml/plantuml.git "$1"
git -C "$1" checkout --detach 149874a1bb2b64c42889d7178cb89f6647ac14bc
for i in 1 2 3; do
  git -C "$1" apply --check "$team_dir/Part2/changes/Change$i/change.patch"
  git -C "$1" apply "$team_dir/Part2/changes/Change$i/change.patch"
done
echo "Reconstructed final source at $1"
echo "Run: cd $1 && GPL_ONLY=1 bash gradlew jar test -Pfast --console=plain"
