section .text
    global _start

_start:
    mov rax, [rsp + 8]
    lea rbx, [rsp + 8]

_exit:
    mov rax, 60
    xor rdi, rdi
    syscall

