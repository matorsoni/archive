CPP="zig c++"
COMPILER_FLAGS="-Wall -pedantic -Werror -g -std=c++20 -fno-exceptions -I eigen"
LINKER_FLAGS=""
COMPILER_AND_LINKER_FLAGS="-fsanitize=undefined"
SOURCE="demo.cpp"

$CPP $COMPILER_FLAGS $COMPILER_AND_LINKER_FLAGS -c $SOURCE -o demo.o
gcc $LINKER_FLAGS $COMPILER_AND_LINKER_FLAGS demo.o -o demo
