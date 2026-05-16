FROM python:3.11-slim

WORKDIR /app

# Use a non-root user for safety
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install system deps for builds and healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	curl \
	cmake \
	libgomp1 \
	libatlas-base-dev \
	libopenblas-dev \
	liblapack-dev \
	gfortran \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements-base.txt requirements-ml.txt requirements.txt ./
# Ensure pip/setuptools/wheel are up-to-date to prefer wheels when available
RUN pip install --upgrade pip setuptools wheel
# Install base requirements (must succeed)
RUN pip install --no-cache-dir -r requirements-base.txt
# Try to install ML requirements; don't fail the build if these fail (fallback supported at runtime)
RUN set -o pipefail; pip install --no-cache-dir -r requirements-ml.txt 2>&1 | tee /tmp/ml_install.log || (echo "ML deps installation failed; continuing without ML packages" > /app/.ml_install_failed)
RUN if [ -f /app/.ml_install_failed ]; then echo "ML deps missing: see /tmp/ml_install.log"; fi

# Copy source and data
COPY app/ ./app/
COPY data/ ./data/
COPY frontend/ ./frontend/
COPY scripts/docker_entrypoint.sh /usr/local/bin/docker_entrypoint.sh
RUN chmod +x /usr/local/bin/docker_entrypoint.sh

# Ensure model directory exists
RUN mkdir -p /app/data/models && chown -R appuser:appuser /app

# Expose port
EXPOSE 8000

# Switch to non-root user
USER appuser

# Use entrypoint to show ML-install hints then run server
ENTRYPOINT ["/usr/local/bin/docker_entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
