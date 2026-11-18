# Bibliothèque de design systems

Des design systems (polices, couleurs, icônes) à réutiliser dans mes projets. Un dossier par design system, identifié par un **nom court en minuscules** ; sa fiche `design-system.json` décrit l'ambiance, la source et la licence.

## Catalogue

| Nom | Ambiance | Tags | Source | Aperçu |
|---|---|---|---|---|
| [**Poulayo**](./poulayo/) — Vert forêt profond et orange vif sur fond crème : un style chaleureux et rassurant pour une application mobile de terrain (élevage avicole). | chaleureux, naturel, rassurant | agriculture, mobile-first, gestion, accessible | Création originale | [voir](./poulayo/preview/index.html) |

## Réutiliser un design system dans un autre projet

```bash
# copie le design system « poulayo » dans ../mon-projet/design-system/poulayo/
python tools/use.py poulayo ../mon-projet
```

Puis, dans le projet : `<link rel="stylesheet" href="design-system/poulayo/css/fonts.css">` et `…/css/tokens.css`. Les tokens JSON (`tokens/`) servent pour Tailwind, Style Dictionary ou Figma.

## Ajouter un design system

1. `cp -r _template mon-nom` : le nom du dossier est son identifiant (minuscules, chiffres, tirets ; court et mémorable).
2. Remplir `design-system.json` (nom, description, ambiance, tags, **source**, licence, couleurs clés), puis les polices, tokens, icônes et `NOTICE.md`.
3. `python tools/build_preview.py mon-nom` génère l'aperçu du design system.
4. `python tools/build_catalog.py` met à jour ce catalogue et la galerie `index.html`.

## Règles pour un dépôt public

- Toujours renseigner la **source** : `original` (créé par moi), `inspired` (inspiré d'un site ou produit : indiquer l'URL) ou `third-party` (système publié par un tiers : respecter sa licence).
- On peut recopier des couleurs, des échelles de texte, des rayons et des ombres. On ne recopie **pas** des polices payantes, ni les icônes ou illustrations d'un autre produit sans licence qui l'autorise : on référence le nom de la police ou le lien à la place.
- Chaque dossier garde ses licences tierces dans son `NOTICE.md`.

## Outils

- `tools/build_catalog.py` : catalogue (README, galerie, `catalog.json`).
- `tools/build_preview.py <dossier>` : aperçu d'un design system.
- `tools/use.py <nom> <projet>` : copie un design system dans un projet.
- `_template/` : dossier de départ.

_Ce fichier est généré par `tools/build_catalog.py` : ne le modifiez pas à la main._
