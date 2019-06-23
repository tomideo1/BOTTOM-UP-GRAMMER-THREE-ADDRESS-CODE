class Grammar:
    def __init__(self,V,T, E, P):
        self.V = V
        self.T = T
        self.E = E
        self.P = P
        self.reverse = {}
        for i in P:
            production =  P[i]
            for inner_element in production:
                production_string = "".join(inner_element)
                self.reverse[production_string] = i

    def checkTerminal(self,string):
        return string in self.T
    def tokenizer(self,string):
        token_arr = []
        last_element = len(string) + 1
        i, j = 0, 1
        while j != last_element:
            sub = string[i: j]
            if sub == " ":
                i += 1
                j += 1
                continue

            if self.checkTerminal(sub):
                while self.checkTerminal(sub):
                    j += 1
                    sub = string[i: j]
                    if j == last_element: break
                j -= 1
                token_arr.append(string[i:j])
                i = j
                j = i + 1
                continue
            else:
                raise Exception("shitty")
        return token_arr

    def iterateStack(self, stack, production):
        last = len(stack) + 1
        first = 0
        sub = "".join(stack[first:last])
        for i in range(first, last):
            sub = "".join(stack[i:last])
            if sub in self.reverse:
                replace = self.reverse[sub]
                production.append({'key': sub, 'value': replace})
                stack = stack[0:i] + [replace]
                return self.iterateStack(stack, production)
        return stack
    def parseTree(self, string):
        try:
            production = []
            tokens = self.tokenizer(string)
            filter= "".join(tokens)
            stack = []
            tokens.reverse()
            inputs = tokens
            while len(inputs) > 0:
                stack = self.iterateStack(stack, production)
                if len(inputs) > 0:
                    handle = inputs.pop()
                else:
                    break
                stack.append(handle)
            stack = self.iterateStack(stack, production)
            if len(stack) == 1 and stack[0] == self.E:
                print('BOTTOM UP APPROACH\n')
                print(string,'\n')
                s = "{:>10} -------------->{:>50}"
                for p in production:
                    v = p['value']
                    t = p['key']
                    prod = "{} =>{}".format(v, t)
                    print(s.format(prod, filter))
                    filter= filter.replace(t, v, 1)
                print(s.format(filter, ""))
                print('accept string')
            else:
                print('BOTTOM UP APPROACH\n')
                s = "{:>10} -------------->{:>50}"
                for p in production:
                    v = p['value']
                    t = p['key']
                    prod = "{} => {}".format(v, t)
                    print(s.format(prod, filter))
                    filter = filter.replace(t, v, 1)
                print(s.format(filter, ""))
                print("reject")
        except:
            print("process error")



