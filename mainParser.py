from Tree import TreeNode, Tree
import time
from graphviz import Graph
import shared

#######################SCANNER PART########################
Reserved_words_tuple = ("if", "else", "then", "until", "read", "write", "repeat", "end")

Special_characters_dict = {
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MULT',
    '/': 'DIV',
    '=': 'EQUAL',
    '<': 'LESSTHAN',
    ';': 'SEMICOLON',
    '(': 'OPENBRACKET',
    ')': 'CLOSEDBRACKET'
}
state_type = {"in_id": "IDENTIFIER", "in_num": "NUMBER", "in_assignment": "ASSIGN"}
keys = Special_characters_dict.keys()


def getScannerError():
    return scannerErrorFlag


# Defining the class TokenRecord
class TokenRecord:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def print_token(self, output_file):
        output_file.write(self.value + "," + self.type + "\n")


# Scanning a character and determining the state
def getToken(look_ahead_char, line, input_file):
    # To store in it the value of the token to be generated
    state = "start"
    while 1:
        if (state != "done" and state != "trap"):
            if (look_ahead_char == ""):
                char = input_file.read(1)  # The character that makes us change states
                if (char == ""):

                    if (state == "in_comment" or state == "in_assign"):
                        if (state == "in_comment"):
                            token = create_token("ERROR", "Expected symbol '}' in line " + str(line), line)

                        else:
                            token = create_token("ERROR", "Unexpected symbol ':' in line " + str(line), line)
                        state = "trap"

                    elif (state == "in_num" or state == "in_id"):
                        if (parsed_string in Reserved_words_tuple):
                            token = create_token(parsed_string.upper(), parsed_string, line)
                        else:
                            token = create_token(state_type[state], parsed_string, line)
                        #token = create_token(state_type[state], parsed_string, line)
                        state = "done"
                    else:
                        return {"token": create_token("EOF", "", line), "look_ahead_char": look_ahead_char,
                                "line": line}
            else:
                char = look_ahead_char
                look_ahead_char = ""

        if state == "start":  # Start State

            parsed_string = ""
            if (char.isdigit()):
                state = "in_num"
                parsed_string = char
            elif (char.isalpha()):
                state = "in_id"
                parsed_string = char
            elif (char == ':'):
                state = "in_assignment"
                parsed_string = char
            elif (char == "{"):
                state = "in_comment"
            elif (char in keys):
                state = "done"
                token = create_token(Special_characters_dict[char], char, line)
            elif (char == " " or char == "\n" or char == "\t"):
                state = "start"
                if (char == "\n"):
                    line = line + 1;
            else:
                state = "trap"
                token = create_token("ERROR", "Unexpected symbol '" + char + "' in line " + str(line), line)

        elif state == "in_comment":  # In-Comment State
            if (char == "}"):
                state = "start"
            elif (char == "\n"):
                line = line + 1
        elif state == "in_id":  # In-ID State
            if (char.isalpha()):
                parsed_string = parsed_string + char
            else:
                if (parsed_string in Reserved_words_tuple):
                    token = create_token(parsed_string.upper(), parsed_string, line)
                else:
                    token = create_token(state_type[state], parsed_string, line)
                look_ahead_char = char
                state = "done"

        elif state == "in_num":  # In-Num State
            if (char.isdigit()):
                parsed_string = parsed_string + char
            else:
                token = create_token(state_type[state], parsed_string, line)
                look_ahead_char = char
                state = "done"
        elif state == "in_assignment":  # In-Assignment State
            if (char == "="):
                token = create_token(state_type[state], ":=", line)
                state = "done"
            else:
                state = "trap"
                token = create_token("ERROR", "Unexpected symbol ':' in line " + str(line), line)


        elif state == "done":  # Done State

            return {"token": token, "look_ahead_char": look_ahead_char, "line": line}

        elif state == "trap":  # Trap State
            return {"token": token, "look_ahead_char": look_ahead_char, "line": line}


def create_token(type, value, line):
    token = TokenRecord(type, value, line)
    return token


