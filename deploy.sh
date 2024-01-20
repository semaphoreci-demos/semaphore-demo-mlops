#!/usr/bin/env bash
# Deploy model to Hugging Face Spaces
# Note: PWD must be the original GitHub/Bitbucket repo
# Usage:
#   ./deploy <HuggingFace HTTPS Git Repo> <SSH Private Key Path>
# example:
#   ./deploy https://huggingface.co/spaces/tomfern/cats-and-dogs /home/semaphore/.ssh/id_ed25519 

repo=$1
shift
privkey=$1
shift

set -e

deploy_tmp=$(mktemp -d)

if [ ! -f "$privkey" ]; then
    echo "Private key not found or not supplied"
    exit 1
fi

# ensure correct permissions
chmod 600 "$privkey"

git lfs install

# clone HF repo
GIT_SSH_COMMAND="ssh -i '$privkey' -o StrictHostKeyChecking=accept-new" git clone "$repo" "$deploy_tmp"

# copy files
cp requirements.txt "$deploy_tmp"
mkdir -p "$deploy_tmp"/src "$deploy_tmp"/models
cp src/app.py src/utils.py "$deploy_tmp"/src
cp models/model.pkl models/model.pth "$deploy_tmp"/models

# add changes
git config user.email "bot@semaphoreci.com"
git config user.name "semaphoreci"
git add models src requirements.txt

# check if there changes and commit
if [ -n "$(git status --porcelain)" ]; then
    echo "==> Deploying $SEMAPHORE_GIT_BRANCH - commit $SEMAPHORE_GIT_SHA"
    git commit -m "deploy branch $SEMAPHORE_GIT_BRANCH - commit $SEMAPHORE_GIT_SHA"
    GIT_SSH_COMMAND="ssh -i '$privkey' -o StrictHostKeyChecking=accept-new" git push origin main
else
  echo "==> No changes to deploy"
fi

rm -rf "$deploy_tmp"
