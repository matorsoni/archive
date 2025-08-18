;------------------------------------------------------------------------------
; Guess Game in 300 lines of x86_64 assembly
; By: Mateus Orsoni
; August/2025
;
; * * *
;
; Build and run:
;
; nasm -felf64 -g guess.asm
; ld guess.o -o guess
; ./guess
;------------------------------------------------------------------------------

;------------------------------------------------------------------------------
; Defines
;------------------------------------------------------------------------------

%define SYS_READ  0
%define SYS_WRITE 1
%define SYS_EXIT  60
%define STDIN_FD  0
%define STDOUT_FD 1
%define EXIT_SUCCESS 0
%define EXIT_FAIL    1
%define EOL_CHAR     0x0a

%define READ_BUF_SIZE 256

;------------------------------------------------------------------------------
; Section RODATA
;------------------------------------------------------------------------------

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

    msg_try_lower db `Nope! Try a lower number.\n\n`
    msg_try_lower_len equ $ - msg_try_lower

    msg_try_higher db `Nope! Try a higher number.\n\n`
    msg_try_higher_len equ $ - msg_try_higher

;------------------------------------------------------------------------------
; Section BSS
;------------------------------------------------------------------------------

section .bss
    read_buf    resb READ_BUF_SIZE
    bytes_read  resq 1
    random      resq 1

;------------------------------------------------------------------------------
; Section TEXT
;------------------------------------------------------------------------------

section .text

; Print string in rsi to stdout
; Input: rsi -> char* src
;        rdx -> size_t len
; Changes: rax, rdi
print:
    mov rax, SYS_WRITE
    mov rdi, STDOUT_FD
    syscall
    ret

; Print string in read_buf to stdout
; Changes: rax, rdi, rsi, rdx
print_from_buf:
    mov rsi, read_buf
    mov rdx, [bytes_read]
    call print
    ret


; Generates a random number between 1 and 100 using Linux syscall 'getrandom'
;   ~ ssize_t getrandom(void* buf, size_t len, uint32_t flags)
;
; Output:  rdx -> random integer from 1 to 100
; Changes: rax, rdi, rsi, rdx, rcx
random_1_100:
    mov rax, 318      ; syscall getrandom
    mov rdi, random   ; pointer to buffer
    mov rsi, 8        ; write 8 bytes to buffer
    xor rdx, rdx      ; flags = 0
    syscall

    ; [random] now holds a 64 bit random number
    mov rax, [random]
    xor rdx, rdx
    mov rcx, 100
    div rcx            ; rax = rax / 100, rdx = rax % 100
    inc rdx            ; rdx in range [0 ... 99] -> [1 ... 100]
    mov [random], rdx  ; store final random number in [random]
    ret

; Check if input string is a valid number between 1 and 100.
; Examples: '1234'      -> valid number, out of bounds
;           '-0001'     -> valid number, out of bounds
;           '+000021'   -> valid number, between 1 and 100
;           '2a843fqc'  -> not a valid number
;
; Input:  rsi -> const char* src
; Output: rax -> converted integer
;         r8  -> 1 if number is valid, 0 if not
;         r9  -> 0 if number is between 1-100, 0 if not
; Changes: rax, rbx, rcx, rdx, r8, r9
check_valid_number:
    xor rax, rax    ; converted integer          = 0
    xor rbx, rbx    ; byte read from buffer      = 0
    xor rcx, rcx    ; index                      = 0
    xor r8, r8      ; 'valid number' flag        = false
    xor r9, r9      ; 'out of bounds 1-100' flag = false

    ; Check if first char is '-'
    mov bl, byte [rsi]
    cmp bl, '-'           ; if src[0] == '-', set out of bounds to true and increment index
    jne .check_plus
    mov r9, 1             ; out of bounds = true
    inc rcx               ; index++
    jmp .digit_loop

.check_plus:
    cmp bl, '+'           ; if src[0] == '+', increment index
    jne .digit_loop
    inc rcx               ; index++

.digit_loop:
    mov bl, byte [rsi+rcx]     ; Read character from buffer
    cmp bl, 0                  ; if char is '\0', jump to finish
    je .end_of_string

    cmp bl, 0x30               ; Check if char is a digit: >= '0' (0x30) and <= '9' (0x39)
    jl .not_a_digit            ; If so, it's not a valid number
    cmp bl, 0x39
    jg .not_a_digit

    mov r8, 1           ; valid number = true
    cmp r9, 1           ; if converted number is already out of bonds, continue to next character
    je .next_iter

    sub bl, 0x30		; convert char to integer
    imul rax, rax, 10   ; rax = rax * 10
    add rax, rbx        ; rax = rax + rbx

    cmp rax, 100
    jle .next_iter
    mov r9, 1           ; if rax > 100, set ouf of bounds to true

.next_iter:
    inc rcx             ; index++
    jmp .digit_loop

.end_of_string:
    cmp rax, 0
    jg .finish
    mov r9, 1           ; if rax <= 0, set ouf of bounds to true

.finish:
    ret

.not_a_digit:
    xor r8, r8          ; set valid number to false and return
    ret


;------------------------------------------------------------------------------
; Main subroutine
;------------------------------------------------------------------------------
global _start
_start:

    ; Save random number to be guessed
    call random_1_100

.guess_a_number:
    ; print guess message
    mov rsi, msg_guess
    mov rdx, msg_guess_len
    call print

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

    ; Remove last character and decrease buffer size if it's '\n' (0x0a)
    ; Example: '123\n\0' (len == 4) -> '123\0\0' (len == 3)
    xor rbx, rbx
    mov bl, byte [read_buf + rax - 1]
    cmp bl, EOL_CHAR
    jne .buffer_ready
    mov byte [read_buf + rax - 1], 0
    dec rax

.buffer_ready:
    ; Save number of bytes read into bytes_read
    mov [bytes_read], rax

    ; Give up if input was exactly 'q' (0x71)
    ; i.e, if [bytes_read] == 1 and read_buf[0] == 'q'
    cmp rax, 1
    jne .dont_give_up
    xor rbx, rbx
    mov bl, byte [read_buf]
    cmp bl, 0x71
    je .give_up

.dont_give_up:

    mov rsi, read_buf
    call check_valid_number

    cmp r8, 0
    je .error_invalid_number

    cmp r9, 1
    je .error_out_of_bounds

    cmp rax, [random]
    jl .try_higher
    jg .try_lower

.you_got_it:
    call print_from_buf
    mov rsi, msg_you_got_it
    mov rdx, msg_you_got_it_len
    call print

.exit_success:
    mov rax, SYS_EXIT
    mov rdi, EXIT_SUCCESS
    syscall


.error_read_fail:
    mov rsi, msg_read_fail
    mov rdx, msg_read_fail_len
    call print
    jmp .guess_a_number

.error_invalid_number:
    call print_from_buf
    mov rsi, msg_invalid_number
    mov rdx, msg_invalid_number_len
    call print
    jmp .guess_a_number

.error_out_of_bounds:
    call print_from_buf
    mov rsi, msg_out_of_bounds
    mov rdx, msg_out_of_bounds_len
    call print
    jmp .guess_a_number

.give_up:
    mov rsi, msg_give_up
    mov rdx, msg_give_up_len
    call print
    jmp .exit_success

.try_lower:
    mov rsi, msg_try_lower
    mov rdx, msg_try_lower_len
    call print
    jmp .guess_a_number

.try_higher:
    mov rsi, msg_try_higher
    mov rdx, msg_try_higher_len
    call print
    jmp .guess_a_number
