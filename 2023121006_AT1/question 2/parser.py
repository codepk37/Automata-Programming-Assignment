

########################## BOILERPLATE ENDS ###########################
import sys
sys.tracebacklimit=0
class TokenType:
    IDENTIFIER = "IDENTIFIER"
    KEYWORD = "KEYWORD"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    SYMBOL = "SYMBOL"

# Token hierarchy dictionary
token_hierarchy = {
    "if": TokenType.KEYWORD,
    "else": TokenType.KEYWORD,
    "print": TokenType.KEYWORD
}


# Helper function to check if it is a valid identifier
def is_valid_identifier(lexeme):
    if not lexeme:
        return False

    # Check if the first character is an underscore or a letter
    if not (lexeme[0].isalpha() or lexeme[0] == '_'):
        return False

    # Check the rest of the characters (can be letters, digits, or underscores)
    for char in lexeme[1:]:
        if not (char.isalnum() or char == '_'):
            return False

    return True


# Tokenizer function
def tokenize(source_code):
    tokens = []
    position = 0

    while position < len(source_code):
        # Helper function to check if a character is alphanumeric
        def is_alphanumeric(char):
            return char.isalpha() or char.isdigit() or (char == '_')

        char = source_code[position]

        # Check for whitespace and skip it
        if char.isspace():
            position += 1
            continue

        # Identifier recognition
        if char.isalpha():
            lexeme = char
            position += 1
            while position < len(source_code) and is_alphanumeric(source_code[position]):
                lexeme += source_code[position]
                position += 1

            if lexeme in token_hierarchy:
                token_type = token_hierarchy[lexeme]
            else:
                # Check if it is a valid identifier
                if is_valid_identifier(lexeme):
                    token_type = TokenType.IDENTIFIER
                else:
                    raise ValueError(f"Invalid identifier: {lexeme}")

        # Integer or Float recognition
        elif char.isdigit():
            lexeme = char
            position += 1

            is_float = False
            while position < len(source_code):
                next_char = source_code[position]
                # Checking if it is a float, or a full-stop
                if next_char == '.':
                    if (position + 1 < len(source_code)):
                        next_next_char = source_code[position + 1]
                        if next_next_char.isdigit():
                            is_float = True

                # Checking for illegal identifier
                elif is_alphanumeric(next_char) and not next_char.isdigit():
                    while position < len(source_code) and is_alphanumeric(source_code[position]):
                        lexeme += source_code[position]
                        position += 1
                    if not is_valid_identifier(lexeme):
                        raise ValueError(f"Invalid identifier: {str(lexeme)}\nIdentifier can't start with digits")

                elif not next_char.isdigit():
                    break

                lexeme += next_char
                position += 1

            token_type = TokenType.FLOAT if is_float else TokenType.INTEGER

        # Symbol recognition
        else:
            lexeme = char
            position += 1
            token_type = TokenType.SYMBOL

        tokens.append((token_type, lexeme))

    return tokens






def checkGrammar(tokens):
    current_token_index = 0
    flagafterif=0  #track of if
    def tokenafterme():
        
        return len(tokens)-(current_token_index+1)

    def S():
        nonlocal current_token_index

        statement()

        
    def statement():
        nonlocal current_token_index,flagafterif
        
        #print("statement ",tokens[current_token_index][1])  when statement is called 

        if current_token_index < len(tokens):
            if tokens[current_token_index][1] == 'if':
                flagafterif=1
                current_token_index += 1
                if(current_token_index>=len(tokens) or tokens[current_token_index][1] in ["if","else"]):
                    raise Exception("no conditoin")
                A()
                 
                
            elif (flagafterif==1 and tokens[current_token_index][1] == 'else'):
                # after A-> cond)(statement) ,i cant go back A ,now so handling else in (statement itself)
                flagafterif=0
                current_token_index +=1

                if(current_token_index>=len(tokens) ):#or (current_token_index<len(tokens) and tokens[current_token_index][1] == 'if') ) :
                    raise Exception("where's else statement")

                statement()
                

            elif (flagafterif==0 and tokens[current_token_index][1] == 'else'):
                raise Exception("'else' occurs before 'if'")
            
            ## (st)(st) case or y case
            elif tokenafterme()==0: #//////////////////########///////
                y()
            else :
                y()  # like  print x y z if 2+3
##                if( tokens[current_token_index][1] in ["if","else"]):
##                    statement()
##                    return   ##jese if   or else come ,back to control flow ,nahito its counting if,else as common word
                
                statement()

    def A():
        nonlocal current_token_index            

        cond()

        if(current_token_index>=len(tokens)) :
                    raise Exception("where's if statement")
        
        statement()
               #execute statement ->st st untill 'else' or 'if' comes
##      if current_token_index < len(tokens) and tokens[current_token_index][1] == 'else':
##      "ELSE"  PART HANDLED IN STATEMENT 
##            current_token_index += 1
##            statement()

    def cond():
        nonlocal current_token_index
        if(current_token_index>=len(tokens)) :
                    raise Exception("where's condition")
        x()
        while(current_token_index<len(tokens) and tokens[current_token_index][0] in TokenType.SYMBOL):
            op1()    ## as x->cond i.e.   (x) op1 (x) op1 (x) ...untill op1 comes
            x()
        if(current_token_index<len(tokens) and tokens[current_token_index][1]=="else"):
                raise Exception("missed statement after if")

    def op1():
        nonlocal current_token_index
        if current_token_index < len(tokens):
            op = tokens[current_token_index][1]
            if op in ['+', '-', '*', '/', '^', '<', '>', '=']:
                current_token_index += 1
            else:
                raise SyntaxError(f"Invalid operator: {op}")

    def x():
        nonlocal current_token_index
        
        if current_token_index < len(tokens):
            token_type, lexeme = tokens[current_token_index]
            if token_type in [TokenType.INTEGER, TokenType.FLOAT,TokenType.IDENTIFIER] or lexeme=="print":
                current_token_index += 1
            else:
                raise Execption("Not a valid condition")
                current_token_index += 1 #done in cond: x-> cond , i.e. x op1 x
        

    def y():
        nonlocal current_token_index
        if current_token_index < len(tokens):
            token_type, lexeme = tokens[current_token_index]
            if token_type in [TokenType.INTEGER, TokenType.FLOAT,TokenType.IDENTIFIER] or lexeme=="print":
                current_token_index += 1
            else:
                
                raise Exception(f"Invalid token: {lexeme} in Statement")
    
    S()   #calling S start
    if current_token_index != len(tokens):
        #TRACK ERROR FROM HERE 
        print(current_token_index,len(tokens))
        raise SyntaxError("Syntax error: Extra tokens at the end of the input")


# Test the tokenizer and syntax checker
if __name__ == "__main__":
    source_code = " if con sta +stat " #dont pass symbols " ; ,symbols " -ve number , semi-colon

    source_code=input("enter input statement :    ");
    
    tokens = tokenize(source_code)

    

    try:
        checkGrammar(tokens)
        print("Syntax analysis passed.")
        for token in tokens:
            print(f"Token Type: {token[0]}, Token Value: {token[1]}")
        
    except SyntaxError as e:
        print(f"Syntax Error : {e}")

## 2xi for (x) op1 (x)  ,and for  y is done in boilerplate
