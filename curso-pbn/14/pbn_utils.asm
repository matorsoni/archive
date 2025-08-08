%ifndef PBN_UTILS
%define PBN_UTILS
; ----------------------------------------------------------
%define SYS_WRITE 1
%define SYS_EXIT  60
; ----------------------------------------------------------
%define STDIN_FD  0
%define STDOUT_FD 1
%define STDERR_FD 2
; ----------------------------------------------------------
%define EXIT_OK   0
%define EXIT_FAIL 1
; ----------------------------------------------------------
%define EOL_CHAR  0x0a
; ----------------------------------------------------------
%define INT64_MIN 0x8000000000000000
%define INT64_MAX 0x7fffffffffffffff
; ----------------------------------------------------------
; Sub-rotinas...
; ----------------------------------------------------------
; - write_buf: copia string (rsi) para um buffer (rdi).
; - rev_buf  : inverte e salva string (rsi) em um buffer (rdi).
; - str_len  : obtém o tamanho de uma string (rsi).
; - print_str: imprime string (rsi)
; - print_eol: imprime quebra de linha.
; - echo_str : imprime string (rsi) com uma quebra de linha.
; - i64_count_digits: conta dígitos de um inteiro (base 10).
; - u64_to_str: converte inteiro sem sinal para string.
; ----------------------------------------------------------
write_buf:
; ----------------------------------------------------------
; Descrição: Copia string em rsi no buffer em rdi.
; Entradas:
;   rsi -> char *str (endereço da string)
;   rdi -> char *buf (endereço do buffer)
; Saída:
;   rsi -> char *buf (endereço do buffer)
; Altera: rax, rcx, r8, rsi (retorno)
; ----------------------------------------------------------
	mov r8, rdi		; r8 => endereço do buffer
.write_loop:
	mov al, byte [rsi]	; copia byte em rsi para rax
	cmp al, 0		; o byte em rax é 0x00?
	je .done

	mov [r8], al		; copia bite de 'txt' em 'buf' 
	inc r8			; próximo espaço em 'buf'
	inc rsi			; próximo byte da string
	jmp .write_loop
.done:
	mov byte [r8], 0	; garante terminador nulo
	mov rsi, rdi		; rsi => endereço do buffer 
	ret
; ----------------------------------------------------------
rev_buf:
; ----------------------------------------------------------
; Descrição: Inverte string em rsi e salva no buffer em rdi.
; Entradas:
;   rdi -> char *buf (buffer para string invertida)	
;   rsi -> char *str (endereço da string)
; Saída:
;   rsi -> char *buf (endereço do buffer)
; Altera: rax, rcx, r8, rsi (retorno)
; Depende de str_len!
; ----------------------------------------------------------
	call str_len		; retorna tamanho da string em rax
	mov r8, rdi		; r8 => endereço do buffer
	mov rcx, rsi		; rcx => endereço da string
	add rcx, rax		; rcx => terminador da string
	dec rcx			; rcx => último caractere
.write_loop:
	mov al, byte [rcx]	; salva byte str[rcx] em rax
	mov byte [r8], al	; copia byte da origem no buffer
	dec rcx			; byte anterior na string
	inc r8			; próximo byte no buffer
	cmp rcx, rsi		; rcx < início da string?
	jb .done		; se menor, termina
	jmp .write_loop
.done:
	mov byte [r8], 0	; garante terminador nulo
	mov rsi, rdi		; rsi => endereço do buffer
	ret
; ----------------------------------------------------------
str_len:
; ----------------------------------------------------------
; Descrição: obtém o tamanho da string em rsi.
; Entrada  : rsi -> char *str (endereço da string)
; Saída    : rax -> quantidade de caracteres excluindo '\0'
; Altera   : rax (retorno), rcx
; ----------------------------------------------------------
	xor rcx, rcx		; contador = 0
.count_loop:
	mov al, byte [rsi+rcx]	; copia byte em rsi[rcx] para rax
	cmp al, 0		; o byte em rax é 0x00?
	je .done

	inc rcx			; contador += 1
	jmp .count_loop
.done:
	mov rax, rcx
	ret
; ----------------------------------------------------------
print_str:
; ----------------------------------------------------------
; Descrição: Imprime string em rsi.
; Entrada  : rsi -> char *src (endereço da string)
; Altera   : rax, rcx, rdx, rdi, r11	
; Depende de str_len!
; ----------------------------------------------------------
	call str_len		; retorna str_len em rax
	mov rdx, rax
	mov rax, SYS_WRITE
	mov rdi, STDOUT_FD
	syscall
	ret
; ----------------------------------------------------------
print_eol:
; ----------------------------------------------------------
; Descrição: Imprime uma quebra de linha.
; Entrada  : não tem entradas
; Altera   : rax, rcx, rdx, rdi, rsi, r11
; ----------------------------------------------------------
	push EOL_CHAR		; salva '\n' na pilha
	mov rax, SYS_WRITE
	mov rdi, STDOUT_FD
	mov rsi, rsp
	mov rdx, 1
	syscall
	add rsp, 8		; restaura o topo da pilha
	ret
