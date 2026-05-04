# Rapport de projet — Resume Screening Assistant

Ce document décrit le projet "Resume Screening Assistant" — architecture, jeux de données, modèles, instructions d'exécution, évaluation, limites et recommandations. Rédigé en français pour remise au professeur.

## 1. Résumé du projet

Objectif : fournir un assistant automatique pour présélectionner et classer des CV par pertinence par rapport à une offre d'emploi. Le pipeline comprend : prétraitement de texte, extraction de sections/keywords, vectorisation (TF‑IDF), classification de catégorie et score de pertinence (TF‑IDF + recoupement mots‑clés + pondération de sections).

## 2. Contenu du dépôt fourni

- `main.py` : point d'entrée monolithique (interface HTML + endpoints Flask/FastAPI légers) utilisé pour l'exécution locale.
- `frontend/index.html` : interface web simple permettant de soumettre une description de poste et d'afficher les CV classés.
- `data/Resume.csv` : jeu de données utilisé pour entraînement / démonstration.
- `data/models/` : artefacts de modèles (vectorizer.joblib, category_classifier.joblib, classifier_meta.json).
- `train.py` : script d'entraînement (prétraitement, TF‑IDF, SMOTE, entraînement du classifieur, sauvegarde des artefacts).
- `requirements.txt` : dépendances Python.
- `reports/` : rapports d'évaluation (inclus pour référence).
- `tests/` : tests unitaires et d'intégration (peuvent nécessiter `data.dataset_loader` si exécutés).

Nota : le dossier `app/` a été retiré pour conserver un livrable minimal centré sur `main.py` comme demandé.

## 3. Architecture et composants clés

- Prétraitement : pipeline de nettoyage (normalisation, suppression de stopwords, tokenisation légère) implémenté dans `core/text_processor.py` (ou équivalent intégré dans `main.py`).
- Vectorisation : `TfidfVectorizer` sauvegardé dans `data/models/vectorizer.joblib`.
- Classification de catégorie : pipeline scikit‑learn sauvegardée dans `data/models/category_classifier.joblib`.
- Scoring : combinaison de similarité TF‑IDF entre description et CV, recoupement mots‑clés extraits et pondération des sections (titre, expérience, compétences).

## 4. Mode d'emploi — exécution locale (recommandé pour le professeur)

Prérequis : Python 3.8+, créer un environnement virtuel et installer les dépendances.

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Lancer l'interface locale (utilise `main.py`) :

```powershell
python main.py
# puis ouvrir http://127.0.0.1:8000/ dans un navigateur
```

Endpoints utiles :
- POST `/api/v1/rank` : soumettre `job_description`, `top_k` et récupérer la liste des CV triés.

Si le professeur préfère exécuter sans interface, un script d'exemple pour invoquer directement la fonction de ranking est inclus dans `data/samples/sample_data.py`.

## 5. Structure des fichiers importants (détail)

