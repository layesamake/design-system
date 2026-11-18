#!/usr/bin/env python3
"""Génère le catalogue de la bibliothèque : README.md, index.html (galerie) et catalog.json.

Usage (depuis la racine du dépôt) :   python tools/build_catalog.py

Chaque design system est un dossier à la racine contenant un `design-system.json` (voir _template/).
Les dossiers dont le nom commence par « _ » ou « . » sont ignorés. Python 3 seulement.
"""
import html, json, os, re, sys

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, 'reconfigure'):
        _stream.reconfigure(encoding='utf-8')

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REQUIRED = ('id', 'name', 'description', 'source', 'license', 'keyColors')
SOURCE_TYPES = {'original': 'Création originale', 'inspired': 'Inspiré de', 'third-party': 'Système tiers'}
SLUG = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')


def load_entries():
    entries, errors = [], []
    for name in sorted(os.listdir(REPO)):
        folder = os.path.join(REPO, name)
        manifest = os.path.join(folder, 'design-system.json')
        if name.startswith(('_', '.')) or not os.path.isdir(folder) or not os.path.exists(manifest):
            continue
        with open(manifest, encoding='utf-8') as f:
            data = json.load(f)
        missing = [k for k in REQUIRED if k not in data]
        if missing:
            errors.append(f'{name}: champs manquants {missing}')
            continue
        if data['id'] != name:
            errors.append(f'{name}: « id » ({data["id"]}) doit être égal au nom du dossier')
            continue
        if not SLUG.match(name):
            errors.append(f'{name}: nom de dossier en minuscules, chiffres et tirets seulement')
            continue
        data['preview'] = os.path.exists(os.path.join(folder, 'preview', 'index.html'))
        entries.append(data)
    return entries, errors


def source_label(entry):
    src = entry['source']
    label = SOURCE_TYPES.get(src.get('type'), src.get('type', ''))
    if src.get('url'):
        label += f' : {src["url"]}'
    return label


def contrast_text(hex_value):
    m = re.fullmatch(r'#([0-9a-fA-F]{6})', hex_value)
    if not m:
        return '#000'
    r, g, b = (int(m.group(1)[i:i + 2], 16) for i in (0, 2, 4))
    return '#000' if (r * 299 + g * 587 + b * 114) / 1000 > 150 else '#fff'


def build_readme(entries):
    lines = [
        '# Bibliothèque de design systems', '',
        'Des design systems (polices, couleurs, icônes) à réutiliser dans mes projets. Un dossier par design system, identifié par un **nom court en minuscules** ; sa fiche `design-system.json` décrit l\'ambiance, la source et la licence.', '',
        '## Catalogue', '',
        '| Nom | Ambiance | Tags | Source | Aperçu |', '|---|---|---|---|---|',
    ]
    for e in entries:
        link = f'[voir](./{e["id"]}/preview/index.html)' if e['preview'] else '—'
        lines.append(f'| [**{e["name"]}**](./{e["id"]}/) — {e["description"]} | {", ".join(e.get("mood", []))} | {", ".join(e.get("tags", []))} | {source_label(e)} | {link} |')
    if not entries:
        lines.append('| _(aucun pour l\'instant)_ | | | | |')
    lines += [
        '', '## Réutiliser un design system dans un autre projet', '',
        '```bash',
        '# copie le design system « poulayo » dans ../mon-projet/design-system/poulayo/',
        'python tools/use.py poulayo ../mon-projet',
        '```', '',
        'Puis, dans le projet : `<link rel="stylesheet" href="design-system/poulayo/css/fonts.css">` et `…/css/tokens.css`. Les tokens JSON (`tokens/`) servent pour Tailwind, Style Dictionary ou Figma.', '',
        '## Ajouter un design system', '',
        '1. `cp -r _template mon-nom` : le nom du dossier est son identifiant (minuscules, chiffres, tirets ; court et mémorable).',
        '2. Remplir `design-system.json` (nom, description, ambiance, tags, **source**, licence, couleurs clés), puis les polices, tokens, icônes et `NOTICE.md`.',
        '3. `python tools/build_preview.py mon-nom` génère l\'aperçu du design system.',
        '4. `python tools/build_catalog.py` met à jour ce catalogue et la galerie `index.html`.', '',
        '## Règles pour un dépôt public', '',
        '- Toujours renseigner la **source** : `original` (créé par moi), `inspired` (inspiré d\'un site ou produit : indiquer l\'URL) ou `third-party` (système publié par un tiers : respecter sa licence).',
        '- On peut recopier des couleurs, des échelles de texte, des rayons et des ombres. On ne recopie **pas** des polices payantes, ni les icônes ou illustrations d\'un autre produit sans licence qui l\'autorise : on référence le nom de la police ou le lien à la place.',
        '- Chaque dossier garde ses licences tierces dans son `NOTICE.md`.', '',
        '## Outils', '',
        '- `tools/build_catalog.py` : catalogue (README, galerie, `catalog.json`).',
        '- `tools/build_preview.py <dossier>` : aperçu d\'un design system.',
        '- `tools/use.py <nom> <projet>` : copie un design system dans un projet.',
        '- `_template/` : dossier de départ.', '',
        '_Ce fichier est généré par `tools/build_catalog.py` : ne le modifiez pas à la main._', '',
    ]
    return '\n'.join(lines)


