
# Recebe um estado
# verifica se o estado atual é um estado final (houve vencedor)
# se nao, verifica se a arvore atingiu uma profundidade 
# se sim, calcula a heuristica do estado e retorna
# se nao, gere os estados sucessores para serem percorridos
# chame a rotina recursiva minimax passando o valor atual e o estado sucessor

import copy

def verificaVencedor(matriz):
    
    if sum(sum(linha) for linha in matriz) ==  9:
        return 0 #deu velha, todas posições preenchidas 
    
    for i in range(3):
        if matriz[i][0] == matriz[i][1] == matriz[i][2] !=  0:
            return matriz[i][0]
    
    for i in range(3):
        if matriz[0][i] == matriz[1][i] == matriz[2][i] !=  0:
            return matriz[0][i]
 
    if matriz[0][0] == matriz[1][1] == matriz[2][2] !=  0:
        return matriz[0][0]
    if matriz[0][2] == matriz[1][1] == matriz[2][0] !=  0:
        return matriz[0][2]
   
    return -1

def geraEstadosFilhos(jogador, matriz):
    listaEstados =[]
    for i in range(3):
        for j in range(3):
            if (matriz[i][j]==0):
                copiaMatriz = copy.deepcopy(matriz)
                copiaMatriz[i][j]=jogador
                listaEstados.append(copiaMatriz)
    return listaEstados
                
def calculaHeuristica(estado):
    heuristica = 2#mudar
    return heuristica

#o retorno será um vetor de 2 posições onde na primeira posição informamos se houve um vencedor, então na primeira posição terá 1 ou 2 
#se houve vencedor e retorna 0 se ainda não ouve
#o valor retornado pela heuristica = h e que sera comparado na função max(v,h) sempre será o valor da posição 2 do vetor
def MiniMax(jogador, estado, profundidade):
    houveVencedor = verificaVencedor(estado)
    if(houveVencedor == 0):
        return [0,0,0,0] #deu velha
    if(houveVencedor != 0 and houveVencedor != -1):
        return houveVencedor
    if(profundidade == 0):
        h = calculaHeuristica(estado)
        return [h,0,]
    
    if(jogador == 1):#max
        estadosFilhos = geraEstadosFilhos(1, estado)
        for estado in estadosFilhos:
            valorAtual = max(valorAtual, MiniMax(2, estado, profundidade-1))
    
# matriza = [[9,  2,  0], [9,  0,  2], [9,  2,  0]]
# vencedor = avaliaEstado(matriza)
# if vencedor is not None:
#     print(f"Jogador {vencedor} venceu!")
# else:
#     print("Sem vencedor.")
