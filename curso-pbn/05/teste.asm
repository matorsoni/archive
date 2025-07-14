section .data
    global_data dd 123 ; define double word (4 bytes): int global_data = 123

section .bss
    global_bss resq 1 ; reserva 1 quad word (4 bytes): int global_bss;

section .ro_data
    msg db "Salve, simpatia!"

section .text
    global _start

_start:
    mov rax, 60
    mov rdi, 2
    syscall
