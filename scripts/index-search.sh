#!/usr/bin/env bash
# Build a Pagefind index and copy it to static/pagefind so hugo server can
# serve /pagefind/. hugo server does not run Pagefind. Re-run this after
# content changes. GitHub Actions indexes public/ itself and does not use
# this copy.
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="${HOME}/.local/bin:${PATH}"
dest="$(mktemp -d)"
trap 'rm -rf "$dest"' EXIT
hugo --destination "$dest" --cleanDestinationDir
npx --yes pagefind@1.5.2 --site "$dest"
rm -rf static/pagefind
cp -a "$dest/pagefind" static/pagefind
echo "Indexed search into static/pagefind"
