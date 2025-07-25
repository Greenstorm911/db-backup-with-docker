# Docker Hub Setup Instructions

To enable automatic pushing to Docker Hub, you need to configure GitHub repository secrets.

## Step 1: Create Docker Hub Access Token

1. Go to [Docker Hub](https://hub.docker.com/)
2. Sign in to your account
3. Click on your profile → **Account Settings**
4. Go to **Security** tab
5. Click **New Access Token**
6. Give it a descriptive name (e.g., "GitHub Actions")
7. Select **Read, Write, Delete** permissions
8. Click **Generate**
9. **Copy the token** (you won't see it again!)

## Step 2: Configure GitHub Repository Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these two secrets:

### DOCKERHUB_USERNAME
- **Name**: `DOCKERHUB_USERNAME`
- **Value**: Your Docker Hub username (e.g., `greenstorm911`)

### DOCKERHUB_TOKEN
- **Name**: `DOCKERHUB_TOKEN`
- **Value**: The access token you copied from Docker Hub

## Step 3: Verify Setup

Once the secrets are configured:

1. Push code to the `main` branch
2. Check the **Actions** tab in GitHub
3. The workflow should successfully build and push to Docker Hub
4. Check your Docker Hub repository at: https://hub.docker.com/r/greenstorm911/db-backup-with-docker

## Usage for End Users

After setup, users can simply use:

```yaml
services:
  db-backup:
    image: greenstorm911/db-backup-with-docker:latest
    # ... rest of configuration
```

No need to build locally or deal with GitHub Container Registry authentication!

## Available Tags

- `latest` - Latest build from main branch
- `v1.0.0` - Specific version tags
- `main-abc1234` - Branch + commit hash for development

## Troubleshooting

### Build Fails with Authentication Error
- Check that both `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets are set correctly
- Verify the Docker Hub access token has write permissions
- Make sure the username matches exactly (case-sensitive)

### Image Not Appearing on Docker Hub
- Check the Actions tab for any error messages
- Verify the repository name is correct in the workflow
- Check if your Docker Hub account has the repository created
