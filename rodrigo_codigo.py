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
        for i in range(5):
            for j in range(5):
                if (self.matriz[i][j] == elementoBuscar):
                    return [i,j]
        return [-1,-1]

def verificaAdversarioPerto(estado):
    posMax = estado.getPosicaoElemento(1)
    posMin = estado.getPosicaoElemento(2)

    diferencaLinha = abs(posMax[0] - posMin[0])
    diferencaColuna = abs(posMax[1] - posMin[1])

    if(diferencaLinha >= 1 and diferencaColuna >= 1):
        return True
    return False 

def estadosMovimentacao(jogador, estado):
    listaMovimentosEstados = []
    posicao = estado.getPosicaoElemento(jogador)
    linha = posicao[0]
    coluna = posicao[1]
    adversario = 2 if jogador == 1 else 1
    novoEstado = None

    #Verifica se é possível se mover para cima
    if(linha - 1 >= 0):
        if(estado.matriz[linha-1][coluna] != adversario):
            novoEstado = copy.deepcopy(estado)
            if(novoEstado.matriz[linha-1][coluna] == 3):
                setattr(novoEstado, f'vida{jogador}', 9)
            if(novoEstado.matriz[linha-1][coluna] == 4):
                setattr(novoEstado, f'municao{jogador}', 5)    
            novoEstado.matriz[linha][coluna] = 0
            novoEstado.matriz[linha-1][coluna] = jogador
            novoEstado.ultimaJogada = 'cima'
            listaMovimentosEstados.append(novoEstado)

    #Verifica se é possível se mover para baixo
    if(linha + 1 <= 4):
        if(estado.matriz[linha + 1][coluna] != adversario):
            novoEstado = copy.deepcopy(estado)
            if(novoEstado.matriz[linha + 1][coluna] == 3):
                setattr(novoEstado, f'vida{jogador}', 9)
            if(novoEstado.matriz[linha + 1][coluna] == 4):
                setattr(novoEstado, f'municao{jogador}', 5)    
            novoEstado.matriz[linha][coluna] = 0
            novoEstado.matriz[linha+1][coluna] = jogador
            novoEstado.ultimaJogada = 'baixo'
            listaMovimentosEstados.append(novoEstado)

    #Verifica se é possível se mover para esquerda
    if(coluna - 1 >= 0):
        if(estado.matriz[linha][coluna - 1] != adversario):
            novoEstado = copy.deepcopy(estado)
            if(novoEstado.matriz[linha][coluna-1] == 3):
                setattr(novoEstado, f'vida{jogador}', 9)
            if(novoEstado.matriz[linha][coluna-1] == 4):
                setattr(novoEstado, f'municao{jogador}', 5)    
            novoEstado.matriz[linha][coluna] = 0
            novoEstado.matriz[linha][coluna-1] = jogador
            novoEstado.ultimaJogada = 'esquerda'
            listaMovimentosEstados.append(novoEstado)

    #Verifica se é possível se mover para direita
    if(coluna + 1  <= 4):
        if(estado.matriz[linha][coluna + 1] != adversario):
            novoEstado = copy.deepcopy(estado)
            if(novoEstado.matriz[linha][coluna+1] == 3):
                setattr(novoEstado, f'vida{jogador}', 9)
            if(novoEstado.matriz[linha][coluna+1] == 4):
                setattr(novoEstado, f'municao{jogador}', 5)    
            novoEstado.matriz[linha][coluna] = 0
            novoEstado.matriz[linha][coluna + 1] = jogador
            novoEstado.ultimaJogada = 'direita'
            listaMovimentosEstados.append(novoEstado)
            
    return listaMovimentosEstados

def geraEstadosFilhos(jogador, estado):
    listaEstados = []  
    adversarioPerto = verificaAdversarioPerto(estado)

    if(jogador ==1):# gera estado de ataque e defesa para MAX (1)
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

        #defesa
        novoEstado1 = copy.deepcopy(estado)
        if(estado.ultimaJogada == 'ataque2' and adversarioPerto):
            novoEstado1.vida1 = novoEstado1.vida1 - 1
        novoEstado1.ultimaJogada= 'defesa'
        listaEstados.append(novoEstado1)
    else:# gera estado de ataque e defesa para MIN (2)
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
        novoEstado1 = copy.deepcopy(estado)
        if(estado.ultimaJogada == 'ataque2' and adversarioPerto):
            novoEstado1.vida2 = novoEstado1.vida2 - 1
        novoEstado1.ultimaJogada= 'defesa'
        listaEstados.append(novoEstado1)
  
    #gera estados referentes a movimentações possíveis no tabuleiro
    movimentosPermitidos = estadosMovimentacao(jogador, estado)
    for estadoMovimento in movimentosPermitidos:
        listaEstados.append(estadoMovimento)
       
    return listaEstados

def avaliacaoEstado(estado):
    dano = 1
    posicaoMax = estado.getPosicaoElemento(1)
    posicaoMin = estado.getPosicaoElemento(2)
    posicaoVida = estado.getPosicaoElemento(4)
    posicaoArma = estado.getPosicaoElemento(3)

    dano = 1
    if(estado.municao1 > 0 or estado.municao2 > 0):
        dano = 2
        heuristica = ((estado.vida1 + dano * estado.municao1) - (estado.vida2 + dano * estado.municao2))
        return heuristica

    if(estado.vida1 < 9 or estado.vida2 < 9):
        if(posicaoVida[0] > -1):
            distanciaMaxVida = abs(posicaoMax[0] - posicaoVida[0]) + abs(posicaoMax[1] - posicaoVida[1])
            distanciaMinVida = abs(posicaoMin[0] - posicaoVida[0]) + abs(posicaoMin[1] - posicaoVida[1])
            return (- distanciaMaxVida + distanciaMinVida)    

    if(posicaoArma[0] > -1):
        distanciaMaxMin = abs(posicaoMax[0] - posicaoMin[0]) + abs(posicaoMax[1] - posicaoMin[1])
        distanciaMaxArma = abs(posicaoMax[0] - posicaoArma[0]) + abs(posicaoMax[1] - posicaoArma[1])
        distanciaMinArma = abs(posicaoMin[0] - posicaoArma[0]) + abs(posicaoMin[1] - posicaoArma[1])

        heuristica =   (-distanciaMaxArma + distanciaMinArma)* (distanciaMaxMin/100)
        return heuristica
     
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
        return melhorEstado

    else: #jogador 2 MIN
        melhorValor = 100000000000000
        melhorEstado =  None
        estadosFilhos = geraEstadosFilhos(jogador, estado)
        for estadoFilho in estadosFilhos:        
            estadoRetornado = MiniMax(1, estadoFilho, profundidade-1)
            melhorValor = min(melhorValor, estadoRetornado.heuristica)
            if(estadoRetornado.heuristica == melhorValor):
                melhorEstado = estadoRetornado
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

retornoMinimax = MiniMax(1, novoEstado, 2)
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
  


    
