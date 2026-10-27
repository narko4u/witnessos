# =============================================================================
# WitnessOS Compliance Pack — Multi-stage Docker Image
# =============================================================================
# Stage 1: Build — install the CLI and its dependencies
# Stage 2: Runtime — minimal image with just the installed CLI
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1 — Builder
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS builder

LABEL maintainer="WitnessOS Team <dev@witnessos.io>"
LABEL version="0.1.0"
LABEL description="WitnessOS Compliance Pack — CLI for NSA MCP and EU AI Act compliance reports"

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire project into the image
WORKDIR /build
COPY . .

# Install the package and its dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# ---------------------------------------------------------------------------
# Stage 2 — Runtime
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

LABEL maintainer="WitnessOS Team <dev@witnessos.io>"
LABEL version="0.1.0"
LABEL description="WitnessOS Compliance Pack — CLI for NSA MCP and EU AI Act compliance reports"

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy the installed Python packages from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Set working directory for report output (mount a volume here)
WORKDIR /data

# The entry point is the witnessos-compliance CLI installed via pyproject.toml
ENTRYPOINT ["witnessos-compliance"]
CMD ["--help"]