def scannerMain(url):
    data=open(url,'r')
    # data = open("inputTiny.txt", 'r')
    global scannerErrorFlag
    global token_list
    token_list = []
    scannerErrorFlag = False
    # Loop to generate tokens until the end of the file
    look_ahead_char = ""
    line = 1
    token_number = 0
    # output_file = open("outputTokens.txt", "w+").close()
    output_file = open("outputTokens.txt", "w+")
    while 1:
        result = getToken(look_ahead_char, line, data)
        token = result["token"]
        look_ahead_char = result["look_ahead_char"]
        line = result["line"]
        if (token.type == "ERROR"):
            output_file.close()
            scannerErrorFlag = True
            return (token.value)  ###############TO BE PRINTED IN GUI
            break
        elif (token.type == "EOF"):
            output_file.close()
            return ("DONE: The number of tokens = " + str(token_number))  ###############TO BE PRINTED
            break
        else:
            token.print_token(output_file)
            token_list.append(token)
            token_number = token_number + 1
    output_file = open("outputTokens.txt", "w+").close()


################END OF SCANNER###############################


###############PARSER PART###################################
def match(token_list, i,
          expected_token_type):  # match function accesses the token_list with the index i (passed as a parameter),
    # checks its *type* and increments i and returns the new i, if not -> error (send a message), abort
    if (token_list[i].type == expected_token_type):
        #print(token_list[i].type)
        if (i < len(token_list) - 1):
            return i + 1
        else:
            return i - 1
    else:
        shared.parserErrorMessage = 'Error in line: ' + str(token_list[i].line) + ' in word: ' + token_list[
            i].value + ', Expected: ' + expected_token_type.lower()
        raise Exception('ERROR OCCURED:')



#########THE GRAMMAR RULES FUNCTIONS WITHOUT THE OPERATORS (THEY WILL BE EMBEDDED IN THE FUNCTION ITSELF)############
def program():
    i = 0  # token_list index
    program_tree, i = stmt_seq(token_list,
                               i)  # we always return the tree as the first parameter and the index (i) as the second
    print(program_tree)
    return program_tree


def stmt_seq(token_list, i):  # only function that identifies the right_sibling of a node
    temp, i = stmt(token_list, i)  # left most tree

    if (token_list[i].value == ';'):  # if condition for first semicolon to keep value of temp unchanged to return it
        i = match(token_list, i, Special_characters_dict[';'])  # semicolon
        temp1, i = stmt(token_list, i)  # call the stmt after the semicolon (right most tree)
        temp.getRoot().setRightSibling(temp1.getRoot())  # set the right sibling for the left tree

    while i < len(token_list) and token_list[
        i].value == ';':  # second semicolon ########### added the first condition to solve the 'out of range' error
        i = match(token_list, i, Special_characters_dict[';'])
        temp2, i = stmt(token_list, i)
        temp1.getRoot().setRightSibling(temp2.getRoot())
        temp1 = temp2  # updating the left tree to become the right most tree
    return temp, i


def stmt(token_list, i):
    if (token_list[i].value == "if"):
        temp, i = if_stmt(token_list, i)
    elif (token_list[i].value == "repeat"):
        temp, i = repeat_stmt(token_list, i)
    elif (token_list[i].value == "read"):
        temp, i = read_stmt(token_list, i)
    elif (token_list[i].value == "write"):
        temp, i = write_stmt(token_list, i)
    else:  # elif (token_list[i].type == state_type["in_id"]):
        temp, i = assign_stmt(token_list, i)
    # else: # to handle errors
    # error
    return temp, i


def if_stmt(token_list, i):  # if -stmt → if exp then stmt-sequence [else stmt-sequence] end
    i = match(token_list, i, "IF")
    temp = TreeNode("statement", "if")

    new_temp, i = exp(token_list, i)
    temp.addChild(new_temp.getRoot())
    new_temp.getRoot().setParent(temp)

    i = match(token_list, i, "THEN")
    temp2, i = stmt_seq(token_list, i)
    temp.addChild(temp2.getRoot())
    temp2.getRoot().setParent(temp)

    if (token_list[i].value == "else"):
        i = match(token_list, i, "ELSE")
        temp_3, i = stmt_seq(token_list, i)
        temp.addChild(temp_3.getRoot())
        temp_3.getRoot().setParent(temp)

    i = match(token_list, i, "END")

    temp = Tree(temp)

    return temp, i


