# Plan de cours Python debutant - adapte au cadrage (version allegee 3 jours)

## 1) Contexte valide
- Niveau participants : debutants complets, pas de pratique de code
- Objectif principal : automatisation de taches et traitement de donnees
- Cas cibles : fichiers Excel/CSV + initiation API
- Environnement : Windows + VS Code
- Hors perimetre : graphiques / data visualisation
- Orientation : scripts courts, concrets, reutilisables

## 2) Objectifs pedagogiques finaux (3 blocs)
A la fin de la formation, les participants savent :
- automatiser des traitements sur fichiers CSV/Excel ;
- structurer un script propre avec fonctions et reutilisation ;
- rendre un script fiable (try/except + validations + logs simples).

## 3) Format pedagogique
- Duree : 3 jours (21h)
- Repartition : 30% theorie / 70% pratique
- Approche : exercices metier + mini-projet fil rouge a portee reduite

## 4) Charge pedagogique maitrisee
- Maximum 2 notions nouvelles fortes par demi-journee
- 60% pratique guidee / 40% pratique en autonomie
- Pause de consolidation sur chaque demi-journee : quiz flash + correction collective
- Objectif de fin de journee explicite et livrable concret quotidien

## 5) Deroule detaille (3 jours)

### Jour 1 - Fondations + premier script utile
**Objectif du jour**
- Prendre en main Python dans VS Code
- Ecrire et executer un script simple de bout en bout

**Contenu**
- Installation et execution : Python, venv, pip, VS Code
- Variables, types, conditions, boucles
- Listes/dictionnaires (niveau essentiel)
- Bonnes pratiques minimales : nommage, lisibilite, structure courte

**Atelier**
- Automatiser une tache repetitive simple sur des fichiers

**Livrable**
- 1 script executable + mode d'emploi en 5 lignes

---

### Jour 2 - Donnees metier CSV/Excel
**Objectif du jour**
- Traiter un export metier de facon fiable

**Contenu**
- Fonctions : decouper le script et eviter les copier-coller
- Lecture/ecriture CSV
- Excel (usage simple) : chargement, nettoyage, export
- Controles de base : colonnes attendues, valeurs manquantes

**Atelier**
- Transformer un export metier en fichier de sortie propre (nettoyage + KPI simples)

**Livrable**
- 1 script de traitement reutilisable

---

### Jour 3 - API initiation guidee + robustesse + mini-projet final
**Objectif du jour**
- Integrer une API simple sans complexite excessive
- Livrer un script final exploitable

**Contenu**
- API initiation guidee : GET simple + token + conversion en CSV
- Pas de pagination avancee
- Robustesse : try/except, validations minimales, logging basique
- Parametrage simple du script (arguments essentiels)
- Mini-projet : conception -> implementation -> test -> restitution

**Atelier**
- Mini-projet fil rouge a portee reduite :
  - source principale CSV/Excel
  - option API courte guidee
  - sortie rapport CSV/Excel

**Livrable final**
- `script_final.py`
- `README_execution.md`
- `donnees_exemple.csv`
- `resultat_exemple.csv`

## 6) Contrat de sortie (documentaire)
- Version officielle du plan : 3 jours allege
- Livrables participants obligatoires :
  - `script_final.py`
  - `README_execution.md`
  - `donnees_exemple.csv` / `resultat_exemple.csv`
- Grille d'evaluation finale : competences minimales atteintes / non atteintes

## 7) Cas limites et modes degrades
- Installation bloquee : bascule sur environnement pret a l'emploi
- Acces API indisponible : JSON local de simulation
- Heterogeneite de niveau : binomes pilot / co-pilot
- Retard J2 : API reduite a demonstration + exercice guide

## 8) Evaluation et criteres de validation
- Evaluation continue sur ateliers
- Restitution finale en fin de J3
- Validation sur 4 points :
  - script de base executable
  - traitement CSV/Excel correct
  - initiation API (GET simple + export CSV)
  - robustesse minimale (erreurs + logs)

## 9) Prerequis techniques avant J1
- Python et VS Code installes sur tous les postes Windows
- Installation des bibliotheques validee (ou packages precharges)
- Jeux de donnees disponibles (CSV/Excel)
- Acces internet/proxy confirmes pour la sequence API
