#!/bin/bash
version=2024.10
tag="release/$version/final"
for repo in opm-common opm-grid opm-simulators
do
#    echo "=== Cloning repo: $repo"
#    git clone https://github.com/OPM/$repo.git
    cd $repo
    git checkout $tag
    cd ..
done
