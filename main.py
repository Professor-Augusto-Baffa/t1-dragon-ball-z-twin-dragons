import auxiliar as aux
from lutas import randomGen, evolucao, simAnnealing, tempoTotal

# Pedro Gonçalves Mannarino - 2210617
# Luiza Marcondes Paes Leme - 2210275


# Fácil alteração dos valores de batalhas e heróis
batalhas = [35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
herois = [1.1, 1.2, 1.3, 1.4, 1.5]

# Escolhemos representar as coordenadas do mapa como [x][y], x sendo linha e y coluna
mapa = aux.lerMapa()

# Carrega a lista de lugares relevantes ao caminho a ser precorrido em ordem
lugares = aux.lerLugares()

# Inicializa uma lista de todos os caminhos entre todos os lugares
caminhos = []

# Inicializa um mapa geral para agregar todos os mapas anteriores a ele, para melhor vizualização
mapaDinamicoFinal = aux.criarMapaDinamico(mapa)

# Inicializa a soma do tempo de cada caminho percorrido
somaTempo = 0

# Para cada lugar que existe -1, para excluir o início
for i in range(len(lugares) - 1):
    # Verifica se o lugar escolhido em lugares.txt existe no mapa
    try:
        # Se sim, delimita o ponto de início e o de fim
        posI, posE = aux.acharPos(mapa, lugares[i], lugares[i + 1])
    except TypeError:
        # Se não, aborta o programa e reclama
        print("Mapa contruído incorretamente.")
        quit()
    
    # Cria um mapa dinâmico local para mostrar a exploração ocorrendo atualmente
    mapaDinamico = aux.criarMapaDinamico(mapa)

    # Instancia a coordenada de início como uma Coord, para começar o algoritmo
    inicio = aux.Coord(posI[0], posI[1], posE, 0, None)
    listaAEstrela = [inicio]

    # Inicializa lista de coords conhecidas pelo algoritmo nessa sessão de exploração
    conhecidos = []

    # Adiciona a coord inicial para a lista de coords conhecidas
    conhecidos.append((posI[0], posI[1]))

    # Desenha o início e o fim no pygame para melhor visualização
    aux.caminharMapaDinamico(mapaDinamico, inicio.x, inicio.y, mapa, aux.screen)
    aux.caminharMapaDinamico(mapaDinamico, posE[0], posE[1], mapa, aux.screen)

    # Enquanto não encontra o final
    while(True):
        # Extrai o primeiro do heap, que é o mais próximo de acordo com o sort que ocorre a toda iteração
        coordAtual = listaAEstrela[0]
        del listaAEstrela[0]
        
        # Se ele chegou em seu destino
        if (coordAtual.heuristica == 0):
            # Adiciona o caminho completo que esse coord teve à lista de caminhos
            caminhos.append(aux.acharCaminho(coordAtual, lugares[i+1]))

            # Expande o mapa final com o mapa local
            aux.agregarMapa(mapaDinamicoFinal, mapaDinamico)

            # Soma o tempo do caminho que acabou de ser criado
            somaTempo += caminhos[i][0]

            # Imprime para acompanhar enquanto explora
            print("Tempo da caminhada até " + lugares[i+1] + ": " + str(somaTempo))
            break
        
        # Avalia quais vizinhos dessa coord podem ser adicionados ao heap
        aux.avaliaVizinhos(mapa, coordAtual, conhecidos)

        # Para cada filho válido a ser adicionado ao heap
        for filho in coordAtual.filhos:
            # Desenha ele no mapa, fazendo com que tudo que o mapa mostre seja tudo que o algoritmo tem conhecimento,
            # e não tudo que ele realmente percorreu
            aux.caminharMapaDinamico(mapaDinamico, filho.x, filho.y, mapa, aux.screen)

        # Adiciona os filhos ao heap
        listaAEstrela.extend(coordAtual.filhos)

        # Ordena o heap considerando o valor percorrido + o valor de sua heurística,
        # garantindo que o primeiro do heap sempre será o mais próximo, ou um dos
        listaAEstrela.sort(key = lambda x : x.percorrido + x.heuristica)

# Determina uma flag para representar uma cor no pygame
flag = 'Z'
# Para cada caminho entre todos os lugares
for caminho in caminhos:
    # Desenha o caminho usando flag como controle para pintar o caminho de 3 cores diferentes
    aux.atualizarMapaDinamico(mapaDinamicoFinal, caminho[2:], flag, aux.screen, caminho[1])
    # Alterna entre 3 flags, ou cores, diferentes
    flag = 'Y' if flag == 'Z' else 'Z' if flag == 'W' else 'W'

# Cálculo do tempo da combinação das lutas
ngens = 1200
indsgen = 100
batalhas.sort()
herois.sort()

geracaoFinal = []

for gens in range(3):
    geracao = randomGen(indsgen, batalhas, herois)
    geracao = evolucao(ngens, indsgen, geracao, batalhas, herois)
    print("Melhor fitness da geracao " + str(gens + 1) + " -> " + str(geracao[0][0]))
    geracao[0] = simAnnealing(geracao[0], batalhas, herois)
    print("Melhor fitness da geracao " + str(gens + 1) + " após sim annealing -> " + str(geracao[0][0]))
    geracaoFinal.extend(geracao[:int(indsgen/3)])

geracaoFinal = evolucao(ngens, indsgen, geracaoFinal, batalhas, herois)
print("Melhor fitness da última geracao -> " + str(geracaoFinal[0][0]))
print("Melhor combinação da última geracao -> " + str(geracaoFinal[0][1]))
print("Melhor tempo da última geração -> " + str(tempoTotal(geracaoFinal[0][1], batalhas, herois)))

melhor = simAnnealing(geracaoFinal[0], batalhas, herois)

print("Melhor fitness da última geracao após sim annealing -> " + str(melhor[0]))
print("Melhor combinação da última geracao após sim annealing -> " + str(melhor[1]))
print("Melhor tempo da última geração após sim annealing -> " + str(tempoTotal(melhor[1], batalhas, herois)))

print("Tempo da caminhada:" + str(somaTempo))

print("TEMPO TOTAL: " + str(somaTempo + tempoTotal(melhor[1], batalhas, herois)))