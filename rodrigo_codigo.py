import sys
import copy

class Estado:
    def __init__(self, matriz, vida1, vida2, municao1, municao2):
        self.heuristica =  0
        self.matriz = matriz       
        self.vida1 =  vida1
        self.vida2 =  vida2
        self.municao1 =  municao1
        self.municao2 =  municao2
        #ataque1 , ataque2 , cima , baixo , esq , dir , defesa
        self.ultimaJogada = ''
        self.posicaoVida = self.getPosicaoElemento(4)
        self.posicaoArma = self.getPosicaoElemento(3)

    def getPosicaoElemento(self, elementoBuscar):
        #se elementoBuscar == 4 entao percorre o tabuleiro 5x5 (this.matriz) e retorna a posição que está o numero 4(vida)
        #se elementoBuscar == 4 entao percorre  o tabuleiro 5x5 (this.matriz) e retorna a posição que está o numero 3(arma)
        for i in range(5):
            for j in range(5):
                if (self.matriz[i][j] == elementoBuscar):
                    return [i,j]

def verificaAdversarioPerto(estado):
    pos1 = estado.getPosicaoElemento(1)
    pos2 = estado.getPosicaoElemento(2)

    diferencaLinha = abs(pos1[0] - pos2[0])
    diferencaColuna = abs(pos1[1] - pos2[1])

    if(diferencaLinha >= 1 and diferencaColuna >= 1):
        return True
    return False 

def estadosMovimentacao(jogador, estado):
    movimentosPermitidos = []
    posicao = estado.getPosicaoElemento(jogador)
    linha = posicao[0]
    coluna = posicao[1]
    adversario = 2 if jogador == 1 else 1
    if(linha - 1 >= 0):
        if(estado.matriz[linha-1][coluna] != adversario):
            movimentosPermitidos.append('cima')
    if(linha + 1 <= 4):
        if(estado.matriz[linha + 1][coluna] != adversario):
            movimentosPermitidos.append('baixo')
    if(coluna - 1 >= 0):
        if(estado.matriz[linha][coluna - 1] != adversario):
            movimentosPermitidos.append('esquerda')
    if(coluna + 1  <= 4):
        if(estado.matriz[linha][coluna + 1] != adversario):
            movimentosPermitidos.append('direita')
    return movimentosPermitidos