; ----------------------------------------------------------
echo_str:
; ----------------------------------------------------------
; Descrição: Imprime string em rsi com uma quebra de linha.
; Entrada  : rsi -> char *src (endereço da string)
; Saída    : Nenhuma
; Altera   : rax, rcx, rdx, rdi, rsi, r11
; Depende de str_len, print_str e print_eol!
; ----------------------------------------------------------
	call print_str
	call print_eol
	ret
; ----------------------------------------------------------
i64_count_digits:
; ----------------------------------------------------------
; Descrição: Conta dígitos de uma constante inteira (int64).
; Entrada  : rdi -> Valor int64 (inteiro com ou sem sinal)
; Saída    : rax -> Quantidade de dígitos
; Altera   : rax (retorno), rcx, r8, r9
; ----------------------------------------------------------
	mov r8, rdi		; salva rdi em r8
	mov rax, 1		; inicia rax = 1 dígito
	test r8, r8		; inteiro é negativo ou zero?
	jz .done		; se ZF=1, retorna rax = 1 (10^0)
	jns .count_start	; se SF=0, salta para contagem
.sig_handler:
	mov r9, INT64_MIN	; 'cmp' só aceita imm ate 32 bits
	cmp r8, r9		; INT64_MIN não pode ser negado!
	je .int64_min		; rax = 19 dígitos
	neg r8			; r8 => valor agora é positivo
.count_start:
	mov rcx, 10		; potência de 10 inicial (10^1)
.count_loop:
	cmp r8, rcx		; num < 10^rax?
	jb .done		; sem menor, termina
	inc rax			; incrementa o contador
	imul rcx, rcx, 10	; rcx = rcx * 10 => 10^rax
	jmp .count_loop
.int64_min:
	mov rax, 19		; INT64_MIN tem 19 bytes
.done:
	ret
; ----------------------------------------------------------
u64_to_str:
; ----------------------------------------------------------
; Descrição: Converte inteiro (uint64) para string.
; Entradas:
;   rdi -> valor uint64 (sem sinal)
;   rsi -> endereço do buffer de saída
; Saída:
;   rsi -> endereço do buffer
; Altera: rax, rcx, rdx, r8
; Depende de i64_count_digits!	
; ----------------------------------------------------------
	call i64_count_digits	; retorna dígitos em rax
	mov rcx, rsi		; rcx => endereço inicial do buffer
	add rcx, rax		; rcx => fim da string + 1
	mov byte [rcx], 0	; terminador nulo
	dec rcx			; rcx => byte anterior no buffer
	
	mov rax, rdi		; copia valor para rax (dividendo)
	mov r8, 10		; r8 = 10 (divisor)
.convert_loop:
	xor rdx, rdx		; zera rdx para o resto (dígito)
	div r8			; rax = valor/10, rdx = valor%10
	add dl, 0x30		; converte resto para ASCII
	mov byte [rcx], dl	; salva caractere no buffer
	dec rcx			; endereço do byte anterior
	cmp rcx, rsi		; rsi < rcx?
	jb .done
	jmp .convert_loop
.done:
	ret
; ----------------------------------------------------------
i64_to_str:
; ----------------------------------------------------------
; Descrição: Converte inteiro (int64) para string.
; Entradas:
;   rdi -> valor uint64 (com ou sem sinal)
;   rsi -> endereço do buffer de saída
; Saída:
;   rsi -> endereço do buffer
; Altera: rax, rcx, rdx, r8, r9, r10
; Depende de i64_count_digits!	
; ----------------------------------------------------------
	call i64_count_digits	; retorna dígitos em rax
	xor r9, r9		; r9 (índice do início do buffer) = 0
	test rdi, rdi		; número tem sinal? (precisa testar de novo?)
	jns .write_term		; se não tem, escreve o terminador
.int64_min:
	mov r10, INT64_MIN	; 'cmp' só aceita imm até 32 bits
	cmp rdi, r10		; INT64_MIN não pode ser negado!
	je .write_int64min	; esrceve os caracteres de INT64_MIN
.sig_handler:
	neg rdi			; torna número positivo (absoluto)
	inc rax			; inclui o sinal na contagem de caracteres
	inc r9			; r9 (novo índice inicial do buffer) = 1
	mov byte [rsi], '-'	; escreve o sinal no início do buffer
.write_term:
	mov rcx, rax		; rcx => índice do fim da string + 1
	mov byte [rsi+rcx], 0	; terminador nulo
	dec rcx			; rcx => byte anterior no buffer
.convert_start:
	mov rax, rdi		; copia valor para rax (dividendo)
	mov r8, 10		; r8 = 10 (divisor)
.convert_loop:
	xor rdx, rdx		; zera rdx para o resto (dígito)
	div r8			; rax = valor/10, rdx = valor%10
	add dl, 0x30		; converte resto para ASCII
	mov byte [rsi+rcx], dl	; salva caractere no buffer
	dec rcx			; endereço do byte anterior
	cmp rcx, r9		; rcx < r9?
	jl .done		; se for, termina
	jmp .convert_loop
.done:
	ret
.write_int64min:
	; Escreve diretamente em rsi os caracteres de INT64_MIN...
	mov dword [rsi], '-922'
	mov dword [rsi+4], '3372'
	mov dword [rsi+8], '0368'
	mov dword [rsi+12], '5477'
	mov dword [rsi+16], '5808'
	mov byte [rsi+20],  0
	ret
; ----------------------------------------------------------

%endif
