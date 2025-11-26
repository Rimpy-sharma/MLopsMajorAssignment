# GitHub Actions workflow validation configuration
# These secrets are expected to be missing in local development
# Add them in GitHub repository settings: Settings > Secrets and variables > Actions
# 
# Required secrets:
# - DOCKER_USERNAME: Your Docker Hub username
# - DOCKER_PASSWORD: Your Docker Hub access token or password
# - KUBE_CONFIG: Base64 encoded Kubernetes config (optional, for deployment)
#
# Workflow will gracefully skip steps that require missing secrets