#gerar estados sucessores
def geraEstadosFilhos(jogador, estado):
    listaEstados = []  
    adversarioPerto = verificaAdversarioPerto(estado)
    #estado onde nos atacamos, ficamos no mesmo lugar
    #apenas muda-se o atributo jogada indicando que foi feito um ataque, indicando ataue 1 ou 2
    #se a ultima jogada feita tiver sido um ataque, verificar dano e diminuir vida
    if(jogador ==1):
        novoEstado = copy.deepcopy(estado)
        #ataque
        if(estado.ultimaJogada == 'ataque1' and adversarioPerto):   
            novoEstado.vida1 = novoEstado.vida1 - 1
        if(estado.ultimaJogada == 'ataque2' and adversarioPerto):
            novoEstado.vida1 = novoEstado.vida1 - 2
        
        if(novoEstado.municao1 > 0):
            novoEstado.ultimaJogada = 'ataque2'
            novoEstado.municao1 = novoEstado.municao1 - 1
        else:
             novoEstado.ultimaJogada = 'ataque1'
        listaEstados.append(novoEstado)
        #ataque

        #defesa
        #estado onde ele defende
        #se a ultima jogada tiver sido um ataque2 entao deve-se diminuir a vida em 1 ponto 
        #muda-se o atributo jogada indicando que ele se defendeu

        novoEstado1 = copy.deepcopy(estado)
        if(estado.ultimaJogada == 'ataque2' and adversarioPerto):
            novoEstado1.vida1 = novoEstado1.vida1 - 1
        novoEstado1.ultimaJogada= 'defesa'
        listaEstados.append(novoEstado1)
        #defesa
    else:
        novoEstado = copy.deepcopy(estado)
        if(estado.ultimaJogada == 'ataque1' and adversarioPerto):
            novoEstado.vida2 = novoEstado.vida2 - 1
        if(estado.ultimaJogada == 'ataque2' and adversarioPerto):
            novoEstado.vida2 = novoEstado.vida2 - 2

        if(novoEstado.municao2 > 0):
            novoEstado.ultimaJogada = 'ataque2'
            novoEstado.municao2 = novoEstado.municao2 - 1
        else:
             novoEstado.ultimaJogada = 'ataque1'
        novoEstado.ultimaJogada= 'ataque'
        listaEstados.append(novoEstado)

        #defesa
        #estado onde ele defende
        #se a ultima jogada tiver sido um ataque2 entao deve-se diminuir a vida em 1 ponto 
        #muda-se o atributo jogada indicando que ele se defendeu

        novoEstado1 = copy.deepcopy(estado)
        if(estado.ultimaJogada == 'ataque2' and adversarioPerto):
            novoEstado1.vida2 = novoEstado1.vida2 - 1
        novoEstado1.ultimaJogada= 'defesa'
        listaEstados.append(novoEstado1)
        #defesa
  
    posicaoJogador = estado.getPosicaoElemento(jogador)
    linha = posicaoJogador[0]
    coluna = posicaoJogador[1]
    vida = getattr(estado, f'vida{jogador}')
    municao = getattr(estado, f'municao{jogador}')

    movimentosPermitidos = estadosMovimentacao(jogador, estado)
    for movimento in movimentosPermitidos:

        if(movimento == 'cima'):
            novoEstado = copy.deepcopy(estado)
            if(novoEstado.matriz[linha-1][coluna] == 3):
                setattr(novoEstado, f'vida{jogador}', 9)
            if(novoEstado.matriz[linha-1][coluna] == 4):
                setattr(novoEstado, f'municao{jogador}', 5)    
            novoEstado.matriz[linha][coluna] = 0
            novoEstado.matriz[linha-1][coluna] = jogador
            novoEstado.ultimaJogada = 'cima'
            listaEstados.append(novoEstado)


        if(movimento == 'baixo'):
            novoEstado = copy.deepcopy(estado)
            if(novoEstado.matriz[linha+1][coluna] == 3):
                setattr(novoEstado, f'vida{jogador}', 9)
            if(novoEstado.matriz[linha+1][coluna] == 4):
                setattr(novoEstado, f'municao{jogador}', 5)    
            novoEstado.matriz[linha][coluna] = 0
            novoEstado.matriz[linha+1][coluna] = jogador
            novoEstado.ultimaJogada = 'baixo'
            listaEstados.append(novoEstado)


        if(movimento == 'esquerda'):
            novoEstado = copy.deepcopy(estado)
            if(novoEstado.matriz[linha][coluna-1] == 3):
                setattr(novoEstado, f'vida{jogador}', 9)
            if(novoEstado.matriz[linha][coluna-1] == 4):
                setattr(novoEstado, f'municao{jogador}', 5)    
            novoEstado.matriz[linha][coluna] = 0
            novoEstado.matriz[linha][coluna-1] = jogador
            novoEstado.ultimaJogada = 'esquerda'
            listaEstados.append(novoEstado)
            


        if(movimento == 'direita'):
            novoEstado = copy.deepcopy(estado)
            if(novoEstado.matriz[linha][coluna+1] == 3):
                setattr(novoEstado, f'vida{jogador}', 9)
            if(novoEstado.matriz[linha][coluna+1] == 4):
                setattr(novoEstado, f'municao{jogador}', 5)    
            novoEstado.matriz[linha][coluna] = 0
            novoEstado.matriz[linha][coluna+1] = jogador
            novoEstado.ultimaJogada = 'direita'
            listaEstados.append(novoEstado)
                       
    return listaEstados

