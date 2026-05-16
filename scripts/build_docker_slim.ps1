# Build and run the slim Docker image, collect logs
Set-StrictMode -Version Latest

Write-Host "Building Docker image (Dockerfile.slim)..."

docker build -f Dockerfile.slim -t resume-screener:slim . 2>&1 | Tee-Object -FilePath docker-build-slim.log
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed (exit code $LASTEXITCODE). See docker-build-slim.log" -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "Running container resume-screener-slim on port 8000..."
# remove any existing container with same name
if (docker ps -a --format "{{.Names}}" | Select-String -Pattern "resume-screener-slim") {
    docker rm -f resume-screener-slim | Out-Null
}

docker run -d --name resume-screener-slim -p 8000:8000 resume-screener:slim
Start-Sleep -Seconds 3

Write-Host "Collecting runtime logs to docker-api-slim.log (first 200 lines)..."
docker logs --tail 200 resume-screener-slim > docker-api-slim.log

Write-Host "Done. Files: docker-build-slim.log, docker-api-slim.log"
Write-Host "To stop the container: docker rm -f resume-screener-slim"
