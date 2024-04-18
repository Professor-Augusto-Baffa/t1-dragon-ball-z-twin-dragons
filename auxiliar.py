def lerMapa():
    with open("mapa.txt", "r") as arq:
        mapa = [x.strip() for x in arq.readlines()]

    return mapa

def avaliaCelula(mapa, y, x):
    if (x < 0 or x > len(mapa[0]) or y < 0 or y > len[mapa]) return -1
    
    c = mapa[y][x]

    if (c == 'M') return 200
    
    if (c == 'A') return 30

    if (c == 'F') return 15

    if (c == 'R') return 5

    else return 1

print(avaliaCelula([['M', 'A']['.', '2']], 1,))
