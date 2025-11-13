#!/bin/bash

ncpus=32
#SBATCH -p rome16q
#SBATCH --mem=0
#SBATCH -t 00-12:40 # time (D-HH:MM)
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=$ncpus
#SBATCH --output=%j-%x-stdout.txt
#SBATCH --error=%j-%x-stderr.txt

ulimit -s unlimited

module purge

module use /cm/shared/ex3-modules/202309a/xeongold32q/modulefiles
module unuse /cm/shared/ex3-modules/202309a/milanq/modulefiles
module use /home/andreast/modules/modulefiles

module load cmake/gcc/3.28.4 zoltan/202309a/12.16 boost-1.73.0 openblas-0.3.21 parmetis-32-4.0.3 suitesparse-32-5.12.0 openmpi-4.1.4
module load dune/202309a/ss/mod-2.9.1

for repo in opm-common opm-grid opm-simulators
do
    echo "=== Building module: $repo"
    rm -r $repo/build
    mkdir $repo/build
    cd $repo/build
    cmake -DMETIS_ROOT=$METIS_ROOT -DPARMETIS_ROOT=$PARMETIS_ROOT -DSuiteSparse_INCLUDE_DIRS=$SUITESPARSE_INCLUDEDIR -DSuiteSparse_ROOT=$SUITESPARSE_ROOT ..
    #cmake -Dopm-common_DIR=~/D1/opm/opm-common/build -Dopm-grid_DIR=~/D1/opm/opm-grid/build -DUSE_MPI=ON -DUSE_OPENMP=ON -DBUILD_FLOW_VARIANTS=ON -DVALGRIND_INCLUDE_DIR=/cm/shared/apps/valgrind/3.15.0/include -DBOOST_INCLUDEDIR=$BOOST_INCLUDEDIR -DBOOST_LIBRARYDIR=$BOOST_LIBRARYDIR -DBoost_NO_SYSTEM_PATHS=ON -DBoost_NO_BOOST_CMAKE=ON -DZOLTAN_INCLUDE_DIR=$ZOLTAN_INCLUDEDIR -DSuiteSparse_INCLUDE_DIRS=$SUITESPARSE_INCLUDEDIR -DSuiteSparse_ROOT=$SUITESPARSE_ROOT -DZOLTAN_LIBRARY=$ZOLTAN_LIBRARYDIR/libzoltan.a -DMETIS_ROOT=$METIS_ROOT -DPARMETIS_ROOT=$PARMETIS_ROOT ../
    make -j $ncpus
    cd ../..
done

