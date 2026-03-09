# Programme de formation Python débutant (Entreprise)

## Informations générales
- **Durée** : 4 jours (28h)
- **Public** : 6 participants débutants
- **Objectif** : rendre les participants capables de produire des scripts utiles au quotidien (automatisation, traitement de données, reporting, intégration fichiers/API)
- **Format pédagogique** : 30% théorie / 70% pratique

## Disponibilités du formateur
- **Semaine 11** : du 9 au 12 mars
- **Semaine 23** : du 1er au 4 juin

## Prérequis de cadrage (à valider avant la session)
- Équipe/service des 6 salariés (finance, opérations, RH, commercial, support, data, etc.)
- Niveau initial (débutants complets ou déjà un peu de code)
- 3 à 5 cas d'usage concrets à automatiser/améliorer
- Formats de données et outils utilisés (Excel/CSV/JSON/BDD, Power BI, ERP, CRM)
- Volumétrie typique des données
- Environnement IT (Windows/Mac, droits d'installation, accès internet/proxy, outil souhaité : VS Code/Jupyter)
- Livrables attendus (attestation, évaluation, support, script réutilisable)

## Organisation pédagogique
- **Rythme recommandé** : 7h/jour (3h30 matin + 3h30 après-midi)
- **Approche** : exercices sur données proches du métier
- **Fil rouge** : mini-projet métier progressif de J1 à J4

## Déroulé détaillé

### Jour 1 - Démarrage rapide + bases solides
**Objectifs**
- Installer et lancer un environnement Python de travail
- Comprendre les bases de syntaxe et de structure d'un script

**Contenu**
- Installation et prise en main : Python, `venv`, `pip`, VS Code, exécution de scripts
- Syntaxe essentielle : variables, types, chaînes, opérations, conditions
- Bonnes pratiques : lisibilité, nommage, structure minimale d'un script

**Atelier entreprise**
- Transformer une tâche manuelle simple en script
- Exemples : renommer/organiser des fichiers, calculs, formatage

**Livrable du jour**
- Script simple exécutable + consignes d'exécution

---

### Jour 2 - Automatisation et manipulation de données
**Objectifs**
- Automatiser des traitements répétitifs
- Structurer du code avec des fonctions

**Contenu**
- Boucles, listes/dictionnaires, tri/filtrage, compréhensions
- Fonctions : réutiliser le code et éviter les copier-coller
- Fichiers : lecture/écriture texte, chemins, dossiers (`pathlib`)

**Atelier entreprise**
- Traitement d'un export CSV : nettoyage + calcul de KPI + génération d'un fichier de sortie

**Livrable du jour**
- Script de traitement de données structuré en fonctions

---

### Jour 3 - CSV/Excel/JSON + API (selon besoin)
**Objectifs**
- Savoir ingérer et transformer les formats de données métier
- Récupérer des données via API et produire un rapport

**Contenu**
- CSV/JSON : lecture, écriture, transformations
- Excel :
  - Option A : `pandas` + `openpyxl` (usage entreprise efficace)
  - Option B : approche light sans pandas (`csv` + xlsx minimal)
- APIs avec `requests` : GET/POST, pagination, authentification par token, gestion d'erreurs

**Atelier entreprise**
- Récupérer des données (fichier ou API), transformer, produire un rapport CSV/Excel

**Livrable du jour**
- Pipeline de collecte/transformation + rapport généré

---

### Jour 4 - Robustesse + mini-projet métier + industrialisation légère
**Objectifs**
- Fiabiliser les scripts
- Livrer un résultat réutilisable par l'équipe

**Contenu**
- Gestion d'erreurs (`try/except`), validations, logs (`logging`)
- Paramétrage d'un script (`argparse`) et configuration (`.env`)
- Mini-projet adapté au métier : conception -> implémentation -> restitution

**Atelier entreprise**
- Réalisation complète du mini-projet fil rouge

**Livrable final**
- Script réutilisable
- Guide d'exécution
- Bonnes pratiques appliquées

## Mini-projet fil rouge (structure)
- **Entrée** : export métier (CSV/Excel/JSON) ou API
- **Traitements** : nettoyage, règles métier, calcul d'indicateurs
- **Sortie** : rapport CSV/Excel + logs
- **Exécution** : script paramétrable en ligne de commande
- **Documentation** : README d'usage interne

## Évaluation
- Diagnostic initial (niveau de départ)
- Évaluation continue sur les ateliers
- Restitution du mini-projet en fin de J4
- Bilan de compétences individuel (si demandé)

## Livrables possibles côté formation
- Support de cours
- Scripts et exercices réalisés
- Mini-projet final réutilisable
- Grille d'évaluation / attestation
