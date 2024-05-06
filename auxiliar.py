import os
import pygame

# Pedro Gonçalves Mannarino - 2210617
# Luiza Marcondes Paes Leme - 2210275

# Classe de coordenada do mapa, armazenando todas as informações relevantes
class Coord():
    def __init__(self, x, y, posE, percorrido, pai):
        # Coordenadas x = linha, y = coluna
        self.x = x
        self.y = y
        # Coordenadas x,y do destino do caminho atual
        self.posE = posE
        # Quantidade de unidades de tempo gasto no caminho percorrido até esse momento
        self.percorrido = percorrido
        # Valor da heurística
        self.heuristica = heuristica(x, y, posE)
        # Referência ao pai para fazer traceback
        self.pai = pai
        # Todos os outros Coords revelados, adjacentes a ele e não antes conhecidos
        self.filhos = []

# Função que lê a informação de mapa.txt e converte em uma matriz
def lerMapa():
    with open("mapa.txt", "r") as arq:
        # O x.strip() serve para remover o \n de todas as linhas de readlines(),
        # e o [] efetivamente cria uma matriz com todas as listas (linhas)
        mapa = [x.strip() for x in arq.readlines()]

    return mapa

# Função que revela todos os tiles desconhecidos do mapaAntigo com os tiles do mapaNovo
def agregarMapa(mapaAntigo, mapaNovo):
    x = 0
    for linha in mapaNovo:
        y = 0
        for char in linha:
            if (mapaAntigo[x][y] == "?"):
                mapaAntigo[x][y] = mapaNovo[x][y]
            y += 1
        
        x += 1

# Função que cria um novo mapa desconhecido que pode ser facilmente modificado por ser composto por chars
def criarMapaDinamico(mapa):
    mapaDinamico = []
    cont = 0
    
    for linha in mapa:
        mapaDinamico.append([])
        
        for coluna in linha:
            mapaDinamico[cont].append("?") 

        cont += 1

    return mapaDinamico

# Função que desenha um caminho dado em um mapaDinamico e no pygame
def atualizarMapaDinamico(mapaDinamico, caminho, c , screen, destino):
    for coord in caminho:
        mapaDinamico[coord[0]][coord[1]] = c
        print("Distância percorrida no caminho até " + destino + ": " + str(coord[2]))
        # Mostrar o mapa atualizando na interface gráfica
        # COMENTAR PARA NÃO IMPRIMIR CAMINHOS:
        imprimirMapa(mapaDinamico, screen)
        

# Função que da um passo no mapa dinâmico, somente para revelá-lo, e atualiza a tela
def caminharMapaDinamico(mapaDinamico, x, y, mapa, screen):
    # Revela aquela posição do mapa dinâmico
    mapaDinamico[x][y] = mapa[x][y]
    
    # Mostrar o mapa atualizando na interface gráfica
    # COMENTAR PARA NÃO IMPRIMIR PASSO A PASSO DA EXPLORAÇÃO:
    imprimirMapa(mapaDinamico, screen)

# Função que lê arquivo lugares.txt para pegar os caracteres que representam a sequência dos lugares a serem percorridos
def lerLugares():
    with open("lugares.txt", "r") as arq:
        lugares = [x for x in arq.readline()]

    return lugares

# Função que encontra as coordenadas x,y para um ponto I e E, início e fim
def acharPos(mapa, cI, cE):
    I = None
    E = None

    x = 0
    for linha in mapa:
        y = 0
        
        for coluna in linha:
            if (mapa[x][y] == cI):
                I = (x, y)
                if (E != None):
                    return I, E
                
            if (mapa[x][y] == cE):
                E = (x, y)
                if (I != None):
                    return I, E
                
            y += 1
        x += 1
        
    return None

# Função que calcula a heurítica, efetivamente determinando um caminho ideal a ser escolhido
# enquanto ele caminha pelo mapa, pois somente pode-se mover cardinalmente
def heuristica(x, y, posE):
    return abs(x - posE[0]) + abs(y - posE[1])

# Função que valida se uma célula selecionada pertence ao mapa
def validaCelula(mapa, x, y):
    if (x < 0 or x >= len(mapa) or y < 0 or y >= len(mapa[0])):
        return False
    
    return True

# Função que avalia quanto tempo uma célula demora para ser caminhada
def avaliaCelula(mapa, x, y):
    c = mapa[x][y]

    if (c == 'M'):
        return 200
    
    if (c == 'A'):
        return 30

    if (c == 'F'):
        return 15

    if (c == 'R'):
        return 5

    return 1

