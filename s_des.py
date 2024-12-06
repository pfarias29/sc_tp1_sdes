
### Função de encriptação S-DES ###
# Parâmetros: chave (key) e bloco de texto (block)
# Retorno: bloco de texto encriptado
# Passos:
# 1. Geração das sub-chaves
# 1.1 Reorganização dos bits da chave
# 1.2 Deslocamento circular
# 1.3 Seleção de 8 bits e permutação deles (K1)
# 1.4 Deslocamento circular duplo
# 1.5 Seleção de 8 bits e permutação deles (K2)
# 2. Permutação Inicial (IP)
# 3. Divisão do bloco de texto em duas partes (L0 e R0)
# 4. Rodadas de Feistel
# 4.1 Função de aplicada a R0 e Ki, possui expansão/permutação, S-Box e permutação
# 4.2 Resultado da função XOR com L0
# 4.3 Troca de L0 e R0
# 5. Permutação Final (IP^{-1})

### Função de geração de sub-chaves ###
def key_generation(key):

    # Tranforma a chave em uma lista e reorganiza os bits
    key = list(key)
    first_permutation = [0 for i in range(10)]
    P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]

    for i in range(10):
        first_permutation[i] = key[P10[i] - 1]

    
    # Separa a chave em duas partes e faz um deslocamento circular
    first_half = first_permutation[:5]
    second_half = first_permutation[5:]

    first_half.append(first_half.pop(0))
    second_half.append(second_half.pop(0))

    circular_shift = first_half + second_half

    # Seleciona 8 bits e faz uma permutação
    P8 = [6, 3, 7, 4, 8, 5, 10, 9]
    K1 = [0 for i in range(8)]
    for i in range(8):
        K1[i] = int(circular_shift[P8[i] - 1])

    # Separa a chave em duas partes e faz um deslocamento circular duplo
    first_half = circular_shift[:5]
    second_half = circular_shift[5:]

    for i in range(2):
        first_half.append(first_half.pop(0))
        second_half.append(second_half.pop(0))
    
    circular_shift = first_half + second_half

    # Seleciona 8 bits e faz uma permutação
    K2 = [0 for i in range(8)]
    for i in range(8):
        K2[i] = int(circular_shift[P8[i] - 1])

    return K1, K2

### Função F do Feistel ###
def f_function(L, R, key):
    expansion_permutation = [[4, 1, 2, 3], 
                             [2, 3, 4, 1]]
    
    # Expansão/Permutação de R e XOR com a chave
    matrix = [[0] * 4 for _ in range(2)]
    for i in range(2):
        for j in range(4):
            matrix[i][j] = int(bool(R[expansion_permutation[i][j] - 1]) ^ bool(key[i + j]))

    print(matrix)

            


def s_des(key, block):
    K1, K2 = key_generation(key)
    block = list(block)

    # Permutação Inicial
    IP = [2, 6, 3, 1, 4, 8, 5, 7]
    first_permutation = [0 for i in range(8)]
    for i in range(8):
        first_permutation[i] = int(block[IP[i] - 1])

    # Divisão do bloco de texto em duas partes
    L0 = block[:4]
    R0 = block[4:]
    f_function(L0, R0, K1)

    
    IP_1 = [4, 1, 3, 5, 7, 2, 8, 6]
    for i in range(8):
        print(first_permutation[IP_1[i] - 1], end="")

    

    return 0

if __name__ == "__main__":
    key = "1010000010"
    block = "11010111"
    s_des(key, block)