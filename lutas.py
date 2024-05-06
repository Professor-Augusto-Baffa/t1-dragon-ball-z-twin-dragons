import random

# Pedro Gonçalves Mannarino - 2210617
# Luiza Marcondes Paes Leme - 2210275

# Função que calcula e retorna o tempo total a partir de uma combinação após todas as lutas
def tempoTotal(ind, batalhas, herois):
    
    tempo = 0

    # Percorre por batalha
    for batalha in batalhas:
        
        soma = 0
        for n in range(len(herois)):
            # Verifica se a batalha está na lista do herói, ou seja, se ele participa da batalha
            if (batalha in ind[n]):
                # Soma o poder do herói
                soma += herois[n]
        # Adiciona ao tempo total o tempo da batalha dividido pela soma dos poderes dos heróis que participam dela
        tempo += batalha/soma
    
    return tempo

# Função que calcula e retorna o fitness de uma combinação
def fitness(ind, batalhas, herois):

    # O valor é calculado com a diferença entre o tempo total e o tempo total da combinação
    # Um tempo total menor irá resultar em uma diferença maior, e portanto, um valor maior
    # O valor é usado como expoente para que uma pequena diferença no tempo resulte em uma grande diferença no fitness
    valor = 1.4 ** (sum(batalhas) - tempoTotal(ind, batalhas, herois))

    # Se por acaso a combinação respeita a regra de cada batalha ter um soma de poderes maior ou igual a anterior, o fitness é multiplicado por 10
    # Isso é favorável, pois analiticamente é mais provável que uma combinação que respeita essa regra seja melhor
    # Entretanto, não é necessário que a combinação respeite isso para ser útil para evolução
    if (not verificaAnt(ind, batalhas, herois)):
        return valor
    return valor * 10

# Função auxiliar que copia uma lista de listas
def copiaListaDeListas(lista):
    nova = []
    for l in lista:
        nova.append(l.copy())
    return nova

# Função que verifica se a combinação respeita a regra de cada batalha ter um soma de poderes maior ou igual a anterior
def verificaAnt(ind, batalhas, herois):

    somaant = 0

    for batalha in batalhas: 

        soma = 0
        for n in range(len(herois)):
            # Verifica se a batalha está na lista do herói, ou seja, se ele participa da batalha
            if (batalha in ind[n]):
                # Soma o poder do herói
                soma += herois[n]

        if (soma < somaant):
            # Se a soma de poderes for menor que a anterior, a regra não é respeitada
            return False
        
        # Atualiza a soma anterior
        somaant = soma

    # Se passar por todas as batalhas sem retornar False, a regra é respeitada
    return True

# Função que executa o algoritmo de Simulated Annealing
def simAnnealing(melhor, batalhas, herois):

    # Cópias da melhor combinação (por enquanto a inicial)
    # MelhorAnt serve para evitar estagnação
    melhorAnt = [melhor[0]]
    melhorAnt.append(copiaListaDeListas(melhor[1]))

    # MelhorTotal serve para guardar a melhor combinação encontrada mesmo se o algoritmo for por um caminho pior
    melhorTotal = [melhor[0]]
    melhorTotal.append(copiaListaDeListas(melhor[1])) 

    # Loop de 5500 tentativas 
    for n in range(5500):

        # Executa uma mutação na melhor combinação
        mutado = mutacao(copiaListaDeListas(melhor[1]), batalhas)
        
        # 40% de chance de executar mais mutações
        # Isso é necessário, pois pode ser que mais de uma mutação seja necessária para melhorar a combinação
        if (random.random() < 0.4):

            # Número de mutações aleatório entre 1 e 7
            num = random.randint(1, 7)

            for i in range(num):
                # Executa a mutação
                mutado = mutacao(copiaListaDeListas(mutado), batalhas)

        # A cada 25 tentativas, verificar estagnação
        if (n % 25 == 0):

            # Se está a mais de 25 tentativas sem melhora
            if (melhor == melhorAnt):

                # Assume derrota e aceita a combinação atual como melhor para progredir dela
                melhor[1] = copiaListaDeListas(mutado)
                melhor[0] = fitness(melhor[1], batalhas, herois)

                # Se a combinação atual é melhor que a melhor encontrada até agora, atualiza
                if (melhor[0] > melhorTotal[0]):
                    melhorTotal = [melhor[0]]
                    melhorTotal.append(copiaListaDeListas(melhor[1])) 

                # Atualiza a combinação anterior
                melhorAnt = [melhor[0]]
                melhorAnt.append(copiaListaDeListas(melhor[1]))

        # Se a combinação mutada é melhor que a melhor encontrada até agora, atualiza
        if (fitness(mutado, batalhas, herois) > melhor[0]):
            melhor[1] = copiaListaDeListas(mutado)
            melhor[0] = fitness(melhor[1], batalhas, herois)
    
    # Se a melhor combinação encontrada pelo Simulated Annealing é pior que a melhor de todas encontrada até agora, retorna a melhor de todas
    if (melhorTotal[0] > melhor[0]):
        return melhorTotal
    # Se não, retorna a melhor atual que superou a melhor de todas anteriormente armazenada
    return melhor


