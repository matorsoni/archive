%include "pbn_utils.asm"

%define SYS_READ  0
%define SYS_WRITE 1
%define SYS_EXIT  60

%define STDIN_FD  0
%define STDOUT_FD 1

%define EXIT_SUCCESS 0
%define EXIT_FAIL    1

%define READ_BUF_SIZE 256

section .rodata
    msg db `Hello!\n`
    msg_len equ $ - msg

    msg_read_fail db `Error: nothing was read :(\n`
    msg_read_fail_len equ $ - msg_read_fail

    msg_give_up db `Never gonna give you up...\n`
    msg_give_up_len equ $ - msg_give_up

section .bss
    read_buf resb READ_BUF_SIZE
    count resq 1


section .text

_print:
    mov rax, SYS_WRITE
    mov rdi, STDOUT_FD
    syscall
    ret

;_check_valid_number:
;    xor rcx, rcx
;    xor r8, r8
;    xor r9, r9
;.test_signal:
;    mov r8b, byte[read_buf]
;    cmp r8b, '-'
;    jne .check_plus
;    inc r9
;    inc rcx
;    jmp .digit_loop
;.check_plus:
;    cmp r8b, '+'
;    jne .check_digit
;    inc rcx
;.digit_loop:
;    mov r8b, byte[buf + rcx]


global _start
_start:

    mov rsi, msg
    mov rdx, msg_len
    call _print

    ; Read from stdin into read_buf
    ; @TODO: flush to avoid leaking anything past READ_BUF_SIZE!
    mov rax, SYS_READ
    mov rdi, STDIN_FD
    mov rsi, read_buf
    mov rdx, READ_BUF_SIZE-1
    syscall

    ; Check if read stdin failed
    cmp rax, 0
    je .error_read_fail

    ; Make sure read_buf is null terminated
    mov byte [read_buf + rax], 0

    ; Remove last character if it is '\n' (0x0a)
    xor rbx, rbx
    mov bl, byte [read_buf + rax - 1]
    cmp bl, EOL_CHAR
    jne .buffer_ready
    mov byte [read_buf + rax - 1], 0
    dec rax

.buffer_ready:

    ; Save number of bytes read into count
    mov [count], rax

    ; Check if 'q' (0x71) was typed
    cmp rax, 1
    jne .dont_give_up
    xor rbx, rbx
    mov bl, byte [read_buf]
    cmp bl, 0x71
    je .give_up

.dont_give_up:

    mov rsi, read_buf
    mov rdx, [count]
    call _print

    mov rdi, [count]
    mov rsi, read_buf
    call i64_to_str

    mov rsi, read_buf
    call echo_str

.exit_success:
    mov rax, SYS_EXIT
    mov rdi, EXIT_SUCCESS
    syscall

.exit_error:
    mov rax, SYS_EXIT
    mov rdi, EXIT_FAIL
    syscall

.error_read_fail:
    mov rsi, msg_read_fail
    mov rdx, msg_read_fail_len
    call _print
    jmp .exit_error

.give_up:
    mov rsi, msg_give_up
    mov rdx, msg_give_up_len
    call _print
    jmp .exit_success
