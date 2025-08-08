section .bss
	buf resd 5		; espaço para 19 caracteres + '\0'
	
section .rodata
	txt db "abcdefghij", 0	; string com 10 caracteres + '\0'

section .text
global _start
_start:

; Tamanho da string em 'txt' -------------------------------
	
	mov rsi, txt		;endereço do primeiro caractere
	call str_len		; retorna quantidade de caracteres em rax

; Impressão da string em 'txt' -----------------------------

_bufp:
	mov rsi, txt
	call echo_str

; Cópia da string no buffer em 'buf' -----------------------

_bufw:
	mov rsi, txt		; endereço do primeiro caractere
	mov rdi, buf		; endereço do buffer
	call write_buf		; escreve no buffer e retorna quantidade em rax

; Impressão da string em 'buf' -----------------------------

	mov rsi, buf
	call echo_str

; Cópia invertida da string no buffer em 'buf' -------------

_bufr:
	mov rsi, txt		; char *str
	call str_len		; retorna tamanho em rax

	mov rdx, rax		; quantidade de bytes
	mov rsi, txt		; char *str
	mov rdi, buf		; char *buf
	call rev_buf		; inverte str em buf

; Impressão da string invertida em 'buf' -------------------

	mov rsi, buf
	call echo_str
	
_exit:
	mov rax, 60
	xor rdi, rdi
	syscall

; ----------------------------------------------------------
str_len:
; ----------------------------------------------------------
; Entrada: rsi -> char *str (endereço da string)
; Saída  : rax -> quantidade de caracteres excluindo '\0'
; ----------------------------------------------------------
	xor rax, rax		; limpa rax para receber os bytes
	xor rcx, rcx		; contador = 0
.count_loop:
	mov al, byte [rsi]	; copia byte em rsi para rax
	cmp al, 0		; o byte em rax é 0x00?
	je .done
	
	inc rsi			; próximo byte
	inc rcx			; contador += 1
	jmp .count_loop
.done:
	mov rax, rcx
	ret

; ----------------------------------------------------------
write_buf:
; ----------------------------------------------------------
; Entradas:
;   rsi -> char *src (endereço da string)
;   rdi -> char *buf (endereço do buffer)
; Saída:
;   rax -> quantidade de bytes escritos
; ----------------------------------------------------------
	xor rax, rax		; limpa rax para receber os bytes
	xor rcx, rcx		; contagem de bytes = 0
.write_loop:
	mov al, byte [rsi]	; copia byte em rsi para rax
	cmp al, 0		    ; o byte em rax é 0x00?
	je .done

	mov [rdi], al		; copia bite de 'txt' em 'buf' 
	inc rsi			    ; próximo byte em 'txt'
	inc rdi			    ; próximo espaço em 'buf'
	inc rcx			    ; contador += 1
	jmp .write_loop
.done:
	mov rax, rcx		; retorno em rax
	ret

; ----------------------------------------------------------
print_str:
; ----------------------------------------------------------
; Entradas:
;   rsi -> char *src (endereço da string)
;   rdx -> uint64 size (quantidade de bytes a imprimir)
; ----------------------------------------------------------
	push rsi
	call str_len	
	
	mov rdx, rax
	pop rsi
	
	mov rax, 1
	mov rdi, 1
	syscall
	ret
	
; ----------------------------------------------------------
print_eol:
; ----------------------------------------------------------
; Não tem entradas
; ----------------------------------------------------------
	push 0x0a		; salva '\n' na pilha
	mov rax, 1
	mov rdi, 1
	mov rsi, rsp
	mov rdx, 1
	syscall
	add rsp, 8		; restaura o topo da pilha
	ret

; ----------------------------------------------------------
rev_buf:
; ----------------------------------------------------------
; Entradas:
;   rdi -> char *buf (buffer para string invertida)	
;   rsi -> char *src (endereço da string)
;   rdx -> uint64 size (quantidade de bytes a imprimir)
; Saída:
;   rax -> quantidade de bytes
; ----------------------------------------------------------
	push rdx		; salva quantidade de bytes na pilha
	xor rax, rax	; zera rax para receber bytes
	mov rcx, rdx	; rcx será o índice de str[i]
	dec rcx			; rcx = size-1 -> 0
.write_loop:
	cmp rcx, 0		; contagem chegou a zero?
	jl .done		; se menor, termina
	
	mov al, byte [rsi+rcx]	; salva byte str[rcx] em rax
	mov [rdi], al	    	; copia byte da origem no buffer
	dec rcx			        ; decrementa a contagem
	inc rdi			        ; próximo byte no buffer
	jmp .write_loop
.done:
	pop rax
	ret
	
; ----------------------------------------------------------
echo_str:
; ----------------------------------------------------------
; Entradas:
;   rsi -> char *src (endereço da string)
;   rdx -> uint64 size (quantidade de bytes a imprimir)
; ----------------------------------------------------------
	call print_str
	call print_eol
	ret
