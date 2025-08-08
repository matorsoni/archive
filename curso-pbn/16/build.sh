nasm -felf64 salve.asm
gcc -c libsalve.c
gcc salve.o libsalve.o -o salve -z noexecstack -no-pie ## flags to fix warnings

