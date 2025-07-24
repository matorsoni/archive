; 1. obter endereco armazenado em rsp (endereco de argc)
; obviamente o endereco ja esta em rsp
; como obter o dado armazenado nesse endereco?
; armazenar o valor no endereco em um registrador


; 2. converter o valor de argc (uint64) em string (terminada em '\0')
; Exemplo: 123
; 123 / 10 = 12 resto 3 -> soma 48 (0x30) -> 0x33 (ascii)
;  12 / 10 = 1  resto 2 -> soma 48 (0x30) -> 0x32 (ascii)
;   1 / 10 = 0  resto 1 -> soma 48 (0x30) -> 0x31 (ascii)
; 3. imprimir argc
; imprimir o passo 2 na ordem inversa


; 4. zerar um reg pra servir de indice


; 5. obter o endereco do elemento de argv
; esta em multiplo de 8 bytes depois do endereco de argc: rsp + 8*(index+1) bytes
; armazenar a indirecao (deference) desse endereco em outro registrador


; 6. obter o valor do elemento de argv
; armazenar a indirecao do endereco em outro registrador


; comparar o valor de argv com 0 (null)
; - se for NULL: encerrar


; 7. imprimir string do argumento
; nao sabemos o tamanho da string, entao podemos:
; imprimir cada byte da string ate encontrar '\0';
; ou calcular o tamanho da string e imprimir ela toda (basicamente implementar strlen)


; 8. avancar para o prox endereco da pilha (pode ser NULL ou proximo elemento de argv)
; incrementar o indice
; voltar ao passo 5


section .text
    global _start

_start:
    mov rax, [rsp]
    ;call print_int
    xor rcx, rcx ; ou entao: mov rcx, 0

_args_loop:
    lea rdx, [rsp + 8 * rcx + 8] ; lea = load effective address
    mov rsi, [rdx]
    test rsi, rsi
    jz _exit ; jump if zero to rotulo _exit

    call print_str
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
    push rcx          ; salva rcx na pilha, para nao perder o seu valor
    push rdx
    mov rax, 1        ; syscall write
                      ; atencao: write afeta rax, rcx e r11
                      ; como rax recebera valor 1 (1 byte escrito) e salvamos rcx, funciona
                      ; mas deve se tomar cuidado com os valores alterados
    mov rdi, 1        ; file descriptor (fd) code
    ; mov rsi, ...    ; rsi ja esta com o endereco (char*) desejado (mov rsi, [rdx])
    mov rdx, 1        ; write just 1 byte

.char_loop:
    cmp byte [rsi], 0
    je .done          ; if *(char*)(rsi) == 0 { return }
    syscall
    inc rsi           ; rsi++
    jmp .char_loop

.done:
    pop rdx
    pop rcx
    ret
