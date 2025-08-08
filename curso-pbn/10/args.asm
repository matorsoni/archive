_start:
    call print_args
    call _exit

print_args:
    xor rcx, rcx
.loop:
    lea rdx, [rsp + 8 * rcx + 16]
    mov rsi, [rdx]

    test rsi, rsi
    jz .return

    push rcx
    call echo_str
    pop rcx

    inc rcx
    jmp .loop
.return:
    ret