def repeat_stmt(token_list, i):  # repeat -stmt → repeat stmt-sequence until exp
    i = match(token_list, i, "REPEAT")
    temp = TreeNode("statement", "repeat")

    new_temp, i = stmt_seq(token_list, i)
    temp.addChild(new_temp.getRoot())
    new_temp.getRoot().setParent(temp)

    i = match(token_list, i, "UNTIL")
    temp_2, i = exp(token_list, i)
    temp.addChild(temp_2.getRoot())
    temp_2.getRoot().setParent(temp)

    temp = Tree(temp)

    return temp, i


def assign_stmt(token_list, i):  # identifier:=exp

    temp = TreeNode("statement", "assign\n(" + token_list[i].value + ")")  # TreeNode(self, type, stringValue)
    i = match(token_list, i, state_type["in_id"])  # increment i to point on :=
    i = match(token_list, i, state_type["in_assignment"])  # increment i to point on exp
    new_temp, i = exp(token_list, i)  # call exp
    temp.addChild(new_temp.getRoot())  # set the child relationship
    new_temp.getRoot().setParent(temp)  # set the parent relationship

    temp = Tree(temp)

    return temp, i


def read_stmt(token_list, i):  # read_stmt -> read identifier
    i = match(token_list, i, "READ")
    new_temp = TreeNode("statement", "read\n(" + token_list[i].value + ")")
    i = match(token_list, i, state_type["in_id"])
    temp = Tree(new_temp)
    return temp, i


def write_stmt(token_list, i):
    i = match(token_list, i, "WRITE")
    new_temp = TreeNode("statement", "write")
    temp, i = exp(token_list, i)
    new_temp.addChild(temp.getRoot())
    temp.getRoot().setParent(new_temp)
    temp = Tree(new_temp)
    return temp, i


def exp(token_list, i):  # exp -> simple_exp [comparison-op simple_exp]
    temp, i = simple_exp(token_list, i)  # save the return value of "simple-exp" in temp (returns a Tree)

    if (token_list[i].value == '<' or token_list[i].value == "="):
        new_temp = TreeNode("expression", "op\n(" + token_list[i].value + ")")
        i = match(token_list, i, Special_characters_dict[
            token_list[i].value])  # passing 3 parameters (token_list, i, value of what we want to match)

        new_temp.addChild(temp.getRoot())  # set the child relationship
        temp.getRoot().setParent(new_temp)  # set the parent relationship

        temp2, i = simple_exp(token_list, i)
        new_temp.addChild(temp2.getRoot())  # set the child relationship
        temp2.getRoot().setParent(new_temp)  # set the parent relationship
        temp = Tree(new_temp)

    return temp, i  # we always return the tree as the first parameter and the index (i) as the second


def simple_exp(token_list, i):  # simple-exp->term{addop term}
    temp, i = term(token_list, i)  # save the return value of "term" in temp (returns a Tree)

    while token_list[i].value == '+' or token_list[i].value == '-':
        new_temp = TreeNode("expression", "op\n(" + token_list[i].value + ")")
        i = match(token_list, i, Special_characters_dict[token_list[i].value])

        new_temp.addChild(temp.getRoot())  # set the child relationship
        temp.getRoot().setParent(new_temp)  # set the parent relationship

        temp2, i = term(token_list, i)
        new_temp.addChild(temp2.getRoot())  # set the child relationship
        temp2.getRoot().setParent(new_temp)  # set the parent relationship

        temp = Tree(new_temp)

    return temp, i


def term(token_list, i):  # term->factor{mulop factor}
    temp, i = factor(token_list, i)  # save the return value of "factor" in temp (returns a Tree)

    while token_list[i].value == '*' or token_list[i].value == '/':
        new_temp = TreeNode("expression", "op\n(" + token_list[i].value + ")")
        i = match(token_list, i, Special_characters_dict[token_list[i].value])

        new_temp.addChild(temp.getRoot())  # set the child relationship
        temp.getRoot().setParent(new_temp)  # set the parent relationship

        temp2, i = factor(token_list, i)
        new_temp.addChild(temp2.getRoot())  # set the child relationship
        temp2.getRoot().setParent(new_temp)  # set the parent relationship

        temp = Tree(new_temp)

    return temp, i


