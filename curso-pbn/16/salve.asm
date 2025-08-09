section .rodata
msg db "galera do baixo nivel", 0

section .text
global main

extern salve

main:
    mov rdi, msg ; pass msg as first argument (const char*) to function 'salve'
    call salve

    xor rax, rax ; return 0 from main
    ret

    ; not needed, since we are returning 0 from main
    ; this is handled by gcc and the libc
    ;mov rax, 60
    ;xor rdi, rdi
    ;syscall



