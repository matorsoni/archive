%include "pbn_utils.asm"

section .bss
buf: resb 21

section .text
global _start
_start:

    mov rsi, buf
    mov rdi, INT64_MIN
    call i64_to_str
    call echo_str

    mov rsi, buf
    mov rdi, INT64_MAX
    call i64_to_str
    call echo_str

    mov rsi, buf
    mov rdi, -123
    call i64_to_str
    call echo_str

    mov rsi, buf
    mov rdi, 0
    call i64_to_str
    call echo_str

    mov rsi, buf
    mov rdi, 123
    call i64_to_str
    call echo_str

    mov rax, 60
	xor rdi, rdi
	syscall
