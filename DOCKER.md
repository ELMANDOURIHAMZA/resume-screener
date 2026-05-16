# Docker: build et exécution

Ce fichier explique comment builder et lancer l'application dans Docker (image Python 3.11) et contient des astuces pour dépanner les problèmes courants (dependances natives, artefacts de modèles).

## Prérequis
- Docker Engine / Docker Desktop installé.
- Docker Compose v2 (commande `docker compose` disponible).
- Le dossier `data/models/` contient les artefacts entraînés : `vectorizer.joblib`, `category_classifier.joblib`, `classifier_meta.json`.

## Builder et démarrer (recommandé)

Depuis la racine du projet :

```bash
docker compose up --build -d
```

Vérifier les logs :

```bash
docker compose logs -f
```

Vérifier l'état des services :

```bash
docker compose ps
```

Tester l'endpoint de santé :

```bash
curl http://localhost:8000/api/v1/health
# PowerShell
Invoke-RestMethod http://localhost:8000/api/v1/health
```

## Commandes utiles

Arrêter et supprimer les conteneurs :

```bash
docker compose down
```

Rebuild sans cache :

```bash
docker compose build --no-cache
docker compose up -d
```

Exécuter une commande dans le conteneur API :

```bash
docker compose exec api bash
# ou PowerShell
docker compose exec api sh
```

Lancer les tests (si présents) depuis le conteneur :

```bash
docker compose exec api pytest -q
```

## Montage des modèles
Le `docker-compose.yml` monte `./data/models` sur `/app/data/models` dans le conteneur. Avant de démarrer en production, assurez-vous que `data/models` contient bien :

- `vectorizer.joblib`
- `category_classifier.joblib`
- `classifier_meta.json`

Si vous entraînez localement, le script `train.py` écrit déjà ces fichiers dans `data/models/`.

## Dépannage
- Échecs `pip install` liés à des compilations natives (pandas, scikit-learn, lightgbm) : utiliser l'image Python 3.11 (déjà configurée) ou builder sur une machine disposant des outils de build. Le Dockerfile installe `build-essential` pour aider à la compilation.
- Problèmes de permission sur Windows : utiliser WSL2 ou Docker Desktop; le conteneur tourne en utilisateur non-root pour la sécurité.
- Si le healthcheck échoue, consultez `docker compose logs api` pour voir les erreurs d'import ou de chargement de modèles.

## Conseils pour la soutenance
- Prépare une image finale contenant déjà les artefacts `data/models/` si tu dois déployer sur une machine sans accès aux sources.
- Documente la commande exacte utilisée pour builder et exécuter (capture d'écran ou snippet dans README).
