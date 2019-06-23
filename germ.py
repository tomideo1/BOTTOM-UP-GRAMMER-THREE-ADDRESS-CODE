class Grammar:
    def __init__(self, variables, terminals, start, production):
        self.variables = variables
        self.terminals = terminals
        self.start = start
        self.production = production
        self.reverseProduction = {}
        for V in production:
            prods = production[V]
            for inner in prods:
                prodstring = "".join(inner)
                self.reverseProduction[prodstring] = V

    def isTerminal(self, s):
        return s in self.terminals

    def tokenize(self, string):
        tokens = []
        last = len(string) + 1
        i, j = 0, 1
        while j != last:
            sub = string[i : j]
            if sub == " ":
                i += 1
                j += 1
                continue
            
            if self.isTerminal(sub):
                while self.isTerminal(sub):
                    j += 1
                    sub = string[i: j]
                    if j == last: break
                j -= 1
                tokens.append(string[i:j])
                i = j
                j = i + 1
                continue
            else:
                raise Exception("shitty")
        return tokens

    def checkStack(self, stack, production):
        last = len(stack) + 1
        first = 0
        sub = "".join(stack[first:last])
        for i in range(first, last):
            sub = "".join(stack[i:last])
            if sub in self.reverseProduction:
                replace = self.reverseProduction[sub]
                production.append({'key': sub, 'value': replace})
                stack = stack[0:i] + [replace]
                return self.checkStack(stack, production)
        return stack



    def parse(self, string):
        try:
            production = []
            tokens = self.tokenize(string)
            cleanstring = "".join(tokens)
            stack = []
            tokens.reverse()
            inputs = tokens
            while len(inputs) > 0:
                stack = self.checkStack(stack, production)
                if len(inputs) > 0:
                    handle = inputs.pop()
                else:
                    break
                stack.append(handle)
            stack =self.checkStack(stack, production)
            if len(stack) == 1 and stack[0] == self.start:
                print("accept")
                s = "{:>20} {:>20}"
                for p in production:
                    v = p['value']
                    t = p['key']
                    prod = "{} => {}".format(v, t)
                    print(s.format(cleanstring, prod))
                    cleanstring = cleanstring.replace(t, v, 1)
                print(s.format(cleanstring,""))
                print('accept')
            else:
                print('reject')
                s = "{:>20} {:>20}"
                for p in production:
                    v = p['value']
                    t = p['key']
                    prod = "{} => {}".format(v, t)
                    print(s.format(cleanstring, prod))
                    cleanstring = cleanstring.replace(t, v, 1)
                print(s.format(cleanstring,""))
                print("reject")
                
        except:
            print("tokenization failed")




def readGrammar(filename):
    start = None
    V = set()
    T = set()
    P = dict()
    prodArray = []
    with open('{}'.format(filename)) as f:
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


if __name__ == "__main__":
    G = readGrammar('grammar.gram')
    G.parse("e^x = 1 + ( x / 1!) + ((x^2) / 2!) + ((x^3)  / 3!) + ((x^4) /4!) ")
    # G.parse("2 + 3*6")
    # G.parse("aaabba")
    pass