# Função que gera uma geração aleatória de qtd indivíduos
def randomGen(qtd, batalhas, herois):
    
    geracao = []

    # Geração aleatória
    for n in range(qtd):

        # Cria uma verificação com todas as batalhas para garantir que cada batalha está com pelo menos um herói
        verificacao = batalhas.copy()

        # Enquanto a verificação não tiver vazia, ou seja, enquanto ao menos uma batalha não tiver um herói, gera uma combinação aleatória
        while(verificacao != set()):

            ind = []
            # Reinicia a verificação
            verificacao = batalhas.copy()

            # Gera uma combinação aleatória de 4 batalhas para o primeiro herói	
            # Isso assume que o primeiro é o mais fraco e portanto é mais útil que ele seja o que sobra no final
            ind.append(random.sample(batalhas, 4))

            # Atualiza a verificação com as batalhas que ainda não tem herói
            verificacao = set(verificacao) - set(ind[0])
            
            # Para os outros heróis, faz o mesmo com 5 batalhas
            for i in range(len(herois) - 1):
                ind.append(random.sample(batalhas, 5))
                verificacao = set(verificacao) - set(ind[i+1])

        # Adiciona a combinação à geração se passar da verificação
        geracao.append([fitness(ind, batalhas, herois), ind])
    
    return geracao

# Função que executa uma mutação em uma combinação
def mutacao(ind, batalhas):

    while(True):

        # Escolhe dois heróis aleatórios
        h1 = random.choice(ind)
        b1 = random.choice(h1)
        h2 = random.choice(ind)

        # Se a batalha aleatoriamente selecionada do herói 1 não estiver na lista do herói 2
        if (b1 not in h2):

            # Escolhe uma batalha aleatória do herói 2
            b2 = random.choice(h2)

            # Se a batalha aleatoriamente selecionada do herói 2 não estiver na lista do herói 1
            if (b2 not in h1):

                # Troca as batalhas de lugar
                h1[h1.index(b1)] = b2
                h2[h2.index(b2)] = b1
                break
    
    return ind

# Função que executa a evolução de uma população
def evolucao(ngens, indsgen, geracao, batalhas, herois):

    # Ordena a geração pela fitness
    sortedgeracao = sorted(geracao, key = lambda x: x[0], reverse = True)
    # Guarda a melhor combinação
    melhor = sortedgeracao[0].copy()

    # Loop que evolui a população pela quantidade de gerações passada de parâmetro
    for gen in range(ngens):
        
        # Ordena a geração pela fitness
        sortedgeracao = sorted(geracao, key = lambda x: x[0], reverse = True)

        # Soma total das fitness
        total = 0
        for el in sortedgeracao:
            total += el[0]

        # Calcula a probabilidade de cada indivíduo ser escolhido a partir da proporção de sua fitness em relação ao total
        prob = []
        for el in sortedgeracao:
            prob.append(el[0]/total)

        novaGeracao = []

        # Se a melhor combinação da geração atual é melhor que a melhor encontrada até agora, atualiza
        if (sortedgeracao[0][0] > melhor[0]):
            melhor = sortedgeracao[0].copy()

        # Adiciona a melhor combinação a cada 50 gerações para evitar regressão
        # Inclusive adiciona na última para garantir que a melhor combinação não seja perdida no resultado retornado
        if ((gen + 1) % 50 == 0):
            novaGeracao.append(melhor)

        # Gera 92% da nova geração a partir de cruzamentos
        for n in range(int(indsgen*0.92)):

            # Escolhe dois pais aleatórios a partir da probabilidade
            pai = random.choices(sortedgeracao, prob)[0][1]
            mae = random.choices(sortedgeracao, prob)[0][1]

            # Cria uma verificação com todas as batalhas para garantir que cada batalha está com pelo menos um herói
            # Isso é necessário para evitar que uma batalha fique sem herói após o cruzamento
            verificacao = batalhas.copy()

            while(verificacao != set()):
                filho = []
                
                verificacao = batalhas.copy()

                # Cria um filho a partir da combinação de genes (lista de batalhas de cada herói) dos pais
                for i in range(len(pai)):

                    # Probabilidade de 50% de herdar do pai ou da mãe
                    if (random.random() < 0.5):
                        filho.append(pai[i].copy())
                    else:
                        filho.append(mae[i].copy())
                    verificacao = set(verificacao) - set(filho[i])

                # 10% de chance de mutação
                if (random.random() < 0.1):
                    filho = mutacao(filho, batalhas)
            
            # Adiciona o filho à nova geração
            novaGeracao.append([fitness(filho, batalhas, herois), filho])

        # Gera 8% da nova geração aleatoriamente    
        novaGeracao.extend(randomGen(int(indsgen*0.08), batalhas, herois))

        # Atualiza a geração
        geracao = novaGeracao

    # Retorna a geração ordenada pela fitness
    return sorted(geracao, key = lambda x: x[0], reverse = True)
