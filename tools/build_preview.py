#!/usr/bin/env python3
"""Génère la page d'aperçu d'un design system à partir de ses fichiers.

Usage :   python tools/build_preview.py <dossier-du-projet> [--title "Nom affiché"] [--out chemin.html]

Lit, dans le dossier du projet :
  tokens/colors.json       {"colors": {"groupe": {"nom": {"value": "#RRGGBB", "role": "…", "usage": 12}}}}
  tokens/typography.json   {"fontSize": {"nom": {"value": "1rem"}}, "fontWeight": {"nom": {"value": 700}}}   (facultatif)
  icons/**/*.svg           toutes les icônes, regroupées par sous-dossier                                       (facultatif)
  css/fonts.css, css/tokens.css                                                                              (facultatifs)
Écrit preview/index.html (ou --out). Aucune dépendance : Python 3 seulement.
"""
import argparse, html, json, os, re, sys

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, 'reconfigure'):
        _stream.reconfigure(encoding='utf-8')


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def contrast_text(hex_value):
    m = re.fullmatch(r'#([0-9a-fA-F]{6})', hex_value or '')
    if not m:
        return '#000'
    r, g, b = (int(m.group(1)[i:i + 2], 16) for i in (0, 2, 4))
    return '#000' if (r * 299 + g * 587 + b * 114) / 1000 > 150 else '#fff'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('project')
    parser.add_argument('--title', default=None)
    parser.add_argument('--out', default=None)
    args = parser.parse_args()

    root = os.path.abspath(args.project)
    if not os.path.isdir(root):
        sys.exit(f'Dossier introuvable : {root}')
    title = args.title or f'Design system {os.path.basename(root)}'
    out = args.out or os.path.join(root, 'preview', 'index.html')
    css_links = ''.join(
        f'<link rel="stylesheet" href="../css/{name}">\n' for name in ('fonts.css', 'tokens.css')
        if os.path.exists(os.path.join(root, 'css', name))
    )

    sections, nav = [], []

    colors = (load_json(os.path.join(root, 'tokens', 'colors.json')) or {}).get('colors', {})
    if colors:
        parts = []
        total = 0
        for group, items in colors.items():
            parts.append(f'<h3>{html.escape(group)}</h3><div class="swatches">')
            for name, entry in items.items():
                value = entry['value'] if isinstance(entry, dict) else str(entry)
                role = entry.get('role', '') if isinstance(entry, dict) else ''
                total += 1
                parts.append(
                    f'<button class="sw" style="background:{value};color:{contrast_text(value)}" data-copy="{html.escape(value)}" '
                    f'title="{html.escape(role)}"><b>{html.escape(name)}</b><span>{html.escape(value)}</span></button>')
            parts.append('</div>')
        sections.append(f'<h2 id="couleurs">Couleurs ({total})</h2>' + ''.join(parts))
        nav.append(('couleurs', 'Couleurs'))

    typo = load_json(os.path.join(root, 'tokens', 'typography.json')) or {}
    if typo:
        parts = []
        weights = [(k, v) for k, v in typo.get('fontWeight', {}).items() if isinstance(v, dict)]
        sizes = [(k, v) for k, v in typo.get('fontSize', {}).items() if isinstance(v, dict) and 'value' in v]
        if weights:
            parts.append('<h3>Graisses</h3>' + ''.join(
                f'<div class="ty" style="font-weight:{v["value"]};font-size:1.1rem"><code>{html.escape(k)} · {v["value"]}</code> Le texte de démonstration</div>'
                for k, v in weights))
        if sizes:
            parts.append('<h3>Échelle de tailles</h3>' + ''.join(
                f'<div class="ty" style="font-size:{v["value"]}"><code>{html.escape(k)} · {v["value"]}</code> Le texte de démonstration</div>'
                for k, v in sizes))
        if parts:
            sections.append('<h2 id="polices">Polices</h2>' + ''.join(parts))
            nav.append(('polices', 'Polices'))

    icons_dir = os.path.join(root, 'icons')
    if os.path.isdir(icons_dir):
        groups = {}
        for dirpath, _, files in os.walk(icons_dir):
            for name in sorted(files):
                if name.lower().endswith('.svg'):
                    rel_group = os.path.relpath(dirpath, icons_dir)
                    groups.setdefault(rel_group if rel_group != '.' else 'icônes', []).append(os.path.join(dirpath, name))
        for group, paths in sorted(groups.items()):
            anchor = 'icones-' + re.sub(r'[^a-z0-9]+', '-', group.lower())
            tiles = []
            for path in paths:
                svg = open(path, encoding='utf-8').read().strip()
                label = os.path.splitext(os.path.basename(path))[0]
                tiles.append(f'<button class="ic" data-copy="{html.escape(label)}" title="{html.escape(label)}">{svg}<span>{html.escape(label)}</span></button>')
            sections.append(f'<h2 id="{anchor}">Icônes : {html.escape(group)} ({len(paths)})</h2><div class="icons">{"".join(tiles)}</div>')
            nav.append((anchor, f'Icônes {group}'))

    nav_html = ''.join(f'<a href="#{a}">{html.escape(t)}</a>' for a, t in nav)
    page = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
{css_links}<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0 auto; padding: 0 16px 60px; max-width: 1100px; font-family: var(--font-brand, system-ui, sans-serif); color: #222; background: #fff; }}
  h1 {{ margin: 0; padding-top: 28px; font-size: 1.8rem; }}
  h2 {{ margin: 40px 0 6px; font-size: 1.35rem; border-bottom: 2px solid #ddd; padding-bottom: 6px; }}
  h3 {{ margin: 22px 0 8px; font-size: .8rem; text-transform: uppercase; letter-spacing: .08em; color: #666; }}
  p.lead {{ color: #666; margin: 4px 0 0; }}
  nav a {{ margin-right: 14px; font-weight: 700; }}
  .swatches {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 8px; }}
  .sw {{ border: 1px solid rgba(0,0,0,.12); border-radius: 12px; padding: 14px 10px; min-height: 76px; text-align: left; font: inherit; cursor: pointer; display: flex; flex-direction: column; gap: 2px; }}
  .sw b {{ font-size: .85rem; }} .sw span {{ font-size: .78rem; font-family: monospace; }}
  .icons {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(96px, 1fr)); gap: 8px; }}
  .ic {{ border: 1px solid #ddd; background: #fff; border-radius: 12px; padding: 12px 4px 8px; display: flex; flex-direction: column; align-items: center; gap: 6px; font: inherit; cursor: pointer; color: inherit; }}
  .ic svg {{ width: 32px; height: 32px; }} .ic span {{ font-size: .7rem; color: #666; word-break: break-all; text-align: center; }}
  .ty {{ padding: 6px 0; border-bottom: 1px dashed #ddd; }}
  .ty code {{ display: inline-block; min-width: 150px; font-size: .72rem; color: #666; font-weight: 400; }}
  #toast {{ position: fixed; bottom: 16px; left: 50%; transform: translateX(-50%); background: #222; color: #fff; padding: 10px 18px; border-radius: 999px; font-weight: 700; opacity: 0; transition: opacity .2s; pointer-events: none; }}
  #toast.on {{ opacity: 1; }}
</style>
</head>
<body>
<header>
  <h1>{html.escape(title)}</h1>
  <p class="lead">Touchez une couleur ou une icône pour copier sa valeur ou son nom.</p>
  <nav aria-label="Sections">{nav_html}</nav>
</header>
{''.join(sections)}
<div id="toast" role="status" aria-live="polite"></div>
<script>
  const toast = document.getElementById('toast');
  document.addEventListener('click', (e) => {{
    const el = e.target.closest('[data-copy]'); if (!el) return;
    if (navigator.clipboard) navigator.clipboard.writeText(el.dataset.copy).catch(() => {{}});
    toast.textContent = 'Copié : ' + el.dataset.copy; toast.classList.add('on'); setTimeout(() => toast.classList.remove('on'), 1400);
  }});
</script>
</body>
</html>
"""
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(page)
    print(f'Aperçu écrit : {out} ({len(sections)} sections)')


if __name__ == '__main__':
    main()
