section .text
global _start

; ----------------------------------------------------------

str_len:
    ; inputs:
    ; rsi -> const char*
    ; outputs:
    ; rax -> number of chars
    xor rcx, rcx
    xor rax, rax
.count_loop:
    mov al, byte [rsi]
    cmp al, 0
    je .done

    inc rcx
    inc rsi
    jmp .count_loop

.done:
    mov rax, rcx
    ret

; ----------------------------------------------------------

print_str:
    ; inputs:
    ; rsi -> const char*
    ; outputs:
    ; rax -> return value for syscall write
    push rsi
    call str_len
    mov rcx, rax
    pop rsi

    mov rax, 1
    mov rdi, 1
    mov rdx, rcx
    syscall
    ret

print_eol:
    push 0x0a   ; push '\0' onto the stack
    mov rax, 1
    mov rdi, 1
    mov rsi, rsp
    mov rdx, 1
    syscall
    add rsp, 8  ; pop 0x0a from the stack without saving its value
    ret

; ----------------------------------------------------------

i64_count_digits:
    mov rcx, 1
    mov r8, 10
    mov rax, rdi
.loop:
    xor rdx, rdx
    div r8
    cmp rax, 0
    je .return

    inc rcx
    jmp .loop

.return:
    mov rax, rcx
    ret

_start:
    xor r10, r10                    ; set counter to zero
.argv_loop:
    mov rsi, [rsp + 8 + (8 * r10)]  ; rsi receives the address of argv[0]
    cmp rsi, 0
    je _exit_success

    call print_str
    call print_eol
    inc r10
    jmp .argv_loop

_exit_success:
    mov rdi, 12345
    call i64_count_digits
    mov rdi, rax
    mov rax, 60
    syscall

; ----------------------------------------------------------
