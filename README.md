# Design system

Polices, couleurs et icônes extraits de l'application **Poulayo** (gestion d'élevage avicole, mobile-first), pour les réutiliser dans d'autres projets.

Ouvrez `preview/index.html` dans un navigateur pour tout voir : pastilles de couleurs, échelle de texte, 100 icônes et 8 illustrations (toucher un élément copie sa valeur).

## Contenu

```
fonts/            Nunito variable (latin + latin-ext, woff2) et sa licence OFL
css/fonts.css     @font-face de Nunito
css/tokens.css    variables CSS : couleurs, rayons, ombres, tailles de texte, tactile, focus
tokens/           les mêmes valeurs en JSON (colors, typography, shape) pour Style Dictionary, Figma Tokens, Tailwind…
icons/lucide/     100 icônes Lucide utilisées par l'app (SVG 24×24, currentColor)
icons/species/    8 illustrations d'espèces de volailles (SVG 64×64)
icons/*.json      index des icônes (nom, fichier, composant Lucide)
preview/          page de démonstration autonome
```

## Utilisation rapide

**Web (CSS)**

```html
<link rel="stylesheet" href="design-system/css/fonts.css">
<link rel="stylesheet" href="design-system/css/tokens.css">
```

```css
.bouton { background: var(--brand-green); color: #fff; border-radius: var(--ds-radius-lg); font-family: var(--font-brand); }
.alerte { background: var(--ds-warning-bg-alert); border: 1.5px solid var(--ds-warning-border); color: var(--ds-warning-text); }
```

**Tailwind** : importez `tokens/colors.json` dans `tailwind.config.js` (`theme.extend.colors`) en lisant `colors.<groupe>.<nom>.value`.

**Icônes React** : `npm i lucide-react@0.475.0`, puis `import { Wheat } from 'lucide-react'` (le champ `lucideComponent` de `icons/lucide-icons.json` donne le nom). Les SVG du dossier servent hors React (HTML, Figma, Flutter, e-mails).

## Principes de la charte

- **Vert `#193C2B`** = marque, texte principal, boutons primaires. **Orange `#E46D2E`** = accent (rubrique active, bouton « + »).
- Pour du **texte orange**, utiliser `#B04A0C` (contraste ≥ 4,5:1) ; pour un gros bouton orange sur fond clair, `#C34D0D` avec texte blanc.
- Fond de page chaud `#FFFDF8`, cartes blanches, bordures `#E0E7E3`.
- Une seule police, **Nunito**. Tout est dimensionné en `rem` : changer la taille de base de la page (100 / 115 / 130 %) agrandit tout le texte.
- **Mobile-first** : zones tactiles ≥ 44 px, champs à 16 px minimum (évite le zoom iOS), focus orange de 3 px, contraste ≥ 4,5:1, respect de `prefers-reduced-motion` et `prefers-contrast`.
- Couleurs d'état : succès vert, erreur rouge, avertissement orange/ambre, information bleu. Chaque famille a un texte, un fond pâle et une bordure.
- Boutons d'action rapide : rouge (perte), vert (vente), orange (alimentation, œufs), bleu (dépense) — fond pâle, texte foncé, bordure assortie.

## Origine et mesures

Les valeurs viennent du code de Poulayo (`saas/web-admin`, `index.css` et composants). Le champ `usage` de `tokens/colors.json` compte les occurrences relevées dans le code : les couleurs très utilisées sont celles à reprendre en priorité ; les autres sont des variantes.

## Licences

- Nunito : SIL Open Font License 1.1 (`fonts/OFL-Nunito.txt`).
- Icônes Lucide : ISC (voir `NOTICE.md`).
- Illustrations d'espèces, couleurs et tokens : créés pour Poulayo.
