# Programmers: Salvador Delgado, Brandy Nguyen, Landon Patam, & Nicholas Reeves
import re
# Lists of Seperators, Operators and Keywords for later reference
separators = ["(", ")", ";", "{", "}", "[", "]", ",", "@"]
operators = ["+", "-", "*", "/", "=", "==", "!=", "<", ">", ">=", "<=", "and", "or", "not"]
keywords = ["while", "if", "for", "fi", "integer", "boolean", "real", "put", "function", "return", "get", "true", "false", "else", "elif", "main"]

# Takes text from input file and converts into a string with no spaces
with open("input.txt", "r" ) as file:
     input = file.read()

# Removes comments from the input string
input = re.sub(r"\[\*.*?\*\]", "", input)

# Instantiating list for Tokens
tokens = []

# Loops through the input_nospaces and seperates each token and places them into a list
temp_token = ""
    
for j in range(len(input)):
    i = input[j]
    if temp_token in operators:
            tokens.append(temp_token)
            temp_token = ""
    if (i in separators) or (i in operators):         
        if len(temp_token) != 0:
          tokens.append(temp_token)
          temp_token = ""
        tokens.append(i)
    elif i == "\n":
         tokens.append(temp_token)
         temp_token = ""
    elif i == " ":
         tokens.append(temp_token)
         temp_token = ""
    else:
        temp_token += i


# Removes spaces and empty tokens from list
tokens = [i for i in tokens if i != "" and i != " "]

# Deals with edge cases of "<" and ">" followed by "="
index = 0
while index < len(tokens):
    i = tokens[index]

    if i == "<":
        if index + 1 < len(tokens) and tokens[index + 1] == "=":
            tokens[index] = "<="
            del tokens[index + 1]

    elif i == ">":
        if index + 1 < len(tokens) and tokens[index + 1] == "=":
            tokens[index] = ">="
            del tokens[index + 1]

    elif i == "=":
        if index + 1 < len(tokens) and tokens[index + 1] == "=":
            tokens[index] = "=="
            del tokens[index + 1]
     
    elif i == "!":
         if index + 1 < len(tokens) and tokens[index + 1] == "=":
              tokens[index] = "!="
              del tokens[index + 1]

    index += 1


# Removes comments from the tokens list

#print(tokens)

first_index = None
last_index = None
for i in range(len(tokens)):
     if tokens[i] == "[" and tokens[i+1] == "*":
          #print ("Found comment" + tokens[i] + tokens[i+1] )
          first_index = i
     elif tokens[i] == "*" and tokens[i+1] == "]":
          last_index = i + 1
if first_index != None and last_index != None:
     del tokens[first_index: last_index+1]

# FSM for Integer
def isInteger(token):
     Integer_dictionary = {
     1 : [1, 2],
     2 : [2, 2]
     }

     state = 1
     accepting_states = [1]

     for i in token:
          if i.isdigit():
               state = Integer_dictionary[state][0]
          else:
               state = 2   
                         
               # checks if final state is in accepting state
     if state in accepting_states:
          return True
     else:
          return False
     

# FSM for Real

def isReal(token):
     real_dictionary = {
     1 : [2, 3],
     2 : [2, 4],
     3 : [3, 3],
     4 : [5, 3],
     5 : [5, 3],

     }

     state = 1
     accepting_states = [5]

     for i in token:
          if i.isdigit():
               state = real_dictionary[state][0]
          elif i == ".":
               state = real_dictionary[state][1]
          else:
               state = 3
                     
                         
               # checks if final state is in accepting state
     if state in accepting_states:
          return True
     else:
          return False


# FSM for Identifer
def isIdentifier(token):
     Identifier_dictionary = {
     1 : [2, 3],
     2 : [4, 5],
     3 : [3, 3],
     4 : [4, 5],
     5 : [6, 5],
     6 : [7, 5],
     7 : [6, 5]

     }

     state = 1
     accepting_states = [2,4,6,7]

     for i in token:
          if i.isalpha():
               state = Identifier_dictionary[state][0]
          elif i.isdigit():
               state = Identifier_dictionary[state][1]
          else:
               state = 3
                    
                    
          # checks if final state is in accepting state
     if state in accepting_states:
          return True
     else:
          return False



