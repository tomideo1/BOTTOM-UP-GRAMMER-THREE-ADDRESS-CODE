
from ReadFile import *

if __name__ == "__main__":
    G = read_from_file('grammar.gram')
    G.parseTree("e^x = 1 + ( x / 1!) + ((x^2) / 2!) + ((x^3)  / 3!) + ((x^4) /4!)")
    # G.parseTree("2 + 3*6")
    # G.parse("aaabba")
    pass