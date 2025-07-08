; montar com: nasm -f elf64 salve-intel.asm
; linkar com: ld salve-intel.o -o salve-intel

section .data
    msg db "Salve, simpatia!", 10 ; 10 = '\n'
    len equ $ - msg

section .text
    global _start

_start:
    ; write(1, msg, len)
    mov rax, 1      ; syscall numero 1: write
    mov rdi, 1      ; stdout
    mov rsi, msg    ; endereco da mensagem
    mov rdx, len    ; tamanho da mensagem
    syscall

    mov rax, 60     ; syscall numero 60: exit
    xor rdi, rdi    ; status 0
    syscall

