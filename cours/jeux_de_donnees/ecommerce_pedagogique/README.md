# Jeu de données e-commerce pédagogique

Source d'inspiration : le dataset Kaggle `benroshan/ecommerce-data`.
Lien : https://www.kaggle.com/datasets/benroshan/ecommerce-data

Ce pack n'est pas le dataset Kaggle brut. C'est une version pédagogique remappée pour le cours intermédiaire.

## Fichiers

- `input/commandes_brutes.csv` : fichier principal pour J1/J2
- `input/commandes_brutes.xlsx` : même contenu pour les démos Excel J2
- `input/objectifs_categories.csv` : objectifs de vente par catégorie pour J2/J3
- `api/clients_segments_api.json` : réponse simulée pour l'enrichissement API J3

## Schéma du fichier principal

- `commande_id`
- `customer_id`
- `client`
- `email`
- `montant`
- `date_commande`
- `statut`
- `categorie`
- `sous_categorie`
- `quantite`
- `profit`
- `mode_paiement`
- `region`

## Mapping logique depuis Kaggle

- `Order ID` -> `commande_id`
- identifiant client / commande -> `customer_id`
- champ client -> `client`
- `Category` -> `categorie`
- `Sub-Category` -> `sous_categorie`
- `Quantity` -> `quantite`
- `Amount` -> `montant`
- `Profit` -> `profit`
- `PaymentMode` -> `mode_paiement`
- `Order Date` / purchase date -> `date_commande`

## Colonnes ajoutées pour le cours

Le dataset pédagogique ajoute ou simplifie des colonnes pour coller au fil rouge du deck :

- `email`
- `statut`
- `customer_id`
- `region`

## Anomalies injectées volontairement

Pour rendre les exercices réalistes :

- emails invalides ou vides
- espaces parasites dans les emails
- casse incohérente dans les statuts
- formats monétaires mélangés : `1 200,50 €`, `980.00`, `1,980.00 $`, `N/A`, vide
- formats de dates mélangés ou invalides
- catégories répétées pour `value_counts()` et `group_by`
- clients répétés pour les cas de contrôle qualité et d'enrichissement

## Utilisation recommandée par jour

### J1

Utiliser `input/commandes_brutes.csv`.

Objectifs :
- lecture CSV
- `head`, `schema`, `null_count`, `describe`
- nettoyage email
- nettoyage montant
- TVA / TTC
- dates
- statuts
- `with_columns`, `map_elements`

### J2

Utiliser `input/commandes_brutes.csv` puis `input/commandes_brutes.xlsx`.

Objectifs :
- `value_counts()`
- `group_by`
- `when / then / otherwise`
- graphiques `df.plot...`
- lecture / écriture Excel

### J3

Utiliser `input/objectifs_categories.csv` et `api/clients_segments_api.json`.

Objectifs :
- jointures
- enrichissement API simulé
- script final et logging