#função avaliação
def avaliacaoEstado(estado):
    dano = 1
    posicaoMax = estado.getPosicaoElemento(1)
    posicaoMin = estado.getPosicaoElemento(2)
    posicaoVida = estado.getPosicaoElemento(4)
    posicaoArma = estado.getPosicaoElemento(3)
    
    #verifica se um dos dois tem a arma
    #(vidaMax+ danoCausado * municao ) - (vidaMin + danoCausado * municao)
    if(estado.municao1 > 0 or estado.municao2 > 0):
        dano = 2
        return ((estado.vida1 + dano * estado.municao1) - (estado.vida2 + dano * estado.municao2))    

    #se a vida nao tiver cheia, verifica a distancia em relação a vida
    if(estado.vida1 < 9 or estado.vida2 < 9):
        distanciaMaxVida = abs(posicaoMax[0] - posicaoVida[0]) + abs(posicaoMax[1] - posicaoVida[1])
        distanciaMinVida = abs(posicaoMin[0] - posicaoVida[0]) + abs(posicaoMin[1] - posicaoVida[1])
        return (- distanciaMaxVida + distanciaMinVida)    
         
    distanciaMaxMin = abs(posicaoMax[0] - posicaoMin[0]) + abs(posicaoMax[1] - posicaoMin[1])
    distanciaMaxArma = abs(posicaoMax[0] - posicaoArma[0]) + abs(posicaoMax[1] - posicaoArma[1])
    distanciaMinArma = abs(posicaoMin[0] - posicaoArma[0]) + abs(posicaoMin[1] - posicaoArma[1])

    return  (-distanciaMaxArma + distanciaMinArma)* (distanciaMaxMin/100)
     
'''A função retorna um vetor com 3 posições, na primeira retornaremos a heuristica quando necessario
na segunda retornaremos o jogador vencedor quando houver e na terceira posição seria retornada a jogada 
que o agente do nó raiz deverá executar'''
def MiniMax(jogador, estado, profundidade):
    if profundidade == 0 or estado.vida1 == 0 or estado.vida2 == 0:
        estado.heuristica = avaliacaoEstado(estado)
        return estado
    
    if(jogador == 1): #jogador 1 MAX
        melhorValor = -100000000000000
        melhorEstado =  None
        estadosFilhos = geraEstadosFilhos(jogador, estado)  
        for estadoFilho in estadosFilhos:    
            estadoRetornado = MiniMax(2, estadoFilho, profundidade-1)
            melhorValor= max(melhorValor, estadoRetornado.heuristica)
            if(estadoRetornado.heuristica == melhorValor):
                melhorEstado = estadoRetornado
        #print(f"melhor valor:{melhorValor}")
        return melhorEstado

    else: #jogador 2 MIN
        melhorValor = 100000000000000
        melhorEstado =  None
        estadosFilhos = geraEstadosFilhos(jogador, estado)
        for estadoFilho in estadosFilhos: 
               
            estadoRetornado = MiniMax(1, estadoFilho, profundidade-1)
            melhorValor = min(melhorValor, estadoRetornado.heuristica)
            #print(f"melhor valor:{melhorValor}")
           # print(f"heuristica: {estadoRetornado.heuristica}")
            if(estadoRetornado.heuristica == melhorValor):
                melhorEstado = estadoRetornado
                #print(f"melhorpara min: {vars(melhorEstado)}")
        #print(f"melhor valor:{melhorValor}")
        return melhorEstado

            
#receber parametros por linha de comando

jogador = sys.argv[1]
estadoTerminal = sys.argv[2]
matriz = [[int(char) for char in estadoTerminal[i:i+5]] for i in range(0, len(estadoTerminal),  5)]
vida1 = sys.argv[3]
vida2 = sys.argv[4]
municao1 = sys.argv[5]
municao2 = sys.argv[6]
novoEstado = Estado(matriz, int(vida1), int(vida2), int(municao1), int(municao2))

retornoMinimax = MiniMax(1, novoEstado, 3)
match retornoMinimax.ultimaJogada:
    case 'ataque1':
        print("attack")
    case 'ataque2':
        print("attack")
    case 'cima':
        print("up")
    case 'esquerda':
        print("left")
    case 'direita':
        print("right")
    case 'baixo':
        print("down")
    case 'defesa':
        print("block")
  


    