def factor(token_list, i):
    if (token_list[i].value == '('):
        i = match(token_list, i, Special_characters_dict['('])
        new_temp, i = exp(token_list, i)
        i = match(token_list, i, Special_characters_dict[')'])

    elif (token_list[i].type == state_type["in_num"]):
        new_temp = TreeNode("expression", "const\n(" + token_list[i].value + ")")
        i = match(token_list, i, state_type["in_num"])

    elif (token_list[i].type == state_type["in_id"]):
        new_temp = TreeNode("expression", "id\n(" + token_list[i].value + ")")
        i = match(token_list, i, state_type["in_id"])

    else:
        shared.parserErrorMessage = 'Error in line: ' + str(token_list[i].line) + ' in word: ' + token_list[
            i].value
        raise Exception('ERROR OCCURED:')

    temp = Tree(new_temp)

    return temp, i


##################END OF PARSER#############################


####################################### LL1 parser ##############################
grammar_rules = [["stmt-seq"],
                 ["statement", "stmt-seq'"],
                 ["SEMICOLON", "statement", "stmt-symbol", "stmt-seq'"],
                 [""],
                 ["if-stmt"],
                 ["repeat-stmt"],
                 ["assign-stmt"],
                 ["read-stmt"],
                 ["write-stmt"],
                 ["IF", "exp", "THEN", "stmt-seq", "if-symbol", "else-part", "END"],
                 ["ELSE", "stmt-seq", "else-symbol"],
                 [""],
                 ["REPEAT", "stmt-seq", "UNTIL", "exp", "repeat-symbol"],
                 ["IDENTIFIER", "ASSIGN", "exp", "assign-symbol"],
                 ["READ", "IDENTIFIER", "read-symbol"],
                 ["WRITE", "exp", "write-symbol"],
                 ["simple-exp", "exp'"],
                 ["comparison-op", "simple-exp", "#"],
                 [""],
                 ["LESSTHAN"],
                 ["term", "simple-exp'"],
                 ["addop", "term", "#", "simple-exp'"],
                 [""],
                 ["PLUS"],
                 ["MINUS"],
                 ["factor", "term'"],
                 ["mulop", "factor", "#", "term'"],
                 [""],
                 ["MULT"],
                 ["DIV"],
                 ["OPENBRACKET", "exp", "CLOSEDBRACKET"],
                 ["NUMBER"],
                 ["IDENTIFIER"],
                 ["EQUAL"]
                 ]
# Parsing table with the corresponding rule number in grammar_rules list
M = [{"IDENTIFIER": 0, "IF": 0, "REPEAT": 0, "READ": 0, "WRITE": 0},
     {"IDENTIFIER": 1, "IF": 1, "REPEAT": 1, "READ": 1, "WRITE": 1},
     {"ELSE": 3, "END": 3, "SEMICOLON": 2, "UNTIL": 3, "$": 3},
     {"IDENTIFIER": 6, "IF": 4, "REPEAT": 5, "READ": 7, "WRITE": 8},
     {"IF": 9},
     {"ELSE": 10, "END": 11},
     {"REPEAT": 12},
     {"IDENTIFIER": 13},
     {"READ": 14},
     {"WRITE": 15},
     {"OPENBRACKET": 16, "NUMBER": 16, "IDENTIFIER": 16},
     {"CLOSEDBRACKET": 18, "THEN": 18, "ELSE": 18, "END": 18, "SEMICOLON": 18, "UNTIL": 18, "$": 18, "LESSTHAN": 17,
      "EQUAL": 17},
     {"OPENBRACKET": 20, "NUMBER": 20, "IDENTIFIER": 20},
     {"CLOSEDBRACKET": 22, "THEN": 22, "ELSE": 22, "END": 22, "SEMICOLON": 22, "UNTIL": 22, "$": 22, "PLUS": 21,
      "MINUS": 21, "LESSTHAN": 22, "EQUAL": 22},
     {"PLUS": 23, "MINUS": 24},
     {"OPENBRACKET": 25, "NUMBER": 25, "IDENTIFIER": 25},
     {"CLOSEDBRACKET": 27, "THEN": 27, "ELSE": 27, "END": 27, "SEMICOLON": 27, "UNTIL": 27, "$": 27, "PLUS": 27,
      "MINUS": 27, "MULT": 26, "DIV": 26, "LESSTHAN": 27, "EQUAL": 27},
     {"MULT": 28, "DIV": 29},
     {"OPENBRACKET": 30, "NUMBER": 31, "IDENTIFIER": 32},
     {"LESSTHAN": 19, "EQUAL": 33}
     ]
