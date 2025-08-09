section .rodata
    string db 'galera do baixo nivel', 0
    format db 'Salve, %s!', '\n', 0

section .text
global main

extern printf

main:
    lea rdi, [rel format] ; rel = relative address, para PIE (position independent executable)
    lea rsi, [rel string] 
    call [rel printf wrt ..got] ; wrt = with relative table, got = global object table


    xor rax, rax
    ret

