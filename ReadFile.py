from Grammar import Grammar
def read_from_file(input):
    start = None
    V = set()
    T = set()
    P = dict()
    prodArray = []
    with open('{}'.format(input)) as f:
        line = f.readline().strip().split(' ')
        V = set(line)
        start = line[0]
        line = f.readline().strip().split(' ')
        T = set(line)
        line = f.readline().strip()
        while line != "":
            i = 0
            j = 1
            tokens = []
            last = len(line) + 1
            while j != last:
                sub = line[i: j]
                if sub == " ":
                    i += 1
                    j += 1
                    continue

                if sub in V or sub in T:
                    while sub in V or sub in T:
                        j += 1
                        sub = line[i: j]
                        if j == last: break
                    j -= 1
                    tokens.append(line[i:j])
                    i = j
                    j = i + 1
                    continue

                if sub == ":":
                    j += 1
                    sub = line[i: j]
                    if sub == ":=":
                        tokens.append(sub)
                    i = j
                    j = i + 1
                    continue

                if sub == "|":
                    tokens.append("|")
                    i += 1
                    j += 1
                    continue
            prodArray.append(tokens)
            line = f.readline().strip()
    P = {v: [] for v in V}
    for prod in prodArray:
        v = prod[0]
        currentProd = []
        for i in range(2, len(prod)):
            if prod[i] != "|":
                currentProd.append(prod[i])
            else:
                P[v].append(currentProd)
                currentProd = []
        P[v].append(currentProd)

    return Grammar(V, T, start, P)
