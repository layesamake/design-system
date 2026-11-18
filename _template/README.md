# Design system « NOM DU PROJET »

> Dossier modèle : copiez-le sous le nom du projet (`cp -r _template mon-projet`), remplissez les fichiers ci-dessous, puis générez l'aperçu.

## Organisation

```
fonts/            polices auto-hébergées (woff2) + leur licence
css/fonts.css     @font-face
css/tokens.css    variables CSS (--ds-couleur-nom, rayons, ombres…)
tokens/           colors.json, typography.json, shape.json (mêmes valeurs, en JSON)
icons/            un sous-dossier par jeu d'icônes (lucide/, maison/…), fichiers .svg
preview/          index.html, généré
NOTICE.md         licences des éléments tiers (polices, icônes)
```

## À faire pour un nouveau projet

1. Copier ce dossier et le renommer.
2. Déposer les polices dans `fonts/` et décrire leur `@font-face` dans `css/fonts.css`.
3. Renseigner les couleurs dans `tokens/colors.json` (groupe → nom → `value`, `role`, `usage` facultatif), puis les reporter en variables dans `css/tokens.css`.
4. Renseigner `tokens/typography.json` et `tokens/shape.json`.
5. Déposer les icônes `.svg` dans `icons/<jeu>/` (24×24, `stroke="currentColor"` pour qu'elles prennent la couleur du texte).
6. Mettre à jour `NOTICE.md` avec les licences.
7. Générer l'aperçu depuis la racine du dépôt :
   ```bash
   python tools/build_preview.py mon-projet --title "Design system Mon projet"
   ```
8. Ajouter une ligne au tableau du README racine.

## Règles de nommage

- Variables CSS : `--ds-<groupe>-<nom>` (ex. `--ds-brand-green`).
- Couleur de texte : toujours indiquer le contraste visé (≥ 4,5:1 sur le fond prévu).
- Tailles de texte en `rem`, pour que la taille de base de la page pilote tout.