# SYNTACTICAL ANALYZER PORTION

with open ("output.txt", "w") as file:
        file.write(f'Output:\nToken{" "*17}{"Lexeme":<23}{"Production Rules"}\n{"-"*9}{" "*13}{"-"*8}{" "*15}{"-"*20}\n')

switch = True

tokens_index = 0

token = tokens[tokens_index]
rules_used = []

def lexer():
    global tokens_index, token, rules_used
    token_type = ""
    if token in operators:
          token_type ='Operator' 
    elif token in separators:
                token_type = 'Separator'
    elif token in keywords:
                token_type = 'Keyword'
    elif isReal(token):
                token_type = 'Real'
    elif isInteger(token):
                token_type = 'Integer'
    elif isIdentifier(token):
                token_type = 'Identifier'
    else:
                token_type = 'Unknown'
    with open("output.txt", "a") as file:



        file.write(f"{token_type:<25}{token:<20}{', '.join(rules_used)}\n")
        rules_used = []
        tokens_index += 1
        if tokens_index < len(tokens):
            token = tokens[tokens_index]

    

# for i in range (len(tokens)):
#    print (tokens[i])
#    lexer()

# Rules

switch = True




def Rat24F():
    if switch:
        print(token + " " + "Rat24F")
        rules_used.append("Rat24F")

    OptFunctionDefinitions()
    if token == "@":
        lexer()
        OptDeclarationList()
        StatementList()
        if token == "@":
            lexer()
        else:
            print("Error, expected @ at end of statement")



def OptFunctionDefinitions():
    if switch:
        print(token + " " + "OptFunctionDefinitions")
        rules_used.append("OptFunctionsDefinitions")
        if token == "function":
            FunctionDefinitions()
        else:
            return

def FunctionDefinitions():
    if switch:
        print(token + " " + "FunctionDefinitions")
        rules_used.append("FunctionsDefinitions")
    Function()
    FunctionDefinitions_prime()


def FunctionDefinitions_prime():
    if switch:
        print(token + " " + "FunctionDefinitions_prime")
        rules_used.append("FunctionsDefintions_prime")
    if token == "function":
        FunctionDefinitions()


def Function():
    if switch:
        print(token + " " + "Function")
        rules_used.append("Function")
    if token == 'function':
        lexer()
        if isIdentifier(token):
            lexer()
            if token == '(':
                lexer()
                OptParameterList()
                if token == ')':
                    lexer()
                    OptDeclarationList()
                    Body()

def OptParameterList():
    if switch:
        print(token + " " + "OptParameterList")
        rules_used.append("OptParamaterList")
    if isIdentifier(token):
        ParameterList()

def ParameterList():
    if switch:
        print(token + " " + "ParameterList")
        rules_used.append("ParamaterList")
    Parameter()
    ParameterListPrime()

def ParameterListPrime():
    if switch:
        print(token + " " + "ParameterListPrime")
        rules_used.append("ParamaterListPrime")
    if token == ",":
        lexer()
        ParameterList()

def Parameter():
    if switch:
        print(token + " " + "Parameter")
        rules_used.append("Paramater")
    if isIdentifier(token):
        IDs()
        Qualifier()

def Qualifier():
    if switch:
        print(token + " " + "Qualifier")
        rules_used.append("Qualifier")
    if (isInteger(token) or isReal(token) or (isinstance(token, bool))):
        lexer()

def Body():
    if switch:
        print(token + " " + "Body")
        rules_used.append("Body")

def OptDeclarationList():
    if switch:
        print(token + " " + "OptDeclarationList")
        rules_used.append("OptDeclarationList")

def DeclarationList():
    if switch:
        print(token + " " + "DeclarationList")
        rules_used.append("DeclarationList")

def DeclarationList_prime():
    if switch:
        print(token + " " + "DeclarationList_prime")
        rules_used.append("DeclarationList_prime")


