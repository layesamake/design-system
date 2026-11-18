# Design systems

Polices, couleurs et icônes réutilisables, un dossier par projet.

| Dossier | Projet | Contenu |
|---|---|---|
| [`poulayo/`](poulayo/) | Poulayo (gestion d'élevage avicole, mobile-first) | Nunito, 75 couleurs, 100 icônes Lucide, 8 illustrations d'espèces, aperçu HTML |

## Ajouter un projet

1. Copier le modèle : `cp -r _template mon-projet` (voir [`_template/README.md`](_template/README.md) pour le détail).
2. Remplir les polices, tokens, icônes et `NOTICE.md`.
3. Générer l'aperçu : `python tools/build_preview.py mon-projet --title "Design system Mon projet"` (Python 3 seulement, aucune dépendance).
4. Ajouter une ligne au tableau ci-dessus.

## Outils

- [`tools/build_preview.py`](tools/build_preview.py) : génère `preview/index.html` d'un projet à partir de ses `tokens/` et de ses `icons/`.
- [`_template/`](_template/) : dossier de départ vide.
