# Script PowerShell pour builder l'image Docker et collecter les logs
# Usage: exécutez depuis la racine du dépôt (C:\Users\Ahmed\Desktop\resume-screener)

Set-StrictMode -Version Latest

Write-Host "Building Docker images (no-cache) and saving output to docker-build.log..."
docker compose build --no-cache 2>&1 | Tee-Object -FilePath docker-build.log
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build command exited with code $LASTEXITCODE. See docker-build.log for details." -ForegroundColor Yellow
    exit $LASTEXITCODE
}

Write-Host "Bringing up services in detached mode..."
docker compose up -d

Write-Host "Collecting API logs to docker-api.log (last 500 lines)..."
docker compose logs --no-color --tail=500 api > docker-api.log

Write-Host "Done. Files: docker-build.log, docker-api.log"
Write-Host "If build failed, please upload docker-build.log. If container starts but API fails, upload docker-api.log."
