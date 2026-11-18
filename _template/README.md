# Design system « NOM DU PROJET »

> Dossier modèle : copiez-le sous le **nom court du design system** (`cp -r _template mon-nom`, en minuscules, chiffres et tirets), remplissez les fichiers ci-dessous, puis générez l'aperçu et le catalogue.

## Organisation

```
design-system.json  fiche d'identité (nom, ambiance, tags, SOURCE, licence, couleurs clés)
fonts/            polices auto-hébergées (woff2) + leur licence
css/fonts.css     @font-face
css/tokens.css    variables CSS (--ds-couleur-nom, rayons, ombres…)
tokens/           colors.json, typography.json, shape.json (mêmes valeurs, en JSON)
icons/            un sous-dossier par jeu d'icônes (lucide/, maison/…), fichiers .svg
preview/          index.html, généré
NOTICE.md         licences des éléments tiers (polices, icônes)
```

## À faire pour un nouveau projet

1. Copier ce dossier et le renommer (le nom du dossier = l'identifiant, égal au champ `id` de la fiche).
1b. Remplir `design-system.json` : surtout la **source** et la licence.
2. Déposer les polices dans `fonts/` et décrire leur `@font-face` dans `css/fonts.css`.
3. Renseigner les couleurs dans `tokens/colors.json` (groupe → nom → `value`, `role`, `usage` facultatif), puis les reporter en variables dans `css/tokens.css`.
4. Renseigner `tokens/typography.json` et `tokens/shape.json`.
5. Déposer les icônes `.svg` dans `icons/<jeu>/` (24×24, `stroke="currentColor"` pour qu'elles prennent la couleur du texte).
6. Mettre à jour `NOTICE.md` avec les licences.
7. Générer l'aperçu depuis la racine du dépôt :
   ```bash
   python tools/build_preview.py mon-nom --title "Design system Mon nom"
   ```
8. Mettre à jour le catalogue : `python tools/build_catalog.py` (README et galerie `index.html` de la racine).

## Règles de nommage

- Variables CSS : `--ds-<groupe>-<nom>` (ex. `--ds-brand-green`).
- Couleur de texte : toujours indiquer le contraste visé (≥ 4,5:1 sur le fond prévu).
- Tailles de texte en `rem`, pour que la taille de base de la page pilote tout.
