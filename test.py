'''
R1. E --> TE'
R2. E' --> +TE' | -TE' | epsilon
R3. T --> id
'''


tokens = ["a", "+", "b", "-", "c"]
id = ["a", "b", "c"]
switch = True


tokens_index = 0

def token():
    if tokens_index <len(tokens):
        return tokens[tokens_index]
    else:
        return None

def lexer():
    global tokens_index
    tokens_index += 1



def E():
    if switch:
        print ("E --> TE'")
    T()
    E_()
    

def E_():
    if switch:
        print("E --> +TE' | -TE' | EMPTY")
    if token() == "+" or token() == "-":
        lexer()
        T()
        E_()


def T():
    if switch:
        print("T --> id")
    if token() in id:
       lexer()
    else:
        print("ID EXPECTED")

E()



