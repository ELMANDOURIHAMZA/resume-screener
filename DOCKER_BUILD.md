Guide de build Docker (Windows PowerShell)

Objectif
- Construire l'image Docker de l'API, démarrer le service et collecter des logs pour diagnostic.

Instructions rapides (PowerShell)
1) Ouvrez PowerShell en tant qu'administrateur (si nécessaire) et placez-vous dans le repo:

```powershell
cd C:\Users\Ahmed\Desktop\resume-screener
```

2) Construire l'image (sans cache) et capturer la sortie dans un fichier:

```powershell
docker compose build --no-cache 2>&1 | Tee-Object -FilePath docker-build.log
```

3) Si la construction réussit, lancer les services en arrière-plan:

```powershell
docker compose up -d
```

4) Récupérer les logs récents du service API:

```powershell
docker compose logs --no-color --tail=500 api > docker-api.log
```

5) Si la construction échoue, fournissez `docker-build.log`. Si le conteneur démarre mais l'API a des erreurs, fournissez `docker-api.log`.

Conseils de diagnostic
- Si l'installation des dépendances ML (lightgbm, scipy, scikit-learn) échoue, joignez docker-build.log; je vous aiderai à ajuster le Dockerfile et requirements.
- Le Dockerfile est conçu pour tenter d'installer les dépendances ML et, si ça échoue, démarrer quand même avec un mode dégradé. Les logs aideront à décider des correctifs.

Fichiers produits
- docker-build.log : sortie de la construction
- docker-api.log : logs runtime du service `api`

Soumettez l'un des fichiers ci-dessus si vous rencontrez un problème et je l'analyserai.

Option: image "slim" (pré-entraînée, évite compilation ML)
------------------------------------------------------
Si vous ne voulez pas compiler les dépendances ML dans l'image (lightgbm/scipy), utilisez l'image "slim" préconfigurée ci-dessous. Elle suppose que les artefacts entraînés sont présents dans le dépôt (`data/models/`) et n'installe que les dépendances runtime.

Construire et lancer (PowerShell):

```powershell
.\scripts\build_docker_slim.ps1
```

Fichiers générés par ce flux:

- `docker-build-slim.log` : logs de la construction avec `Dockerfile.slim`
- `docker-api-slim.log` : logs runtime du conteneur `resume-screener-slim`

Remarques:
- `Dockerfile.slim` installe uniquement `requirements-runtime.txt` et copie les artefacts présents dans le dépôt.
- Si vous souhaitez ignorer les artefacts dans le dépôt et les monter au runtime, vous pouvez lancer le conteneur avec `-v ${PWD}/data/models:/app/data/models`.
