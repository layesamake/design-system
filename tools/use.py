#!/usr/bin/env python3
"""Copie un design system de la bibliothèque dans un autre projet.

Usage :   python tools/use.py <nom> <dossier-du-projet> [--dest design-system] [--only fonts,css,tokens,icons]

Crée <projet>/<dest>/<nom>/ (par défaut « design-system/<nom> ») avec les dossiers choisis (tous par défaut, sauf preview)
et NOTICE.md. Ne touche à rien d'autre dans le projet. Python 3 seulement.
"""
import argparse, os, shutil, sys

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, 'reconfigure'):
        _stream.reconfigure(encoding='utf-8')

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ALL_PARTS = ('fonts', 'css', 'tokens', 'icons')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name')
    parser.add_argument('project')
    parser.add_argument('--dest', default='design-system')
    parser.add_argument('--only', default=','.join(ALL_PARTS))
    args = parser.parse_args()

    source = os.path.join(REPO, args.name)
    if args.name.startswith(('_', '.')) or not os.path.exists(os.path.join(source, 'design-system.json')):
        sys.exit(f'Design system introuvable : {args.name} (voir le catalogue dans README.md)')
    parts = [p.strip() for p in args.only.split(',') if p.strip()]
    unknown = [p for p in parts if p not in ALL_PARTS]
    if unknown:
        sys.exit(f'Parties inconnues : {unknown} (choix : {", ".join(ALL_PARTS)})')

    project = os.path.abspath(args.project)
    if not os.path.isdir(project):
        sys.exit(f'Dossier de projet introuvable : {project}')
    target = os.path.join(project, args.dest, args.name)
    if os.path.exists(target):
        sys.exit(f'{target} existe déjà : supprimez-le ou choisissez --dest pour éviter d\'écraser votre copie')

    os.makedirs(target)
    copied = []
    for part in parts:
        src = os.path.join(source, part)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(target, part), ignore=shutil.ignore_patterns('.gitkeep'))
            copied.append(part)
    for extra in ('NOTICE.md', 'design-system.json'):
        if os.path.exists(os.path.join(source, extra)):
            shutil.copy(os.path.join(source, extra), os.path.join(target, extra))

    rel = f'{args.dest}/{args.name}'
    print(f'« {args.name} » copié dans {target} ({", ".join(copied)}).')
    print('\nÀ ajouter dans la page :')
    if 'css' in copied:
        print(f'  <link rel="stylesheet" href="{rel}/css/fonts.css">')
        print(f'  <link rel="stylesheet" href="{rel}/css/tokens.css">')
    print('Les licences tierces sont dans NOTICE.md : gardez-le avec les fichiers.')


if __name__ == '__main__':
    main()
