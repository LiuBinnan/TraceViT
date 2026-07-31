"""Render arc-steps records as static HTML filmstrips (input -> steps -> output).

Zero-dependency viewer for the `lbn32/arc-steps` dataset: point it at one
config's `train.jsonl` and it writes a browsable static site (an index page
plus one page per task).

Usage:
    python visualize_steps.py data/rearc/train.jsonl
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

# Official ARC color palette (color index -> hex).
PALETTE = {
    0: "#000000",
    1: "#0074d9",
    2: "#ff4136",
    3: "#2ecc40",
    4: "#ffdc00",
    5: "#aaaaaa",
    6: "#f012be",
    7: "#ff851b",
    8: "#7fdbff",
    9: "#870c25",
}


def render_grid(grid):
    height = len(grid)
    width = len(grid[0]) if height else 0
    max_dim = max(height, width, 1)
    px = max(4, min(12, 240 // max_dim))
    rows = "".join(
        "<tr>" + "".join(f'<td class="c{int(v)}"></td>' for v in row) + "</tr>"
        for row in grid
    )
    return f'<table class="g" style="--s:{px}px"><tbody>{rows}</tbody></table>'


def frame_labels(n_steps):
    if n_steps == 0:
        return ["input", "output"]
    return ["input"] + [f"step {i}" for i in range(1, n_steps)] + ["output"]


def render_record(index, record):
    steps = record.get("steps") or []
    if steps:
        chain = [record["input"], *steps]
    else:
        chain = [record["input"], record["output"]]
    labels = frame_labels(len(steps))
    caption = " &middot; ".join(
        [f"r{index}", html.escape(str(record.get("category", ""))), f"{len(steps)} steps"]
    )
    frames = '<span class="arr">&#8594;</span>'.join(
        f'<div class="frame">{render_grid(grid)}<div class="fl">{label}</div></div>'
        for grid, label in zip(chain, labels)
    )
    return (
        f'<div class="rec"><div class="cap">{caption}</div>'
        f'<div class="chain">{frames}</div></div>'
    )


def scan_corpus(path, k, only_tasks=None, progress_every=None):
    """Single streaming pass over a train.jsonl.

    Keeps the first `k` full records per task plus corpus-wide counts, so
    memory stays flat regardless of file size.
    """
    path = Path(path)
    tasks = {}
    source = None
    with path.open() as fh:
        for lineno, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}: invalid JSON on line {lineno}: {exc}")
            if source is None:
                source = rec.get("source", "corpus")
            task_id = rec["task_id"]
            if only_tasks is not None and task_id not in only_tasks:
                continue
            entry = tasks.setdefault(task_id, {"kept": [], "total": 0, "with_steps": 0})
            entry["total"] += 1
            if rec.get("steps"):
                entry["with_steps"] += 1
            if len(entry["kept"]) < k:
                entry["kept"].append(rec)
            if progress_every and lineno % progress_every == 0:
                print(f"[viz] scanned {lineno:,} lines...", flush=True)
    if only_tasks is not None:
        missing = sorted(set(only_tasks) - tasks.keys())
        if missing:
            raise SystemExit(f"Task ids not found in {path.name}: {', '.join(missing)}")
    return dict(sorted(tasks.items())), source


CSS = (
    "body{font-family:system-ui,sans-serif;margin:16px;background:#fafafa;color:#111}"
    "h1{font-size:20px}"
    "nav{margin:8px 0;font-size:14px}"
    "nav a{margin-right:14px}"
    ".meta{color:#555;font-size:13px;margin:4px 0 12px}"
    ".rule{font-size:14px;background:#fff;border:1px solid #ddd;border-radius:4px;"
    "padding:8px 10px;margin:8px 0;max-width:60em}"
    ".rec{border-bottom:1px solid #ddd;padding:8px 0}"
    ".cap{font-size:12px;color:#555;margin-bottom:4px}"
    ".chain{display:flex;align-items:center;gap:8px;overflow-x:auto;padding:2px 0}"
    ".frame{display:flex;flex-direction:column;align-items:center;flex:none}"
    ".fl{font-size:11px;color:#666;margin-top:3px}"
    "table.g{border-collapse:collapse;flex:none}"
    "table.g td{width:var(--s);height:var(--s);padding:0;border:1px solid #444}"
    ".arr{font-size:16px;color:#888;flex:none}"
    "#q{font-size:15px;padding:6px;width:16em;margin:6px 0}"
    "ul.tl{list-style:none;padding:0;columns:4 16em;font-size:14px}"
    "ul.tl li{margin:2px 0}"
    "ul.tl span{color:#777;font-size:12px}"
    + "".join(f".c{k}{{background:{v}}}" for k, v in PALETTE.items())
)

SEARCH_JS = (
    "var q=document.getElementById('q');"
    "var items=Array.prototype.slice.call(document.querySelectorAll('li[data-id]'));"
    "q.addEventListener('input',function(){"
    "var v=q.value.trim().toLowerCase();"
    "items.forEach(function(li){li.style.display=li.dataset.id.indexOf(v)>=0?'':'none'});});"
    "q.addEventListener('keydown',function(e){"
    "if(e.key!=='Enter'){return}"
    "var v=q.value.trim().toLowerCase();"
    "var exact=items.some(function(li){return li.dataset.id===v});"
    "var vis=items.filter(function(li){return li.dataset.id.indexOf(v)>=0});"
    "if(exact){location.href='t/'+v+'.html'}"
    "else if(vis.length===1){location.href='t/'+vis[0].dataset.id+'.html'}});"
)


def page(title, body):
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<title>{html.escape(title)}</title><style>{CSS}</style></head>"
        f"<body>{body}</body></html>"
    )


def render_task_page(source, task_id, entry, prev_id, next_id):
    nav = []
    if prev_id:
        nav.append(f'<a href="{prev_id}.html">&#8592; {prev_id}</a>')
    nav.append('<a href="../index.html">index</a>')
    if next_id:
        nav.append(f'<a href="{next_id}.html">{next_id} &#8594;</a>')
    rule = next((r.get("rule") for r in entry["kept"] if r.get("rule")), None)
    rule_html = f'<div class="rule">{html.escape(rule)}</div>' if rule else ""
    body = (
        f"<h1>{html.escape(source)} &middot; {html.escape(task_id)}</h1>"
        f'<nav>{"".join(nav)}</nav>'
        f'<div class="meta">{entry["total"]} records in corpus &middot; '
        f'{entry["with_steps"]} with steps &middot; '
        f'showing first {len(entry["kept"])} (file order)</div>'
        + rule_html
        + "".join(render_record(i, r) for i, r in enumerate(entry["kept"]))
    )
    return page(f"{source} {task_id}", body)


def render_index(source, tasks):
    total_records = sum(e["total"] for e in tasks.values())
    total_with_steps = sum(e["with_steps"] for e in tasks.values())
    items = "".join(
        f'<li data-id="{html.escape(tid)}"><a href="t/{html.escape(tid)}.html">'
        f'{html.escape(tid)}</a> <span>{e["total"]} records &middot; '
        f'{e["with_steps"]} with steps</span></li>'
        for tid, e in tasks.items()
    )
    body = (
        f"<h1>{html.escape(source)} steps corpus</h1>"
        f'<div class="meta">{len(tasks)} tasks &middot; {total_records} records &middot; '
        f"{total_with_steps} with steps &middot; one page per task</div>"
        '<input id="q" placeholder="filter task id, Enter to open" autofocus>'
        f'<ul class="tl">{items}</ul>'
        f"<script>{SEARCH_JS}</script>"
    )
    return page(f"{source} steps corpus", body)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Render arc-steps records as a static HTML site."
    )
    parser.add_argument("jsonl", type=str, help="path to one config's train.jsonl")
    parser.add_argument("--out-dir", type=str, default=None,
                        help="output directory (default: steps_viz_<config>)")
    parser.add_argument("--tasks", type=str, default=None,
                        help="comma-separated task ids (default: all tasks)")
    parser.add_argument("--records-per-task", type=int, default=10,
                        help="records rendered per task page (default: 10)")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.records_per_task < 1:
        raise SystemExit("--records-per-task must be >= 1")
    path = Path(args.jsonl)
    if not path.is_file():
        raise SystemExit(f"Input file not found: {path}")
    only_tasks = None
    if args.tasks:
        only_tasks = {t.strip() for t in args.tasks.split(",") if t.strip()}
    tasks, source = scan_corpus(
        path, k=args.records_per_task, only_tasks=only_tasks, progress_every=100_000
    )
    out = Path(args.out_dir) if args.out_dir else Path(f"steps_viz_{source}")
    (out / "t").mkdir(parents=True, exist_ok=True)
    task_ids = list(tasks)
    for i, tid in enumerate(task_ids):
        prev_id = task_ids[i - 1] if i > 0 else None
        next_id = task_ids[i + 1] if i < len(task_ids) - 1 else None
        target = out / "t" / f"{tid}.html"
        target.write_text(render_task_page(source, tid, tasks[tid], prev_id, next_id))
    (out / "index.html").write_text(render_index(source, tasks))
    total_records = sum(e["total"] for e in tasks.values())
    print(f"[viz] {len(tasks)} task pages, {total_records:,} records indexed -> {out}")


if __name__ == "__main__":
    main()
