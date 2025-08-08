%include "pbn_utils.asm"

section .bss
buf: resb 21
buf2: resb 21

section .text
global _start


str_to_uint64:
; input:
;   rsi: const char*
; output:
;   rax: uin64
; changes regs:
;   rax, rdi, rcx, r8, r9

    xor rcx, rcx       ; counter = 0
    xor r9, r9         ; uint64 output = 0
    mov rdi, 1         ; rdi = 10 ** 0 = 1
.loop:
    xor rax, rax
    mov al, byte [rsi + rcx]
    cmp al, 0
    je .done

    sub al, 0x30       ; char to digit (0, ... ,9)
    mov r8, rdi        ; r8 (temporary) = 10 ** counter
    imul r8, rax       ; r8 = (10 ** counter) * digit
    add r9, r8         ; output += r8

    imul rdi, rdi, 10  ; rdi = rdi * 10
    inc rcx            ; counter++
    jmp .loop

.done:
    mov rax, r9
    ret

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

    mov rsi, buf
    call str_to_uint64
    mov rdi, rax
    mov rsi, buf2
    call i64_to_str
    call echo_str


    mov rax, 60
	xor rdi, rdi
	syscall
