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
    msg_guess db `Guess a number between 1 and 100: `
    msg_guess_len equ $ - msg_guess

    msg_read_fail db `Empty input! :(\n\n`
    msg_read_fail_len equ $ - msg_read_fail

    msg_invalid_number db ` is not a valid number!\n\n`
    msg_invalid_number_len equ $ - msg_invalid_number

    msg_out_of_bounds db ` is not between 1 and 100!\n\n`
    msg_out_of_bounds_len equ $ - msg_out_of_bounds

    msg_give_up db `Never gonna give you up, never gonna let you down...\n\n`
    msg_give_up_len equ $ - msg_give_up

    msg_you_got_it db `! You got it!!\n\n`
    msg_you_got_it_len equ $ - msg_you_got_it

    msg_try_again db `Nope! Try again.\n\n`
    msg_try_again_len equ $ - msg_try_again


section .bss
    read_buf resb READ_BUF_SIZE
    count    resq 1
    random   resq 1


section .text
_print:
    mov rax, SYS_WRITE
    mov rdi, STDOUT_FD
    syscall
    ret

_print_input:
    mov rsi, read_buf
    mov rdx, [count]
    call _print
    ret

_check_valid_number:
; input:
; rsi -> const char* buf
; output:
; rax -> converted integer
; r8  -> 1 if number is valid, 0 if not
; r9  -> 0 if number is between 1-100, 0 if not
    xor rax, rax    ; converted integer          = 0
    xor rbx, rbx    ; byte read from buffer      = 0
    xor rcx, rcx    ; index                      = 0
    xor r8, r8      ; 'valid number' flag        = false
    xor r9, r9      ; 'out of bounds 1-100' flag = false

    ; Check if first char is '-'
    mov bl, byte [rsi]
    cmp bl, '-'
    jne .check_plus
    mov r9, 1             ; out of bounds = true
    inc rcx
    jmp .digit_loop

.check_plus:

    cmp bl, '+'
    jne .digit_loop
    inc rcx

.digit_loop:

    mov bl, byte [rsi+rcx]
    cmp bl, 0                  ; Check if char is '\0'
    je .done
    cmp bl, 0x30               ; Check if char is a digit: >= '0' (0x30) and <= '9' (0x39)
    jl .not_a_digit
    cmp bl, 0x39
    jg .not_a_digit

    mov r8, 1           ; valid number = true
    cmp r9, 1           ; if number is already out of bonds, skip
    je .next_iter

    sub bl, 0x30		; convert char to integer
    imul rax, rax, 10   ; rax = rax * 10
    add rax, rbx        ; rax = rax + rbx

    cmp rax, 100        ; if rax > 100, set ouf of bounds to true
    jle .next_iter
    mov r9, 1


.next_iter:
    inc rcx             ; index++
    jmp .digit_loop

.done:
    cmp rax, 0
    jg .finish
    mov r9, 1

.finish:
    ret

.not_a_digit:
    xor r8, r8
    ret


global _start
_start:

    ; Save random number to be guessed
    mov byte [random], 33

.guess_a_number:
    mov rsi, msg_guess
    mov rdx, msg_guess_len
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

    ; Give up if 'q' (0x71) was typed as input
    cmp rax, 1
    jne .dont_give_up
    xor rbx, rbx
    mov bl, byte [read_buf]
    cmp bl, 0x71
    je .give_up

.dont_give_up:

    mov rsi, read_buf
    call _check_valid_number

    cmp r8, 0
    je .error_invalid_number

    cmp r9, 1
    je .error_out_of_bounds

    cmp rax, [random]
    je .you_got_it

    mov rsi, msg_try_again
    mov rdx, msg_try_again_len
    call _print
    jmp .guess_a_number

.exit_success:
    mov rax, SYS_EXIT
    mov rdi, EXIT_SUCCESS
    syscall


.error_read_fail:
    mov rsi, msg_read_fail
    mov rdx, msg_read_fail_len
    call _print
    jmp .guess_a_number

.error_invalid_number:
    call _print_input
    mov rsi, msg_invalid_number
    mov rdx, msg_invalid_number_len
    call _print
    jmp .guess_a_number

.error_out_of_bounds:
    call _print_input
    mov rsi, msg_out_of_bounds
    mov rdx, msg_out_of_bounds_len
    call _print
    jmp .guess_a_number

.give_up:
    mov rsi, msg_give_up
    mov rdx, msg_give_up_len
    call _print
    jmp .exit_success

.you_got_it:
    call _print_input
    mov rsi, msg_you_got_it
    mov rdx, msg_you_got_it_len
    call _print
    jmp .exit_success