#!/usr/bin/env bash
#
# Install MatCom AI Skills into a target skills directory.
#
# Usage:
#     ./install.sh                # install to $HOME/.claude/skills/
#     SKILLS_DEST=path ./install.sh   # install to a custom directory
#     ./install.sh --force        # overwrite existing skills
#     ./install.sh --list         # list installable skills, do nothing
#
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_SRC="$REPO_DIR/skills"
SKILLS_DEST="${SKILLS_DEST:-$HOME/.claude/skills}"

FORCE=0
LIST_ONLY=0
for arg in "$@"; do
    case "$arg" in
        --force|-f)   FORCE=1 ;;
        --list|-l)    LIST_ONLY=1 ;;
        --help|-h)
            sed -n '2,/^set/p' "$0" | sed '$d' | sed 's/^# \?//'
            exit 0
            ;;
        *)
            echo "error: unknown argument: $arg" >&2
            echo "try: $0 --help" >&2
            exit 2
            ;;
    esac
done

if [ ! -d "$SKILLS_SRC" ]; then
    echo "error: skills directory not found at $SKILLS_SRC" >&2
    exit 2
fi

if [ "$LIST_ONLY" -eq 1 ]; then
    echo "Skills available in this repo:"
    for skill in "$SKILLS_SRC"/*/; do
        name=$(basename "$skill")
        echo "  - $name"
    done
    echo ""
    echo "Default install destination: $SKILLS_DEST"
    exit 0
fi

mkdir -p "$SKILLS_DEST"

installed=0
skipped=0
for skill in "$SKILLS_SRC"/*/; do
    [ -d "$skill" ] || continue
    name=$(basename "$skill")
    target="$SKILLS_DEST/$name"

    if [ -e "$target" ] && [ "$FORCE" -eq 0 ]; then
        echo "skip: $name (already at $target — use --force to overwrite)"
        skipped=$((skipped + 1))
        continue
    fi

    if [ -e "$target" ] && [ "$FORCE" -eq 1 ]; then
        rm -rf "$target"
    fi

    cp -r "$skill" "$target"
    echo "installed: $name → $target"
    installed=$((installed + 1))
done

echo ""
echo "Done. Installed $installed skill(s); skipped $skipped."
echo "Destination: $SKILLS_DEST"

if [ "$installed" -gt 0 ]; then
    echo ""
    echo "Reload your agent (or restart the session) for the new skills to appear."
fi
