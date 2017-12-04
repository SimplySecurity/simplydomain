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
git checkout -b "Version-$VERSION"
git add --all
git commit -m "version $VERSION"
git tag -a "$VERSION" -m "version $VERSION"
git push origin "Version-$VERSION"
git push origin "Version-$VERSION" --tags
git checkout master
git merge "Version-$VERSION"
git push
hub release create Version-$VERSION -m  "Version compiled by 'build.sh': $VERSION"

# DOCKER TAG/VERSIONING
docker tag $USERNAME/$IMAGE:latest $USERNAME/$IMAGE:$VERSION

# PUSH TO DOCKER HUB
docker push $USERNAME/$IMAGE:latest
echo "Docker image pushed: $USERNAME/$IMAGE:latest"
docker push $USERNAME/$IMAGE:$VERSION
echo "Docker image pushed: $USERNAME/$IMAGE:$VERSION"