#!bin/bash

echo "Fast push"

git pull
git add .
git commit -m "fast-push"
git push