def Declaration():
    if switch:
        print(token + " " + "Declaration")
        rules_used.append("Declaration")

def IDs():
    if switch:
        print(token + " " + "IDs")
        rules_used.append("IDs")

def IDs_prime():
    if switch:
        print(token + " " + "IDs_prime")
        rules_used.append("IDs_prime")


def StatementList():
    if switch:
        print(token + " " + "StatementList")
        rules_used.append("StatementList")
    Statement()
    StatementList_prime()

def StatementList_prime():
    if switch:
        print(token + " " + "StatementList_prime")
        rules_used.append("StatementList_prime")
        if token in {"if", "return", "put", "get", "while"}:
            StatementList()

def Statement():
    if switch:
        print(token + " " + "Statement")
        rules_used.append("Statement")
        if token == '{':
            Compound()
        elif isIdentifier(token):
            Assign()
        elif token == 'if':
            If()
        elif token == 'return':
            Return()
        elif token == 'put':
            Print()
        elif token == 'get':
            Scan()
        elif token == 'while':
            While()

def Compound():
    if switch:
        print(token + " " + "Compound")
        rules_used.append("Compound")

def Assign():
    if switch:
        print(token + " " + "Assign")
        rules_used.append("Assign")
    if isIdentifier(token):
        lexer()
        if token == '=':
            lexer()
            Expression()
            if token == ';':
                lexer()

def If():
    if switch:
        print(token + " " + "If")
        rules_used.append("If")
    if token == "if":
        lexer()
        if token == "(":
            lexer()
            Condition()
            if token == ")":
                lexer()
                Statement()
                If_prime()
            else:
                print("Error: Expected ')' at end of condition in if statement")
        else:
            print("Error: Expected '(' after 'if'")


def If_prime():
    if switch:
        print("If_prime")
        rules_used.append("If_prime")

def Return():
    if switch:
        print("Return")
        rules_used.append("Return")

def Return_prime():
    if switch:
        print("Return_prime")
        rules_used.append("Return_prime")

def Print():
    if switch:
        print("Print")
        rules_used.append("Print")

def Scan():
    if switch:
        print("Scan")
        rules_used.append("Scan")

def While():
    if switch:
        print("While")
        rules_used.append("While")

def Condition():
    if switch:
        print("Condition")
        rules_used.append("Condition")

def Relop():
    if switch:
        print("Relop")
        rules_used.append("Relop")

def Expression():
    if switch:
        print(token + " " + "Expression")
        rules_used.append("Expression")
    Term()  # Start by parsing a term
    ExpressionPrime()  # Handle additional terms (if any) via ExpressionPrime

def ExpressionPrime():
    if switch:
        print(token + " " + "ExpressionPrime")
        rules_used.append("ExpressionPrime")
    if token == "+":  # Check for addition operator
        lexer()  # Move to the next token
        Term()  # Parse the next term after '+'
        ExpressionPrime()  # Recur to handle more additions if present
    # If token is not '+', we assume epsilon (no further action needed)

def Term():
    if switch:
        print(token + " " + "Term")
        rules_used.append("Term")
    Factor()  # Start by parsing a factor
    TermPrime()  # Handle further multiplication or division (if needed)

def TermPrime():
    if switch:
        print(token + " " + "TermPrime")
    # Here you could handle other operators like *, /
    # For addition, only use ExpressionPrime, not TermPrime

def Factor():
    if switch:
        print(token + " " + "Factor")
        rules_used.append("Factor")
    # Factor could be an integer, identifier, or nested expression
    if isInteger(token) or isIdentifier(token):
        lexer()  # Move past the integer or identifier token
    elif token == "(":  # Handle parentheses
        lexer()  # Consume '('
        Expression()  # Recursively parse the expression inside parentheses
        if token == ")":
            lexer()  # Consume ')'
        else:
            print("Error: Expected ')' after expression")
    else:
        print("Error: Unexpected token in Factor")


def Primary():
    if switch:
        print("Primary")

def Empty():
    if switch:
        print("Empty")


Rat24F()