def build_gallery(entries):
    cards = []
    for e in entries:
        swatches = ''.join(
            f'<span class="sw" style="background:{v};color:{contrast_text(v)}" title="{html.escape(k)} {v}"><b>{html.escape(k)}</b>{v}</span>'
            for k, v in e['keyColors'].items())
        tags = ''.join(f'<li>{html.escape(t)}</li>' for t in e.get('mood', []) + e.get('tags', []))
        fonts = ', '.join(e.get('fonts', [])) or '—'
        icons = ', '.join(e.get('icons', [])) or '—'
        preview = f'<a class="btn" href="./{e["id"]}/preview/index.html">Ouvrir l\'aperçu</a>' if e['preview'] else ''
        cards.append(f"""<article class="card" id="{e['id']}">
  <div class="swatches">{swatches}</div>
  <h2>{html.escape(e['name'])} <small><code>{e['id']}</code></small></h2>
  <p>{html.escape(e['description'])}</p>
  <ul class="tags">{tags}</ul>
  <dl><dt>Polices</dt><dd>{html.escape(fonts)}</dd><dt>Icônes</dt><dd>{html.escape(icons)}</dd><dt>Source</dt><dd>{html.escape(source_label(e))}</dd><dt>Licence</dt><dd>{html.escape(e['license'])}</dd></dl>
  <div class="actions">{preview}<button class="btn ghost" data-copy="python tools/use.py {e['id']} ../mon-projet">Copier la commande « utiliser »</button></div>
</article>""")
    empty = '' if entries else '<p>Aucun design system pour l\'instant.</p>'
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bibliothèque de design systems</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0 auto; padding: 0 16px 60px; max-width: 1100px; font-family: system-ui, sans-serif; color: #1b1f1d; background: #fafaf7; }}
  h1 {{ margin: 0; padding-top: 28px; font-size: 1.8rem; }}
  .lead {{ color: #5d665f; margin: 4px 0 20px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }}
  .card {{ background: #fff; border: 1px solid #e3e6e1; border-radius: 16px; padding: 16px; display: flex; flex-direction: column; gap: 8px; }}
  .card h2 {{ margin: 6px 0 0; font-size: 1.25rem; }} .card h2 small {{ font-weight: 400; color: #6b736d; }}
  .card p {{ margin: 0; color: #3b423d; }}
  .swatches {{ display: flex; border-radius: 12px; overflow: hidden; border: 1px solid rgba(0,0,0,.1); min-height: 72px; }}
  .sw {{ flex: 1; padding: 8px 6px; font-size: .68rem; font-family: monospace; display: flex; flex-direction: column; justify-content: flex-end; }}
  .sw b {{ font-family: system-ui, sans-serif; font-size: .7rem; }}
  .tags {{ list-style: none; padding: 0; margin: 0; display: flex; flex-wrap: wrap; gap: 6px; }}
  .tags li {{ background: #eef2ee; border-radius: 999px; padding: 3px 10px; font-size: .78rem; }}
  dl {{ display: grid; grid-template-columns: auto 1fr; gap: 2px 12px; margin: 4px 0 0; font-size: .85rem; }}
  dt {{ color: #6b736d; }} dd {{ margin: 0; overflow-wrap: anywhere; }}
  .actions {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: auto; padding-top: 8px; }}
  .btn {{ min-height: 44px; padding: 0 14px; border-radius: 12px; background: #1b1f1d; color: #fff; text-decoration: none; display: inline-flex; align-items: center; font: inherit; font-weight: 700; border: 0; cursor: pointer; }}
  .btn.ghost {{ background: #eef2ee; color: #1b1f1d; }}
  #toast {{ position: fixed; bottom: 16px; left: 50%; transform: translateX(-50%); background: #1b1f1d; color: #fff; padding: 10px 18px; border-radius: 999px; font-weight: 700; opacity: 0; transition: opacity .2s; pointer-events: none; }}
  #toast.on {{ opacity: 1; }}
</style>
</head>
<body>
<header><h1>Bibliothèque de design systems</h1><p class="lead">{len(entries)} design system{'s' if len(entries) > 1 else ''} : couleurs clés, ambiance, source. Un clic copie la commande pour l'utiliser dans un projet.</p></header>
<main class="grid">
{''.join(cards)}{empty}
</main>
<div id="toast" role="status" aria-live="polite"></div>
<script>
  const toast = document.getElementById('toast');
  document.addEventListener('click', (e) => {{
    const el = e.target.closest('[data-copy]'); if (!el) return;
    if (navigator.clipboard) navigator.clipboard.writeText(el.dataset.copy).catch(() => {{}});
    toast.textContent = 'Copié : ' + el.dataset.copy; toast.classList.add('on'); setTimeout(() => toast.classList.remove('on'), 1600);
  }});
</script>
</body>
</html>
"""


def main():
    entries, errors = load_entries()
    if errors:
        print('Fiches invalides :')
        for err in errors:
            print('  -', err)
        sys.exit(1)
    for name, content in (('README.md', build_readme(entries)), ('index.html', build_gallery(entries))):
        with open(os.path.join(REPO, name), 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
    with open(os.path.join(REPO, 'catalog.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'designSystems': [{k: v for k, v in e.items() if k != 'preview'} for e in entries]}, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(f'Catalogue généré : {len(entries)} design system(s) : {", ".join(e["id"] for e in entries)}')


if __name__ == '__main__':
    main()
