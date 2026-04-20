# Programme de formation Python intermédiaire - 3 jours

## Positionnement
- Niveau : intermédiaire
- Public : participants ayant déjà vu les bases Python et souhaitant automatiser des traitements de données métier
- Angle pédagogique : notebook pour explorer, script `.py` pour industrialiser
- Stack officielle : `polars` + `Altair` + `requests`

## Objectifs pédagogiques
À l'issue de la formation, les participants sauront :
- lire des fichiers `CSV` et `Excel` avec `Polars` ;
- nettoyer et transformer des données en ajoutant des colonnes dérivées ;
- produire des contrôles qualité et des graphiques simples dans un notebook ;
- transformer un notebook d'exploration en script Python exécutable ;
- consommer une API et fusionner les données externes avec un fichier local ;
- travailler dans une arborescence entreprise avec `input/`, `output/`, `secret/` et `libs/`.

## Packages et environnement
- Python `3.12+`
- VS Code + extension Python + extension Jupyter
- `polars`
- `polars[rtcompat]` pour une compatibilité CPU plus large sur les postes hétérogènes
- `fastexcel` pour la lecture Excel
- `xlsxwriter` pour l'écriture Excel
- `altair`
- `jupyter`
- `requests`

## Règles pédagogiques à figer
- `import polars as pl`
- aucun `import pandas as pd` dans le parcours normal
- `Polars` en API eager d'abord
- notebooks conservés pour l'exploration et la visualisation
- `Altair` comme stack officielle de graphiques
- transformation par ajout de colonnes dérivées
- pas d'écrasement destructif des colonnes sources par défaut

## Déroulé détaillé

### Jour 1 matin - Notebook + prise en main de Polars
**Contenu**
- différence entre notebook et script `.py`
- création d'un notebook dans VS Code
- lecture `CSV` avec `pl.read_csv`
- découverte du `DataFrame` Polars
- inspection des données : aperçu, schéma, types, nulls
- premières opérations : `select`, `filter`, `head`, `sort`

**Atelier**
- ouvrir un export métier brut
- identifier les colonnes utiles
- repérer les lignes incohérentes ou incomplètes

**Compétences visées**
- lire un fichier brut
- comprendre la structure des données
- faire des filtres simples sans casser le jeu source

### Jour 1 après-midi - Nettoyage et colonnes dérivées avec Polars
**Contenu**
- création de colonnes avec `with_columns`
- transformations texte : trim, lower, replace
- conversions de types
- gestion des `null`
- normalisation de montants, dates, statuts
- principe de colonnes dérivées et conservation des colonnes sources

**Atelier**
- créer :
  - `email_clean`
  - `montant_net`
  - `statut_normalise`
  - `ligne_valide`

**Compétences visées**
- construire un pipeline de transformation lisible
- séparer donnée source et donnée transformée
- isoler les anomalies

### Jour 2 matin - Contrôle qualité et visualisation notebook
**Contenu**
- comptages et synthèses : `group_by`, `agg`, `len`, `sum`, `mean`
- détection de doublons
- indicateurs qualité simples
- graphiques `Altair` sur données `Polars`
- lecture avant / après transformation

**Atelier**
- produire un mini diagnostic qualité
- créer 2 à 3 graphiques utiles :
  - répartition des statuts
  - nombre d'anomalies
  - volumétrie par catégorie ou équipe

**Compétences visées**
- rendre les transformations visibles
- justifier les nettoyages par des indicateurs
- utiliser le notebook comme outil d'analyse, pas comme livrable final unique

### Jour 2 après-midi - Excel avec Polars + passage notebook -> script
**Contenu**
- lecture Excel avec `pl.read_excel`
- écriture Excel avec `write_excel`
- dépendances Excel :
  - lecture via moteur externe (`fastexcel`)
  - écriture via `xlsxwriter`
- structuration du code en fonctions
- `main()`
- `if __name__ == "__main__":`
- organisation projet : `input/`, `output/`, `secret/`, `libs/`

**Atelier**
- prendre une logique validée en notebook
- la transformer en script `.py` rejouable
- produire un fichier final + un fichier d'anomalies

**Compétences visées**
- sortir du mode exploration
- livrer un traitement exécutable par l'équipe
- garder une architecture simple et propre

### Jour 3 matin - API + JSON + enrichissement avec Polars
**Contenu**
- appels HTTP avec `requests`
- lecture JSON
- transformation JSON -> `Polars DataFrame`
- `join` entre données API et données locales
- gestion minimale des erreurs : `timeout`, codes HTTP, `try/except`
- token et règles `secret/`

**Atelier**
- enrichir un fichier métier avec une API
- produire une table consolidée exploitable

**Compétences visées**
- intégrer une source externe proprement
- manipuler JSON sans repasser par `pandas`
- produire un résultat final cohérent

### Jour 3 après-midi - Industrialisation légère + IA + bonus Polars
**Contenu**
- finalisation du script métier
- workflow entreprise avec `input/`, `output/`, `secret/`
- usage de Gemini / Copilot dans un cadre propre
- exclusions de contexte
- relecture et correction du code généré
- bonus si rythme suffisant :
  - introduction courte au lazy API de Polars
  - packaging simple avec `PyInstaller`

**Atelier final**
- notebook d'analyse
- script final
- export propre
- `README_execution.md`

**Compétences visées**
- livrer un traitement propre
- encadrer l'usage de l'IA
- comprendre qu'un notebook sert à explorer et un script sert à produire

## Livrables attendus
- `analyse_metier.ipynb`
- `script_final.py`
- un export transformé
- un fichier d'anomalies
- `README_execution.md`

## Hors périmètre
- pas de `pandas`
- pas de POO avancée
- pas de lazy API en tronc commun
- pas de streaming avancé
- pas de machine learning

## Validation pédagogique
- lecture `CSV` et `Excel` en `Polars`
- création de colonnes dérivées sans modifier la source
- notebook avec graphiques simples et lisibles
- script `.py` reprenant une logique validée en notebook
- fusion d'un jeu API avec un fichier local
