import socket
import sys
import json
import time
import threading
from random import randint
from tabuleiro import gerarTabuleiro, editInput, jogador, jogada, automatico

clientes = []

host = socket.gethostname()
port = 10100

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(10)

def sendTabuleiro(tabuleiro, client):
    tab = json.dumps(tabuleiro)
    client.send(tab.encode())

def recvPosicao(client, tabuleiro, key):
    pos = client.recv(5000).decode().split(' ', 1)
    x, y = editInput(pos[0], pos[1])
    print(x, y)

    # Se for 0 a posição é válida
    if not (jogada(tabuleiro, (x, y), key)):
        return '1'
    else:
        return '0'

def recebeOpcao(client):
    try:
        while True:
            op = client.recv(1024).decode()
            print(type(op), op)
            if op == '1':
                print("Jogar no automatico")
                jogando = False
                play = ''

                # Gera o tabuleiro
                tabuleiro = gerarTabuleiro()

                # Gera o X ou O
                key = jogador()
                keyAut ='O' if key == 'X' else 'X'
                print(keyAut)

                # Decide quem vai começar o jogo
                vez = randint(1, 2)
                if vez == 1: # O cliente começa
                    vezAut = 2
                    client.send((str(vez) + " " + key).encode())
                    jogando = True
                    play = '0'
                else: # Servidor começa e avisa pro cliente que o servidor vai começar
                    vezAut = 1
                    client.send((str(vez) + " " + key).encode())
                    validAut = automatico(tabuleiro, keyAut)
                    if (validAut == '0'):
                        jogando = True
                        play = '0'
                        time.sleep(0.3)
        
                # time.sleep(0.3)
                while jogando:
                    if (play == '0'):
                        sendTabuleiro(tabuleiro, client)
                        valid = recvPosicao(client, tabuleiro, key)
                        client.send(valid.encode())
                        play = '1'
                        if (valid == '0'):
                            print("posição válida!")
                            validAut = automatico(tabuleiro, 'X')
                            if (validAut == '0'):
                                print(validAut)
                                play = '0'
                        else:
                            print("posição inválida!")

            elif op == '2':
                print("cadastro")
            elif op == '0':
                print("Encerrando!")
                client.close()
                sys.exit()
            else:
                print(" \nOpção inválida! Tente novamente.")
    except ConnectionResetError as erro:
        print(erro)

while True:
    try:
        client, addr = serversocket.accept()
        print("conexão aceita")
        clientes.append(client)
        threading.Thread(target=recebeOpcao, args=(client,)).start()
    except KeyboardInterrupt as erro:
        print(erro)