# PowerShell script to build and run the Docker Compose stack, then wait for health
Param()

Set-StrictMode -Version Latest
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$Root\.."

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker n'est pas installé ou disponible dans PATH."
    exit 1
}

Write-Host "Building and starting containers..."
docker compose up --build -d

$Url = 'http://localhost:8000/api/v1/health'
$Retries = 30
$Sleep = 2
for ($i = 1; $i -le $Retries; $i++) {
    try {
        $r = Invoke-RestMethod -Uri $Url -Method Get -TimeoutSec 5
        if ($r.status -eq 'ok') {
            Write-Host "API prête"
            docker compose ps
            exit 0
        }
    } catch {
        # ignore
    }
    Write-Host "- waiting ($i/$Retries)"
    Start-Sleep -Seconds $Sleep
}

Write-Host "API did not become ready in time. See logs:"
docker compose logs --tail 200 api
exit 2