# Função que observa e avalia todos os vizinhos de uma célula
def avaliaVizinhos(mapa, pai, conhecidos):
    avaliaVizinho(mapa, pai, conhecidos, pai.x + 1, pai.y)
    avaliaVizinho(mapa, pai, conhecidos, pai.x - 1, pai.y)
    avaliaVizinho(mapa, pai, conhecidos, pai.x, pai.y + 1)
    avaliaVizinho(mapa, pai, conhecidos, pai.x, pai.y - 1)

# Função que avalia se um vizinho já foi percorido e se é válido antes de adicioná-lo como filho de uma outra célula
def avaliaVizinho(mapa, pai, conhecidos, x, y):
    if ((x, y) not in conhecidos and validaCelula(mapa, x, y)):
        pai.filhos.append(Coord(x, y, pai.posE, pai.percorrido + avaliaCelula(mapa, x, y), pai))
        conhecidos.append((x, y))


# Função que encontra o caminho percorrido por uma célula através do traceback pelo seu pai
def acharCaminho(coord, c):
    lista = [(coord.x, coord.y, coord.percorrido)]
    percorrido = coord.percorrido

    while (coord.pai != None):
        coord = coord.pai
        lista.insert(0, (coord.x, coord.y, coord.percorrido))
    lista.insert(0, c)
    lista.insert(0, percorrido)

    return lista
        
# Inicializa pygame, sua tela, e seu clock
pygame.init()
screen = pygame.display.set_mode((1200, 342))
clock = pygame.time.Clock()

# Determina tamanho de cada célula do mapa
tile_width = 6
tile_height = 6

# Define os tipos diferentes de tiles e suas cores no pygame
tileX = pygame.Surface((tile_width, tile_height))
tileM = pygame.Surface((tile_width, tile_height))
tileA = pygame.Surface((tile_width, tile_height))
tileF = pygame.Surface((tile_width, tile_height))
tileR = pygame.Surface((tile_width, tile_height))
tilePonto = pygame.Surface((tile_width, tile_height))
tileElse = pygame.Surface((tile_width, tile_height))
tileVermelho = pygame.Surface((tile_width, tile_height))
tileRosa = pygame.Surface((tile_width, tile_height))
tileLaranja = pygame.Surface((tile_width, tile_height))
tileX.fill((0, 0, 0))
tileM.fill((128, 64, 0))
tileA.fill((0, 191, 255))
tileF.fill((20, 82, 20))
tileR.fill((174, 174, 163))
tilePonto.fill((140, 255, 102))
tileElse.fill((255, 255, 0))
tileVermelho.fill((255, 0, 0))
tileRosa.fill((255, 128, 213))
tileLaranja.fill((255, 153, 0))

# Função exclusiva do pygame para desenhar o mapa usando as cores determinadas anteriormente
def imprimirMapa(mapa, screen):
    screen.fill((0, 0, 0))

    for x in range(len(mapa)):
        for y in range(len(mapa[0])):
            if (mapa[x][y] == "?"):
                screen.blit(tileX, (y * tile_width, x * tile_height))
            elif (mapa[x][y] == "M"):
                screen.blit(tileM, (y * tile_width, x * tile_height))
            elif (mapa[x][y] == "A"):
                screen.blit(tileA, (y * tile_width, x * tile_height))
            elif (mapa[x][y] == "F"):
                screen.blit(tileF, (y * tile_width, x * tile_height))
            elif (mapa[x][y] == "R"):
                screen.blit(tileR, (y * tile_width, x * tile_height))
            elif (mapa[x][y] == "."):
                screen.blit(tilePonto, (y * tile_width, x * tile_height))
            elif (mapa[x][y] == "Z"):
                screen.blit(tileVermelho, (y * tile_width, x * tile_height))
            elif (mapa[x][y] == "Y"):
                screen.blit(tileRosa, (y * tile_width, x * tile_height))
            elif (mapa[x][y] == "W"):
                screen.blit(tileLaranja, (y * tile_width, x * tile_height))
            else:
                screen.blit(tileElse, (y * tile_width, x * tile_height))
    
    # Atualiza a tela a cada frame de desenho
    pygame.display.flip()
    # Função interna para impedir com que a tela congele durante a renderização assíncrona
    pygame.event.pump()
    # Limita o FPS para 60
    clock.tick(60)