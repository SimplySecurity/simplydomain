#!/usr/bin/env bash
set -ex

# SET THE FOLLOWING VARIABLES
USERNAME=simplysecurity
IMAGE=simplydomain

# UPDATE THE SOURCE CODE
git pull

# bump version
docker run --rm -v "$PWD":/app treeder/bump patch
VERSION=`cat VERSION`
echo "version: $VERSION"

# ALERT VERSION
echo "Building Version: $VERSION"

# START BUILD
./build.sh

# TAG IT
git add -A
git commit -m "version $VERSION"
git tag -a "$VERSION" -m "version $VERSION"
git push
git push --tags

# DOCKER TAG/VERSIONING
docker tag $USERNAME/$IMAGE:latest $USERNAME/$IMAGE:$VERSION

# PUSH TO DOCKER HUB
docker push $USERNAME/$IMAGE:latest
echo "Docker image pushed: $USERNAME/$IMAGE:latest"
docker push $USERNAME/$IMAGE:$VERSION
echo "Docker image pushed: $USERNAME/$IMAGE:$VERSION"