# Dictionary to get the non_terminal entry in the parsing table
non_terminal = {"program": 0,
                "stmt-seq": 1,
                "stmt-seq'": 2,
                "statement": 3,
                "if-stmt": 4,
                "else-part": 5,
                "repeat-stmt": 6,
                "assign-stmt": 7,
                "read-stmt": 8,
                "write-stmt": 9,
                "exp": 10,
                "exp'": 11,
                "simple-exp": 12,
                "simple-exp'": 13,
                "addop": 14,
                "term": 15,
                "term'": 16,
                "mulop": 17,
                "factor": 18,
                "comparison-op": 19
                }
# List of non-terminals name
non_terminal_key = non_terminal.keys()
# List of terminals name
terminal = ["OPENBRACKET", "CLOSEDBRACKET", "NUMBER", "IDENTIFIER", "IF", "THEN", "ELSE", "END", "SEMICOLON", "REPEAT",
            "UNTIL", "READ",
            "WRITE", "$", "LESSTHAN", "EQUAL", "PLUS", "MINUS", "MULT", "DIV", "ASSIGN"]

# List of symbols that must be pushed in the tree_stack when it is matched
stacksymbols = ["NUMBER", "IDENTIFIER", "LESSTHAN", "EQUAL", "PLUS", "MINUS", "MULT", "DIV"]

# List of action markers to construct a tree from the subtrees in the tree_stack
actionmarker = ["stmt-symbol", "if-symbol", "else-symbol", "repeat-symbol", "assign-symbol", "read-symbol",
                "write-symbol", "#"]