- `main.py` : charge les modèles depuis `data/models/`, expose l'API et sert `frontend/index.html`.
- `train.py` : pour reproduire l'entraînement, produit `vectorizer.joblib` et `category_classifier.joblib`.
- `data/models/classifier_meta.json` : méta‑informations (version du modèle, date, métriques d'entraînement).

## 6. Évaluation et métriques

Les rapports d'évaluation (dans `reports/`) présentent : accuracy, precision, recall et F1 pour les classes du classifieur; validation croisée et matrices de confusion. Points saillants :

- F1 macro moyen observé : (voir `reports/evaluation_report.json`).
- Limitations : classes déséquilibrées (SMOTE utilisé), quelques erreurs de segmentation de sections sur CV mal formatés.

## 7. Limites connues et recommandations

- Absence de `data/dataset_loader.py` dans la version fournie : certaines routines d'entraînement / tests peuvent échouer sans ce loader. J'ai gardé les artefacts entraînés pour permettre l'exécution sans réentraîner.
- Améliorations possibles : intégration d'un embedder sémantique (SBERT) pour meilleur matching, normalisation robuste des sections, pipeline CI/CD, tests automatisés end‑to‑end.

## 8. Déploiement recommandé (option production)

Pour un déploiement simple en production :

1. Construire une image Docker basée sur Python slim.
2. Servir l'application via `uvicorn` derrière `nginx` (reverse proxy) pour TLS et gestion des connections.
3. Mettre en place un service de stockage sécurisé pour les artefacts modèles et un mécanisme de migration / versioning.

Extrait minimal de `Dockerfile` :

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

## 9. Commentaires sur la reproduction et la sûreté

- Les modèles fournis sont destinés à usage pédagogique ; éviter de les utiliser directement en production sans calibration métier.
- Documenter le jeu de données, les biais possibles (sur‑/sous‑représentation), et prévoir une revue humaine pour décisions finales.

## 10. Annexes

- Liste des fichiers inclus :
  - `main.py`
  - `train.py`
  - `requirements.txt`
  - `frontend/index.html`
  - `data/Resume.csv`
  - `data/models/*`
  - `REPORT.md` (ce fichier)
  - `README.md`

- **Authors:** Hamza El Mandouri, Zakariya Kalakhy

---

## 11. Spécifications fonctionnelles, non‑fonctionnelles et architecture détaillée

### Fonctionnel
- **But principal :** présélectionner et classer automatiquement des CV selon une description de poste.
- **Entrées :** `job_description` (texte libre), paramètres `top_k`, corpus de CV (`data/Resume.csv` ou dossiers de CV).
- **Sorties :** liste ordonnée de candidats avec score, catégorie prédite et éléments d'explication (mots‑clés matchés, sections influentes).
- **Cas d'utilisation :** requête interactive via interface web, scoring batch pour lots de CV, export des résultats pour revue humaine.
- **Contraintes métier :** la sortie est indicative — décision finale humaine; fournir trace d'explicabilité minimale.

### Non‑fonctionnel
- **Performance :** latence cible < 2s pour un scoring individuel lorsque `vectorizer` et `classifier` sont préchargés.
- **Scalabilité :** architecture conçue pour pré‑calcul TF‑IDF et traitement batch / workers afin d'augmenter le débit.
- **Disponibilité :** déploiement conteneurisé recommandé avec reverse proxy (`nginx`) et process manager pour redémarrage automatique.
- **Sécurité & confidentialité :** validation des entrées, accès restreint aux artefacts modèles, stockage chiffré si sensible.
- **Maintenabilité :** séparation nette entre composants d'entraînement (`train.py`) et runtime (`main.py`), tests unitaires et rapports d'évaluation versionnés.

### Architecture technique (détaillée)
- **Composants :**
  - *Frontend* : `frontend/index.html` — UI minimale pour soumettre une offre et afficher le Top K.
  - *API / Entrypoint* : `main.py` — charge les artefacts depuis `data/models/`, expose `/api/v1/rank` et sert le frontend.
  - *Prétraitement* : normalisation, suppression stopwords, tokenisation, extraction de sections et keywords.
  - *Vectorisation* : `TfidfVectorizer` persisté en `data/models/vectorizer.joblib`.
  - *Classifieur* : pipeline scikit‑learn persisté en `data/models/category_classifier.joblib`.
  - *Engine de Scoring* : combine similarité TF‑IDF, recoupement mots‑clés et pondération par sections pour produire le score final.
  - *Stockage* : `data/Resume.csv` (source) et `data/models/` (artefacts)

- **Flux de données :**
  1. Le frontend POSTe `job_description` à l'API.
  2. L'API prétraite la description et vectorise uniquement la requête.
  3. Les CV du corpus sont pré‑vectorisés (ou vectorisés à la demande) ; la similarité est calculée entre la requête et chaque CV.
  4. Le classifieur peut filtrer/prioriser par catégorie métier.
  5. Le moteur combine scores et renvoie le Top K avec explications.

- **Décisions techniques clés :**
  - Précharger `vectorizer` et `classifier` au démarrage pour réduire la latence.
  - Pré‑calculer et stocker la matrice TF‑IDF des CV pour les gros corpus.
  - Fournir endpoints de healthcheck et logs de latence pour observabilité.

### Diagramme d'architecture

```
Frontend (index.html)
    ↓
API (main.py) 
    ├→ Prétraitement
    ├→ Vectorizer (TF-IDF)
    ├→ Classifier (Category)
    ├→ Scoring Engine
    └→ Data/Models
         ├→ vectorizer.joblib
         ├→ category_classifier.joblib
         └→ Resume.csv
    ↓
Résultats + Frontend
```

Fin du rapport.
