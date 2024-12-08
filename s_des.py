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
    K1 = [0 for _ in range(8)]
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
    ## Cria uma matriz 2x4 para armazenar os valores de R e a chave
    ## Faz um XOR com os valores booleanos de R e a chave e transforma em inteiros
    matrix = [[0] * 4 for _ in range(2)]
    for i in range(2):
        for j in range(4):
            matrix[i][j] = int(bool(int(R[expansion_permutation[i][j] - 1])) ^ bool(key[(4 * i) + j]))

    # S-Boxes
    S0 = [[1, 0, 3, 2],
          [3, 2, 1, 0],
          [0, 2, 1, 3],
          [3, 1, 3, 2]]
    
    S1 = [[0, 1, 2, 3],
          [2, 0, 1, 3],
          [3, 0, 1, 0],
          [2, 1, 0, 3]]
    
    matrix_S_Box = []
    # Pega os valores da matriz e transforma em binário
    ## P(i,0) + P(j,3) = linha
    ## P(i,1) + P(j,2) = coluna
    for i in range(2):
        if i == 0:
            row = int(str(matrix[i][0]) + str(matrix[i][3]), 2)
            col = int(str(matrix[i][1]) + str(matrix[i][2]), 2)
            res = list(format(S0[row][col], '02b'))
            matrix_S_Box += res
        else:
            row = int(str(matrix[i][0]) + str(matrix[i][3]), 2)
            col = int(str(matrix[i][1]) + str(matrix[i][2]), 2)
            res = list(format(S1[row][col], '02b'))
            matrix_S_Box += res
    
    # Permutação pós-S-Boxes
    P4 = [2, 4, 3, 1]
    final_permutation = [0 for i in range(4)]
    for i in range(4):
        final_permutation[i] = matrix_S_Box[P4[i] - 1]


    # XOR com L
    final_res = [0 for i in range(4)]
    for i in range(4):
        final_res[i] = str(int(bool(int(L[i])) ^ bool(int(final_permutation[i]))))


    # Retorna o lado esquerdo e direito, respectivamente
    return final_res, R
            
### Função de decriptação do S-DES ###
def decriptition_s_des(key, block):
    K1, K2 = key_generation(key)
    block = list(block)

    # Permutação Inicial
    IP = [2, 6, 3, 1, 4, 8, 5, 7]
    first_permutation = [0 for _ in range(8)]
    for i in range(8):
        first_permutation[i] = block[IP[i] - 1]

    first_permutation = "".join(first_permutation)


    # Divisão do bloco de texto em duas partes
    L0 = list(first_permutation[:4])
    R0 = list(first_permutation[4:])
    L1, R1 = f_function(L0, R0, K2)

    L2, R2 = f_function(L1, R1, K1)
    final_block = L2 + R2

    # Permutação Final    
    IP_1 = [4, 1, 3, 5, 7, 2, 8, 6]
    IP_1_permutation = [0 for i in range(8)]   
    for i in range(8):
        IP_1_permutation[i] = final_block[IP_1[i] - 1]

    IP_1_permutation = "".join(IP_1_permutation)    

    return IP_1_permutation

### Função de encriptação do S-DES ###
def s_des(key, block):
    K1, K2 = key_generation(key)
    block = list(block)

    # Permutação Inicial
    IP = [2, 6, 3, 1, 4, 8, 5, 7]
    first_permutation = [0 for _ in range(8)]
    for i in range(8):
        first_permutation[i] = block[IP[i] - 1]

    first_permutation = "".join(first_permutation)


    # Divisão do bloco de texto em duas partes
    L0 = list(first_permutation[:4])
    R0 = list(first_permutation[4:])
    L1, R1 = f_function(L0, R0, K1)

    L2, R2 = f_function(L1, R1, K2)
    final_block = L2 + R2

    # Permutação Final    
    IP_1 = [4, 1, 3, 5, 7, 2, 8, 6]
    IP_1_permutation = [0 for i in range(8)]   
    for i in range(8):
        IP_1_permutation[i] = final_block[IP_1[i] - 1]

    IP_1_permutation = "".join(IP_1_permutation)    

    return IP_1_permutation

if __name__ == "__main__":
    key = "1010000010"
    block = "11010111"
    ciphered_block = s_des(key, block)
    deciphered_block = decriptition_s_des(key, ciphered_block)

    # Teste de encriptação
    print("### Teste do S-DES ###")
    print("Passou" if ciphered_block == "10010111" else "Falhou")
    print("Resultado: ", ciphered_block)

    # Teste de decriptação
    print("### Teste de decriptação do S-DES ###")
    print("Passou" if deciphered_block == block else "Falhou")
    print("Resultado: ", deciphered_block)