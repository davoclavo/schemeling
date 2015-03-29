# Parser for the Schemeling Interpreter
#
# Authors: Keyan Pishdadian and David Gomez Urquiza
import operator

def tokenize(string):
    """
    Returns a list containing each individual character of a string.

    string --> a string of Lisp code
    """
    string = string.replace("(", " ( ")
    string = string.replace(")", " ) ")
    token_list = string.split()

    return token_list


def parenthesize(tokens, array=[]):
    """
    Returns a nested array where each '(' starts a new dict and each
    character is labeled by type and value

    tokens --> an array of characters from tokenize()
    """
    try:
        current_token = tokens.pop(0)
    except IndexError:
        current_token = None

    if current_token == '(':
        array.append(parenthesize(tokens, []))
    elif current_token == ')':
        return array
    elif current_token is not None:
        array.append(categorize(current_token))
        parenthesize(tokens, array)

    return array


def categorize(token):
    """
    Returns a dict with two entries, 'type' and 'indentifier' which describe
    the input token

    token --> a single, non-parenthesis, token from the array passed to
    parenthesize()
    """

    try:
        return {'type': 'literal', 'value': int(token)}
    except:
        return {'type': 'identifier', 'value': token}

def parse(lisp_string):
    """
    Just a wrapper for tokenize() and subsequent parenthesize()
    """
    if lisp_string == '':
        return
    else:
        return parenthesize(tokenize(lisp_string)).pop()

def scheme_eval(ast, environment=None):
    if type(ast) == list:
        first_element = ast[0]
        if first_element['type'] == 'identifier':
            numbers = [scheme_eval(number, environment) for number in ast[1:]]
            if first_element['value'] == '+':
                return reduce(operator.add, numbers)
            if first_element['value'] == '*':
                return reduce(operator.mul, numbers)
            if first_element['value'] == '-':
                return reduce(operator.sub, numbers)
            if first_element['value'] == '/':
                return reduce(operator.div, numbers)
    else:
        if ast['type'] == 'identifier':
            return lookup(ast['value'], environment)
        if ast['type'] == 'literal':
            return ast['value']

def lookup(variable, environment):
    if environment == None:
        raise SyntaxError
    elif environment.entries.has_key(variable):
        return environment.entries[variable]
    else:
        return lookup(variable, environment.parent)

class Environment(object):
    def __init__(self, entries, parent=None):
        self.parent = parent
        self.entries = entries

if __name__ == "__main__":
    print parse("((lambda (x) x) 'Lisp')")
    print scheme_eval(parse("(+ 1 2 3 4)"))
    print scheme_eval(parse("(* 2 (+ 2 3 4))"))
    print scheme_eval(parse("(- 20 2 3 4)"))
    print scheme_eval(parse("(+ 1 x)"), Environment({'x': 5}))
