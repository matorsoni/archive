; 1. obter endereco armazenado em rsp (endereco de argc)
; obviamente o endereco ja esta em rsp
; como obter o dado armazenado nesse endereco?
; armazenar o valor no endereco em um registrador

    mov rax, [rsp]

; 2. converter o valor de argc (uint64) em string (terminada em '\0')
; Exemplo: 123
; 123 / 10 = 12 resto 3 -> soma 48 (0x30) -> 0x33 (ascii)
;  12 / 10 = 1  resto 2 -> soma 48 (0x30) -> 0x32 (ascii)
;   1 / 10 = 0  resto 1 -> soma 48 (0x30) -> 0x31 (ascii)
; 3. imprimir argc
; imprimir o passo 2 na ordem inversa

    call print_int

; 4. zerar um reg pra servir de indice

    xor rcx, rcx ; ou entao: mov rcx, 0

; 5. obter o endereco do elemento de argv
; esta em multiplo de 8 bytes depois do endereco de argc: rsp + 8*(index+1) bytes
; armazenar a indirecao (deference) desse endereco em outro registrador

_args_loop:
    lea rdx, [rsp + 8 * rcx + 8] ; lea = load effective address

; 6. obter o valor do elemento de argv
; armazenar a indirecao do endereco em outro registrador

    mov rax, [rdx]

; comparar o valor de argv com 0 (null)
; - se for NULL: encerrar

    test rax, rax
    jz _exit ; jump if zero to rotulo _exit

; 7. imprimir string do argumento
; nao sabemos o tamanho da string, entao podemos:
; imprimir cada byte da string ate encontrar '\0';
; ou calcular o tamanho da string e imprimir ela toda (basicamente implementar strlen)

    call print_str

; 8. avancar para o prox endereco da pilha (pode ser NULL ou proximo elemento de argv)
; incrementar o indice
; voltar ao passo 5

    inc rcx
    jmp _args_loop


_exit:
    mov rax, 60
    xor rdi, rdi
    syscall

print_int:
    ; ...
    ret

print_str:
    ; ...
    ret
