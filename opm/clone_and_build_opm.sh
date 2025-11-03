#!/bin/bash
for repo in opm-common opm-grid opm-simulators opm-upscaling
do
    echo "=== Cloning and building module: $repo"
    git clone https://github.com/OPM/$repo.git
    mkdir $repo/build
    cd $repo/build
    cmake ..
    make -j2 # Only 2 threads to limit RAM usage
    cd ../..
done

ln -s opm-simulators/build/bin/flow

# Clone dataset repos
git clone https://github.com/OPM/opm-data.git
git clone https://github.com/OPM/opm-tests.git

