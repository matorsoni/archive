# montar com: as salve-att.s -o salve-att.o
# linkar com: ld salve-att.o -o salve-att

    .section .data
msg:
    .ascii "Salve, simpatia!\n"
len = . - msg

    .section .text
    .global _start

_start:
    #
    mov $1, %rax
    mov $1, %rdi
    lea msg(%rip), %rsi
    mov $len, %rdx
    syscall

    mov $60, %rax
    xor %rdi, %rdi
    syscall

