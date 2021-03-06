import os
from random import randint

# Interface
def menu(): 
    menu = '''
|================================================|
|                 JOGO DA VELHA                  |
|================================================|
| 1 - 1 jogador                                  |
| 2 - 2 jogadores                                |
| 0 - Sair                                       |
|================================================|                             
    '''
    print(menu, end="")

def drawTabuleiro(tab):
    tabuleiro = '''
|================================================|
|                                                |
|                 A     B     C                  |
|              +-----+-----+-----+               |
|          1   |  {}  |  {}  |  {}  |               |
|              +-----+-----+-----+               |
|          2   |  {}  |  {}  |  {}  |               |
|              +-----+-----+-----+               |
|          3   |  {}  |  {}  |  {}  |               |
|              +-----+-----+-----+               |
|                                                |
|================================================|
    ''' .format(tab[0][0], tab[0][1], tab[0][2], tab[1][0], tab[1][1], tab[1][2], tab[2][0], tab[2][1], tab[2][2])
    
    print(tabuleiro)

# Gera uma matriz 3x3 
def gerarTabuleiro():
    tabuleiro = [ [' ' for i in range(3)] for j in range(3)]
    return tabuleiro

# Escolhe aleatoriamente a key do jogador
def jogador():
    return 'X' if randint(1, 2) == 1 else 'O'

# Transforma as letras no index correto.  
# Diminui 1 do número, pois a matriz é de 0-3 
def editInput(letra, numero):
    if (letra == "A" or letra == 'a'):
        letra = 0
    elif (letra == "B" or letra == 'b'):
        letra = 1
    elif (letra == "C" or letra == 'c'):
        letra = 2

    x = int(numero) - 1
    y = int(letra)

    return x, y

# Verifica se a posição que o usuário entrou está disponível.
def posicaoDisponivel(matriz, x, y): 
    disponivel = True

    if matriz[x][y] != ' ':
        disponivel = False
        
    return disponivel

# Atribui um X ou O à posição que o usuário jogou.
def jogada(matriz, pos, key):
    if posicaoDisponivel(matriz, pos[0], pos[1]):
        matriz[pos[0]][pos[1]] = str(key)
        return True
    else:
        return False

# Verifica se deu velha, a key é X ou O.
def velha(tabuleiro, key, x, y):
    jogando = True
    dp = 0
    ds = 0
    l1 = 0
    l2 = 0
    l3 = 0
    c1 = 0
    c2 = 0
    c3 = 0

    for i in range(3):
        # # # diagonal principal # # #
        if (tabuleiro[i][i] == key):
            dp += 1
    
        # # # diagonal secundária # # #
        if (tabuleiro[i][3-1-i] == key):
            ds += 1

        # # # linhas # # #
        if (x == 0):
            if (tabuleiro[0][i] == key):
                l1 += 1
        elif (x == 1):
            if (tabuleiro[1][i] == key):
                l2 += 1
        elif (x == 2):
            if (tabuleiro[2][i] == key):
                l3 += 1
    
        # # # colunas # # #
        if (y == 0):
            if (tabuleiro[i][0] == key):
                c1 += 1
        elif (y == 1):
            if (tabuleiro[i][1] == key):
                c2 += 1
        elif (y == 2):
            if (tabuleiro[i][2] == key):
                c3 += 1

    # # # Se o contador for == 3, deu velha # # #
    if (dp == 3 or ds == 3 or l1 == 3 or l2 == 3 or l3 == 3 or c1 == 3 or c2 == 3 or c3 == 3):
        jogando = False
    
    return jogando

# Se a soma for igual a 4 e não tiver ganhado, deu empate
def empate(tabuleiro, key):
    soma = 0
    for i in range(3):
        for j in range(3):
            if (tabuleiro[i][j] == key):
                soma += 1
    return soma

# Jogada do automático, se a posição estiver disponível
# retorna 0, senão retorna 1
# Se vencer, retorna 2
# Se empatar, retorna 3
def automatico(tabuleiro, key, key2):
    valid = ''

    x = randint(0, 2)
    y = randint(0, 2)
    
    if jogada(tabuleiro, (x, y), key):
        if not (velha(tabuleiro, str(key), x, y)):
            print("Automático Venceu!")
            valid = '2'
        elif (empate(tabuleiro, key) == 4 and empate(tabuleiro, key2) == 4):
            print("Empate!")
            valid = '3'
        else:
            valid = '0'
    else:
        valid = '1'
        
    return valid