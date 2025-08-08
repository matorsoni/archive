;----------------------------------------------------
%define SYS_READ    0
%define SYS_WRITE   1
%define SYS_OPEN    2
%define SYS_CLOSE   3
%define SYS_EXIT    60
;----------------------------------------------------
%define STDOUT      1
%define STDERR      2
;----------------------------------------------------
%define EXIT_OK     0
%define EXIT_USE_ER 1
%define EXIT_OPE_ER 2
;----------------------------------------------------
%define BUF_SIZE    8192 
;----------------------------------------------------
%define O_RDONLY    0
;----------------------------------------------------

section .rodata
    use_msg db "Uso: ./gato <nome_do_arquivo>", 10, 0
    use_len equ $ - use_msg

    err_msg db "Erro: não foi possível abrir o arquivo", 10, 0
    err_len equ $ - err_msg

section .bss
    buf resb BUF_SIZE       ; buffer para leitura do arquivo
    fd  resq 1              ; local para guardar o descritor do arquivo

section .text
    global _start

_start:
    ; Verificando se foi passado um nome de arquivo como argumento
    pop rax                 ; argc agora está em rax
    cmp rax, 2              ; Tem 2 argumentos?
    jne use_error           ; Se não, vá para use_error

    ; Salvando argv[1] em rdi
    pop rax                 ; endereço de argv[0] agora está em rax
    pop rdi                 ; endereço de argv[1] agora está em rdi
    
    ; Abrindo o arquivo (rdi já aponta para o nome do arquivo)
    mov rax, SYS_OPEN       ; syscall open
    mov rsi, O_RDONLY       ; flag somente leitura
    mov rdx, 0              ; usado apenas quando um novo arquivo é criado
    syscall

    cmp rax, 0              ; o arquivo foi aberto com sucesso?
    jl open_error           ; se rax < 0, vá para open_error
    mov [fd], rax           ; Salvando o descritor de arquivo na memória

read_loop:
    ; Lendo o arquivo
    mov rax, SYS_READ       ; syscall read
    mov rdi, [fd]           ; descritor do arquivo em rdi
    mov rsi, buf            ; buffer de leitura
    mov rdx, BUF_SIZE       ; quantidade de bytes para leitura
    syscall

    ; Verificando se chegamos ao fim do arquivo
    cmp rax, 0              ; rax <= 0?
    jle close_file          ; se sim, fim de arquivo. Vá para close_file

    ; Escrevendo a leitura do arquivo na saída padrão (STDOUT)
    mov rdx, rax            ; quantidade de bytes lidos
    mov rax, SYS_WRITE      ; syscall write
    mov rdi, STDOUT         ; saída padrão
    mov rsi, buf            ; buffer com a leitura do arquivo
    syscall

    jmp read_loop

close_file:
    ; Fechando o arquivo
    mov rax, SYS_CLOSE      ; syscall close
    mov rdi, [fd]           ; descritor do arquivo a ser fechado
    syscall

    ; Saindo com sucesso (código de término 0)
    mov rax, SYS_EXIT       ; syscall exit
    xor rdi, rdi            ; rdi = 0
    syscall

use_error:
    ; Mostrando mensagem de uso correto
    mov rax, SYS_WRITE      ; syscall write
    mov rdi, STDERR         ; saída de erro padrão (STDERR)
    mov rsi, use_msg        ; endereço da mensagem a exibir
    mov rdx, use_len        ; tamanho da mensagem
    syscall

    ; Saindo com código de erro 1
    mov rax, SYS_EXIT       ; syscall exit
    mov rdi, EXIT_USE_ER    ; rdi = 1
    syscall

open_error:
    ; Mostrando mensagem de erro na abertura do arquivo
    mov rax, SYS_WRITE      ; syscall write
    mov rdi, STDERR         ; saída de erro padrão (STDERR)
    mov rsi, err_msg        ; endereço da mensagem a exibir
    mov rdx, err_len        ; tamanho da mensagem
    syscall

    ; Saindo com código de erro 2
    mov rax, SYS_EXIT       ; syscall exit
    mov rdi, EXIT_OPE_ER    ; rdi = 2
    syscall
