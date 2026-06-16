#!/usr/bin/env python3
"""
Convert plain `[Author Year]` citations to Pandoc superscript-link form
`^[N](#ref-N)^` in every dimension file of a SOTA cache.

Usage:
    convert-citations.py \\
        --cache-dir <path-to-.sota-cache/<slug>>/ \\
        --citation-map <path-to-citation-map.tsv> \\
        [--dry-run]

The citation map is a tab-separated file with one mapping per line:

    [Wei et al. 2022]\\t35
    [DeepMind 2024]\\t9
    [Anthropic 2026]\\t4
    ...

The script handles composite citations of the form `[A; B; C]` by
splitting on `;` and looking up each piece independently, joining
the resulting superscripts with `, ` in the output.

Markdown links of the form `[text](url)` are left untouched.

Unmapped citations are reported to stderr and left as plain text
for manual review; the script's exit code is non-zero if any
unmapped form remains.
"""
import argparse
import re
import sys
from pathlib import Path


CITATION_RE = re.compile(r"\[([^\[\]]+?)\]")


def load_citation_map(path: Path) -> dict[str, int]:
    """Parse a tab-separated [Author Year] -> N map."""
    m: dict[str, int] = {}
    for ln, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        if "\t" not in line:
            print(f"  warn: line {ln} has no tab: {line!r}", file=sys.stderr)
            continue
        key, n_str = line.split("\t", 1)
        key = key.strip()
        # accept both "[Wei et al. 2022]" and "Wei et al. 2022" in the map
        if key.startswith("[") and key.endswith("]"):
            key = key[1:-1]
        try:
            m[key.strip()] = int(n_str.strip())
        except ValueError:
            print(f"  warn: line {ln} has non-int ref: {n_str!r}", file=sys.stderr)
    return m


def convert_one(inner: str, cmap: dict[str, int], unmapped: set[str]) -> str:
    """Convert a single `[...]` content. Composite (split on `;`) supported."""
    pieces = [p.strip() for p in inner.split(";")]
    out = []
    for p in pieces:
        if p in cmap:
            n = cmap[p]
            out.append(f"^[{n}](#ref-{n})^")
            continue
        # tolerate trailing year-suffix variants like "Anthropic 2026a"
        # by trying the base form
        if re.match(r".*\d{4}[a-z]$", p):
            base = p[:-1]
            if base in cmap:
                n = cmap[base]
                out.append(f"^[{n}](#ref-{n})^")
                continue
        unmapped.add(p)
        out.append(f"[{p}]")  # leave for manual review
    return ", ".join(out)


def transform(text: str, cmap: dict[str, int], unmapped: set[str]) -> tuple[str, int]:
    """Run the substitution. Returns (new_text, n_substitutions)."""
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        inner = m.group(1).strip()
        # Skip markdown links: `[text](url)` — match starts with `[` and the
        # *next* char after `]` is `(`. The regex already excludes `[` and `]`
        # in `inner`, but we still need to detect the trailing `(`.
        end = m.end()
        if end < len(text) and text[end] == "(":
            return m.group(0)
        # Skip pure-numeric refs like `[1]`, `[N]`, footnote markers
        if not re.search(r"\d{4}", inner):
            return m.group(0)
        count += 1
        return convert_one(inner, cmap, unmapped)

    new = CITATION_RE.sub(repl, text)
    return new, count


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cache-dir", type=Path, required=True,
                    help="Directory containing dimension-D*.md files.")
    ap.add_argument("--citation-map", type=Path, required=True,
                    help="TSV file mapping [Author Year] -> reference number.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Report substitutions without modifying files.")
    args = ap.parse_args()

    if not args.cache_dir.is_dir():
        print(f"error: --cache-dir does not exist: {args.cache_dir}", file=sys.stderr)
        return 2
    if not args.citation_map.is_file():
        print(f"error: --citation-map does not exist: {args.citation_map}", file=sys.stderr)
        return 2

    cmap = load_citation_map(args.citation_map)
    print(f"loaded {len(cmap)} citation mappings")

    files = sorted(args.cache_dir.glob("dimension-D*.md"))
    if not files:
        print(f"error: no dimension-D*.md files in {args.cache_dir}", file=sys.stderr)
        return 2

    unmapped: set[str] = set()
    total = 0
    for f in files:
        body = f.read_text(encoding="utf-8")
        new, count = transform(body, cmap, unmapped)
        total += count
        action = "would write" if args.dry_run else "wrote"
        print(f"  {action} {f.name} ({count} substitutions)")
        if not args.dry_run:
            f.write_text(new, encoding="utf-8")

    print(f"total: {total} substitutions across {len(files)} files")

    if unmapped:
        print(f"\nWARNING: {len(unmapped)} unmapped citation(s) — left as plain text:",
              file=sys.stderr)
        for u in sorted(unmapped):
            print(f"  [{u}]", file=sys.stderr)
        print("\nAdd them to the citation map and re-run, or accept the plain-text form.",
              file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
