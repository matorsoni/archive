%include "pbn_utils.asm"

section .bss
buf: resb 21

section .text
global _start
_start:

    mov rax, 0
    mov rdi, 1
    mov rsi, buf
    mov rdx, 20
    syscall

    ; desafios para aula 13:
    ;
    ; converter string lida no buffer para inteiro (uint64 por enquanto)
    ; somar valor convertido com 42
    ; imprimir o resultado da soma
    ;
    ; em paralelo, pesquisar como limpar o buffer do
    ; (o que causa "command not found" para entradas longas)


    mov rsi, buf
    call echo_str

    mov rax, 60
	xor rdi, rdi
	syscall
