.intel_syntax noprefix
.globl main
.type main, @function

main:
    jmp pop_payload

decode_setup:
    pop r10
    mov rdx, r10
    mov rdi, 0x6262626262626262
    add r10, rdi
    xor rax, rax
    xor rcx, rcx

decode_loop:
    mov al, [r10 + rcx]
    xor al, [rdx + rcx]
    mov [rdx + rcx], al
    inc rcx
    cmp rcx, rdi
    jne decode_loop
    xor rax, rax
    mov [rdx + rcx], al
    jmp payload

pop_payload:
    call decode_setup

payload:
