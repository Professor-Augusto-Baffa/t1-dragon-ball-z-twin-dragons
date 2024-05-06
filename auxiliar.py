import os
import pygame

# Pedro Gonçalves Mannarino - 2210617
# Luiza Marcondes Paes Leme - 2210275

class Coord():
    def __init__(self, x, y, posE, percorrido, pai):
        self.x = x
        self.y = y
        self.posE = posE
        self.percorrido = percorrido
        self.heuristica = heuristica(x, y, posE)
        self.pai = pai
        self.filhos = []

    def print(self):
        print((self.x, self.y, self.posE, self.percorrido, self.heuristica, self.pai, self.filhos))


def lerMapa():
    with open("mapa.txt", "r") as arq:
        mapa = [x.strip() for x in arq.readlines()]

    return mapa


def agregarMapa(mapaAntigo, mapaNovo):
    x = 0
    for linha in mapaNovo:
        y = 0
        for char in linha:
            if (mapaAntigo[x][y] == "?"):
                mapaAntigo[x][y] = mapaNovo[x][y]
            y += 1
        
        x += 1

def criarMapaDinamico(mapa):
    mapaDinamico = []
    cont = 0
    
    for linha in mapa:
        mapaDinamico.append([])
        
        for coluna in linha:
            mapaDinamico[cont].append("?") 

        cont += 1

    return mapaDinamico


def atualizarMapaDinamico(mapaDinamico, caminho, c , screen):
    for coord in caminho:
        mapaDinamico[coord[0]][coord[1]] = c
        imprimirMapa(mapaDinamico, screen)
        


def caminharMapaDinamico(mapaDinamico, x, y, mapa, screen):
    mapaDinamico[x][y] = mapa[x][y]
    imprimirMapa(mapaDinamico, screen)


def concatenarMapaDinamico(mapaDinamico):
    cont = 0
    for linha in mapaDinamico:
        mapaDinamico[cont] = ''.join(linha)
        cont += 1


def lerLugares():
    with open("lugares.txt", "r") as arq:
        lugares = [x for x in arq.readline()]

    return lugares


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


def heuristica(x, y, posE):
    return abs(x - posE[0]) + abs(y - posE[1])


def validaCelula(mapa, x, y):
    if (x < 0 or x >= len(mapa) or y < 0 or y >= len(mapa[0])):
        return False
    
    return True


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


def avaliaVizinhos(mapa, pai, conhecidos):
    if ((pai.x + 1, pai.y) not in conhecidos and validaCelula(mapa, pai.x + 1, pai.y)):
        pai.filhos.append(Coord(pai.x + 1, pai.y, pai.posE, pai.percorrido + avaliaCelula(mapa, pai.x + 1, pai.y), pai))
        conhecidos.append((pai.x + 1, pai.y))

    if ((pai.x - 1, pai.y) not in conhecidos and validaCelula(mapa, pai.x - 1, pai.y)):
        pai.filhos.append(Coord(pai.x - 1, pai.y, pai.posE, pai.percorrido + avaliaCelula(mapa, pai.x - 1, pai.y), pai))
        conhecidos.append((pai.x - 1, pai.y))

    if ((pai.x, pai.y + 1) not in conhecidos and validaCelula(mapa, pai.x, pai.y + 1)):
        pai.filhos.append(Coord(pai.x, pai.y + 1, pai.posE, pai.percorrido + avaliaCelula(mapa, pai.x, pai.y + 1), pai))
        conhecidos.append((pai.x, pai.y + 1))

    if ((pai.x, pai.y - 1) not in conhecidos and validaCelula(mapa, pai.x, pai.y - 1)):
        pai.filhos.append(Coord(pai.x, pai.y - 1, pai.posE, pai.percorrido + avaliaCelula(mapa, pai.x, pai.y - 1), pai))
        conhecidos.append((pai.x, pai.y - 1))


def acharCaminho(coord, c):
    lista = [(coord.x, coord.y)]
    percorrido = coord.percorrido

    while (coord.pai != None):
        coord = coord.pai
        lista.insert(0, (coord.x, coord.y, coord.percorrido))
    lista.insert(0, c)
    lista.insert(0, percorrido)

    return lista
        

pygame.init()
screen = pygame.display.set_mode((1200, 342))
clock = pygame.time.Clock()

tile_width = 6
tile_height = 6

tileX = pygame.Surface((tile_width, tile_height))
tileM = pygame.Surface((tile_width, tile_height))
tileA = pygame.Surface((tile_width, tile_height))
tileF = pygame.Surface((tile_width, tile_height))
tileR = pygame.Surface((tile_width, tile_height))
tilePonto = pygame.Surface((tile_width, tile_height))
tileX.fill((0, 0, 0))
tileM.fill((128, 64, 0))
tileA.fill((0, 191, 255))
tileF.fill((20, 82, 20))
tileR.fill((174, 174, 163))
tilePonto.fill((140, 255, 102))

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
            else:
                screen.blit(tilePonto, (y * tile_width, x * tile_height))
    
    pygame.display.flip()
    pygame.event.pump()
    clock.tick(60)