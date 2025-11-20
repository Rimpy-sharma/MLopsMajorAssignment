# GitHub Actions Workflow Setup

## Overview
This CI/CD pipeline automates model training, testing, Docker image building, and Kubernetes deployment.

## Workflow Jobs

### 1. **Test Job**
- Runs on every push and pull request
- Sets up Python environment
- Installs dependencies
- Trains the ML model
- Runs tests
- Uploads model artifacts

### 2. **Build and Push Docker Job**
- Runs only on push to `main` or `docker_cicd` branches
- Requires the test job to pass
- Downloads trained model
- Builds Docker image
- Pushes to Docker Hub with multiple tags

### 3. **Deploy Job (Optional)**
- Runs only on push to `main` branch
- Requires Docker build to succeed
- Updates Kubernetes deployment
- Applies changes to cluster

## Required GitHub Secrets

To use this workflow, configure these secrets in your GitHub repository:

### Go to: Settings → Secrets and variables → Actions → New repository secret

1. **DOCKER_USERNAME**
   - Your Docker Hub username
   - Example: `your-dockerhub-username`

2. **DOCKER_PASSWORD**
   - Your Docker Hub access token (recommended) or password
   - Get token from: https://hub.docker.com/settings/security
   - Click "New Access Token"

3. **KUBE_CONFIG** (Optional - only for deployment job)
   - Your Kubernetes cluster config file (base64 encoded)
   - Get it: `cat ~/.kube/config | base64 -w 0`
   - Paste the base64 string as the secret value

## Setup Instructions

### Step 1: Set up Docker Hub Secrets
```bash
# Go to GitHub repository → Settings → Secrets and variables → Actions
# Add DOCKER_USERNAME and DOCKER_PASSWORD
```

### Step 2: Update Kubernetes Deployment (if using K8s)
Edit `k8s-deployment.yaml` and replace `<YOUR_DOCKERHUB_USERNAME>` with your actual Docker Hub username, or the workflow will do it automatically if you set up the deployment job.

### Step 3: Enable Workflow
The workflow will automatically run on:
- Push to `main` or `docker_cicd` branches
- Pull requests to `main` branch

## Workflow Features

✅ **Automated Testing**: Runs train and test scripts on every commit  
✅ **Artifact Management**: Saves trained models for 30 days  
✅ **Docker Multi-tagging**: Creates `latest`, branch, and SHA tags  
✅ **Build Caching**: Speeds up Docker builds using registry cache  
✅ **Conditional Deployment**: Only deploys from main branch  
✅ **Kubernetes Integration**: Automated deployment updates  

## Docker Image Tags

The workflow creates multiple tags:
- `latest` - Latest from main branch
- `docker_cicd` - Latest from docker_cicd branch
- `main` - Latest from main branch
- `docker_cicd-abc1234` - Specific commit SHA

## Disabling Jobs

To disable the deployment job (if you don't have K8s):
- It's already optional and won't fail if KUBE_CONFIG is not set
- Or comment out the entire `deploy` job in the workflow file

## Testing the Workflow

1. Make a change to your code
2. Commit and push:
   ```bash
   git add .
   git commit -m "Test CI/CD pipeline"
   git push origin docker_cicd
   ```
3. Check workflow status: https://github.com/Rimpy-sharma/MLopsMajorAssignment/actions

## Troubleshooting

**Problem**: Docker login fails  
**Solution**: Check DOCKER_USERNAME and DOCKER_PASSWORD secrets are correct

**Problem**: Python version not available  
**Solution**: Workflow uses Python 3.11 (stable), modify if needed

**Problem**: Kubernetes deployment fails  
**Solution**: Ensure KUBE_CONFIG is properly base64 encoded and valid

## Manual Workflow Trigger

You can also trigger the workflow manually:
1. Go to Actions tab
2. Select "MLOps CI/CD Pipeline"
3. Click "Run workflow"
