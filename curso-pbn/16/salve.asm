section .rodata
msg db "galera do baixo nivel", 0

section .text
global main

extern salve

main:
    mov rdi, msg
    call salve

    mov rax, 60
    xor rdi, rdi
    syscall