# LL1 Parser function
def LL1parser():
    tree_stack = []
    token_list.append("$")
    parsing_stack = ["$", "program"]
    i = 0
    while not (parsing_stack[len(parsing_stack) - 1] in terminal and token_list[i] == "$") or (
            parsing_stack[len(parsing_stack) - 1] != "$"):
    #while (parsing_stack[len(parsing_stack) - 1] in terminal or token_list[i] != "$") and (parsing_stack[len(parsing_stack) - 1] != "$"):
        # Get the index of the top of the parsing stack
        n = len(parsing_stack) - 1

        if (token_list[i] != "$"):
            T = token_list[i].type
        else:
            T = "$"

        # If the top of the parsing stack is nonterminal --> generate
        if parsing_stack[n] in non_terminal_key:
            N = non_terminal[parsing_stack[n]]
            terminal_key = M[N].keys()

            if T in terminal_key or T == "$":
                rule = grammar_rules[M[N][T]]
                l = len(rule)
                parsing_stack.pop()
                for j in range(l):
                    parsing_stack.append(rule[l - 1 - j])
            else:
                shared.parserErrorMessage = ' Error in line: ' + str(token_list[i].line) + ' in word: ' + token_list[
                    i].value
                token_list.pop()
                raise Exception('ERROR OCCURED:')
                ###############################ERROR in token_list[i]
                break

        # If the top of the parsing stack is terminal --> check the match
        elif parsing_stack[n] in terminal:
            if parsing_stack[n] == T:
                if T in stacksymbols:
                    if T == "IDENTIFIER":
                        v = "id\n(" + token_list[i].value + ")"
                    elif T == "NUMBER":
                        v = "const\n(" + token_list[i].value + ")"
                    else:
                        v = "op\n(" + token_list[i].value + ")"
                    t = TreeNode("expression", v)
                    temp = Tree(t)
                    tree_stack.append(temp)
                i = i + 1
                parsing_stack.pop()
            else:
                if(T != "$"):
                    shared.parserErrorMessage = ' Error in line: ' + str(token_list[i].line) + ' in word: ' + token_list[
                        i].value + ', Expected: ' + parsing_stack[n]
                else:
                    shared.parserErrorMessage = ' Error in line: ' + str(token_list[i-1].line) + ' Expected: ' + parsing_stack[n]
                token_list.pop()
                raise Exception('ERROR OCCURED:')








        # If the top of the parsing stack is an actionmarker --> build a tree
        elif parsing_stack[n] in actionmarker:
            if parsing_stack[n] == "stmt-symbol":
                new_temp = tree_stack.pop()
                temp = tree_stack.pop()
                temp2 = temp.getRoot()

                while (temp2.getRightSibling() != None):
                    temp2 = temp2.getRightSibling()

                temp2.setRightSibling(new_temp.getRoot())
                tree_stack.append(temp)

            elif parsing_stack[n] == "if-symbol":
                node = TreeNode("statement", "if")
                new_temp = tree_stack.pop()
                temp = tree_stack.pop()
                node.addChild(temp.getRoot())
                node.addChild(new_temp.getRoot())
                temp = Tree(node)
                tree_stack.append(temp)

            elif parsing_stack[n] == "else-symbol":
                new_temp = tree_stack.pop()
                temp = tree_stack.pop()
                temp.getRoot().addChild(new_temp.getRoot())
                tree_stack.append(temp)

            elif parsing_stack[n] == "repeat-symbol":
                node = TreeNode("statement", "repeat")
                new_temp = tree_stack.pop()
                temp = tree_stack.pop()
                node.addChild(temp.getRoot())
                node.addChild(new_temp.getRoot())
                temp = Tree(node)
                tree_stack.append(temp)

            elif parsing_stack[n] == "read-symbol":
                new_temp = tree_stack.pop().getRoot().getStringValue()[3:]
                node = TreeNode("statement", "read\n" + new_temp)
                temp = Tree(node)
                tree_stack.append(temp)

            elif parsing_stack[n] == "assign-symbol":
                temp = tree_stack.pop()
                new_temp = tree_stack.pop().getRoot().getStringValue()[3:]
                node = TreeNode("statement", "assign\n" + new_temp)
                node.addChild(temp.getRoot())
                temp = Tree(node)
                tree_stack.append(temp)

            elif parsing_stack[n] == "write-symbol":
                node = TreeNode("statement", "write")
                new_temp = tree_stack.pop()
                node.addChild(new_temp.getRoot())
                temp = Tree(node)
                tree_stack.append(temp)

            else:
                new_temp = tree_stack.pop()
                op = tree_stack.pop()
                temp = tree_stack.pop()
                op.getRoot().addChild(temp.getRoot())
                op.getRoot().addChild(new_temp.getRoot())
                tree_stack.append(op)
            parsing_stack.pop()

        elif parsing_stack[n] == "":
            parsing_stack.pop()

        else:
            token_list.pop()
            raise Exception('ERROR OCCURED:')  #################No need to handle it

    if parsing_stack[len(parsing_stack) - 1] == "$" and token_list[i] == "$":
        token_list.pop()
        return tree_stack.pop()

    else:

        if token_list[i] == "$":
            shared.parserErrorMessage = ' Error in line: ' + str(token_list[i-1].line)
        else:
            shared.parserErrorMessage = ' Error in line: ' + str(token_list[i].line)

        token_list.pop()
        raise Exception('ERROR OCCURED:')
     ##############ERROR in token_list[i] if its equal "$" generate error for the last line
##################END OF LL1-PARSER #############################


# def Main():
#   token_list = []
#  scannerMain(token_list) # passed by reference
# program_tree = program(token_list)
# program_tree.DrawTree()
# LL1parser(token_list)


# if __name__ == '__main__':
#   Main()




