#!/usr/bin/env bash
# Install the semantic-recon skill into every agent CLI found on this machine.
# All three (Claude Code, Codex CLI, Copilot CLI) use the same layout:
#   <config>/skills/<name>/SKILL.md
#
# Default is a symlink so the source stays the single point of truth.
#   ./install.sh            symlink (recommended)
#   ./install.sh --copy     copy instead
#   ./install.sh --uninstall
set -euo pipefail

NAME="semantic-recon"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="${1:---link}"

TARGETS=(
  "$HOME/.claude/skills:Claude Code"
  "$HOME/.codex/skills:Codex CLI"
  "$HOME/.copilot/skills:Copilot CLI"
)

for entry in "${TARGETS[@]}"; do
  dir="${entry%%:*}"
  label="${entry#*:}"
  parent="$(dirname "$dir")"

  if [ ! -d "$parent" ]; then
    printf '%-14s skipped (%s not present)\n' "$label" "$parent"
    continue
  fi

  mkdir -p "$dir"
  dest="$dir/$NAME"

  case "$MODE" in
    --uninstall)
      rm -rf "$dest"
      printf '%-14s removed\n' "$label"
      ;;
    --copy)
      rm -rf "$dest"
      cp -R "$SRC" "$dest"
      printf '%-14s copied  -> %s\n' "$label" "$dest"
      ;;
    *)
      rm -rf "$dest"
      ln -s "$SRC" "$dest"
      printf '%-14s linked  -> %s\n' "$label" "$dest"
      ;;
  esac
done

if [ "$MODE" != "--uninstall" ]; then
  mkdir -p "$HOME/contracts"
  if [ ! -f "$HOME/contracts/INDEX.md" ]; then
    cp "$SRC/templates/INDEX.md" "$HOME/contracts/INDEX.md"
    echo "registry       created -> ~/contracts/INDEX.md"
  else
    echo "registry       exists  -> ~/contracts/INDEX.md"
  fi
fi
