%include "pbn_utils.asm"

%define BUF_SIZE  21
%define E_NUMB    42
%define E_OVER    23
%define MUL10_MAX 922337203685477580
%define TCFLUSH   0x540B
%define TCIFLUSH  0

section .bss
    buf resb BUF_SIZE

section .text
global _start
_start:

    xor rax, rax
    xor rdi, rdi
    mov rsi, buf
    mov rdx, BUF_SIZE - 1
    syscall

    push rax

_term_flush:
    mov rax, 16       ; syscall ioctl
    xor rdi, rdi
    mov rsi, TCFLUSH
    mov rdx, TCIFLUSH
    syscall

    pop rax

_check_read:
   cmp rax, 0		; se rax  == 0, é erro
   je _exit_err
   mov byte [buf+rax], 0	; garante terminador nulo

   ; converter caracteres em números
_convert:
   xor rax, rax		; resultados
   mov rbx, 10		; multiplicador por 10
   xor rcx, rcx		; índice = 0
   xor rdx, rdx		; dígitos convertidos
   xor r9, r9		; flag de sinal
.test_sig:
   mov r8b, byte [buf+rcx]	; carrega primeiro caractere
.check_minus:
   cmp r8b, '-'		; tem sinal de negativo?
   jne .check_plus
   inc r9			; flag de sinal = 1 (negativo)
   inc rcx			; avança para próximo caractere
   jmp .digit_loop
.check_plus:
   cmp r8b, '+'		; tem sinal de positivo?
   jne .check_digit
   inc rcx			; só avança para próximo caractere
.digit_loop:
   mov r8b, byte [buf+rcx]	; carrega caractere seguinte
.check_digit:
   cmp r8b, '0' 		; se menor, termina
   jl .check_count
   cmp r8b, '9'		; se maior, termina
   jg .check_count
   sub r8b, 0x30		; converter para int
.check_i64max:			; isso sacrifica INT64_MIN
   mov r10, MUL10_MAX	; INT64_MAX / 10
   cmp rax, r10		; se maior, overflow
   ja _exit_overflow
   jb .safe
   cmp r8b, 7		; rax == MUL10_MAX, só pode somar até 7
   ja _exit_overflow
.safe:
   mul rbx			; rax = rax × 10
   add rax, r8		; rax = rax + r8b
   inc rcx			; índice do próximo caractere
   inc rdx			; incrementa contagem de dígitos
   jmp .digit_loop
.check_count:
   cmp rdx, 0		; se rcx == 0, nada foi convertido
   je _exit_err
.negative:
   cmp r9, 0		; negativo?
   je .done
   neg rax			; torna negativo
.done:

   ; verificar se pode somar (NUM <= INT64_MAX-valor)
   ; somar rax valor com 42
   add rax, 42

   ; converter soma para string
    mov rsi, buf
    mov rdi, rax
    call i64_to_str
   ; imprimir resultado
    call echo_str

_exit_ok:
   xor rdi, rdi
   jmp _exit
_exit_err:
   mov rdi, E_NUMB
   jmp _exit
_exit_overflow:
   mov rdi, E_OVER
_exit:
   mov rax, 60
   syscall
