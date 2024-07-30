# OVE TRI METODE ĆE BITI POZIVANE KROZ AUTOMATSKE TESTOVE. NEMOJTE MENJATI NAZIV, PARAMETRE I POVRATNU VREDNOST.
# Dozvoljeno je implementirati dodatne, pomoćne metode, ali isključivo u okviru ovog modula.

import tokenizer


class StackError(Exception):
    pass


class Stack(object):
    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def push(self, e):
        self._data.append(e)

    def top(self):
        if self.is_empty():
            raise StackError('Stek je prazan.')
        return self._data[-1]

    def pop(self):
        if self.is_empty():
            raise StackError('Stek je prazan.')
        return self._data.pop()


"""Funkcija konvertuje izraz iz infiksne u postfiksnu notaciju
    Args:
        expression (string): Izraz koji se parsira. Izraz može da sadrži cifre, zagrade, znakove računskih operacija.
        U slučaju da postoji problem sa formatom ili sadržajem izraza, potrebno je baciti odgovarajući izuzetak.
    Returns:
        list: Lista tokena koji predstavljaju izraz expression zapisan u postfiksnoj notaciji.
    Primer:
        ulaz '6.11 – 74 * 2' se pretvara u izlaz [6.11, 74, 2, '*', '-']
    """


# + KAO UNARNI OPERATOR, +7+9 NE RADI, () DA LI JE ISPRAVAN IZRAZ ILI NE NPR 7+()9 MENI RADI, LISTA TOKENA DA LI JE TYPIZIRANA ILI SU SVE STRINGOVI (9 7 + URADI 97)

def get_priority(operator):
    if operator == '+' or operator == '-' or operator == '!':
        return 1
    if operator == '*' or operator == '/':
        return 2
    if operator == '^':
        return 3
    return 0


class MySyntaxError(Exception):
    pass


class WrongNumberOperatorsError(Exception):
    pass


class WrongNumberOperandsError(Exception):
    pass


class BracketsError(Exception):
    pass


class MathError(Exception):
    pass


def give_type(token):
    if '.' in token:
        return float(token)
    else:
        return int(token)


def is_operator(token):
    return token in ['-', '+', '/', '^', '*', '!']


def is_operand(token):  # trebalo bi da posto je tokenizer odradio kako treba posao, token ili jedno ili drugo
    return not is_operator(token) and token not in ['(', ')']


def is_all_good(tokens):
    previous_elem = tokens[0]
    if is_operator(previous_elem) and previous_elem != '!':  # ne sme da se zavrsi opretatorom
        raise WrongNumberOperatorsError("Pogresan broj operatora, ne sme izraz da se pocne operatorom")
    if previous_elem == ')':
        raise BracketsError("Izraz ne sme da pocinje sa )")
    stack_zagrada = Stack()
    if previous_elem == '(':
        stack_zagrada.push('(')

    for i in range(1, len(tokens)):
        if tokens[i] == ')':
            if stack_zagrada.is_empty():
                raise BracketsError("Pogresna upotreba zagrada")
            if stack_zagrada.top() == '(':
                stack_zagrada.pop()
        if tokens[i] == '(':
            stack_zagrada.push('(')

        if previous_elem == '!' and is_operator(tokens[i]):  # ovo je dobro
            continue
        if tokens[i] == '!' and is_operator(previous_elem):  # ovo je dobro
            continue

        if is_operator(previous_elem) and is_operator(tokens[i]):
            raise WrongNumberOperatorsError("Pogresan broj operatora, postoji visak")
        if is_operand(previous_elem) and is_operand(tokens[i]):
            raise WrongNumberOperandsError("Pogresan broj operanada, postoji visak")
        if not tokens[i] in ['(', ')']:
            previous_elem = tokens[i]
        if is_operator(tokens[i - 1]) and tokens[i] == ')':
            raise BracketsError("Greska pri upotrebi zagrada")
        if is_operand(tokens[i - 1]) and tokens[i] == '(':
            raise BracketsError("Greska pri upotrebi zagrada")
        if tokens[i-1] == '(' and tokens[i] == ')':
            raise BracketsError("Greska: () nije validan izraz")

    if is_operator(previous_elem):  # ne sme da se zavrsi opretatorom
        raise WrongNumberOperatorsError("Pogresan broj operatora, ne sme da se zavrsi izraz operatorom")
    if not stack_zagrada.is_empty():
        raise BracketsError("Zagrade nisu pravilno zatvorene")


def infix_to_postfix(expression):
    for c in expression:
        if c == ' ' or c == '.':
            continue
        if not (c in ['-', '+', '/', '^', '*', '(', ')'] or '0' <= c <= '9'):
            raise MySyntaxError('Syntax error, token nije operator ni operand')

    tokens = tokenizer.tokenize(expression)

    previous_elem = '('
    for i in range(len(tokens)):
        if tokens[i] == '-' and previous_elem == '(':
            tokens[i] = '!'
        previous_elem = tokens[i]
    is_all_good(tokens)
    # _______________________________________________________________
    # dovde bi trebalo da nema vise gresaka. Ostalo mi je samo da proverim korenovanje negativnog broja...
    ret = []
    stack = Stack()
    stack.push('(')
    for token in tokens:
        if is_operand(token):
            ret.append(token)
            # print("na sol apendujem ", token)
        elif token in ['+', '*', '-', '!', '/', '^']:
            while get_priority(stack.top()) >= get_priority(token):
                ret.append(stack.pop())
            # print("Na stek pushujem: ", token)
            stack.push(token)
        elif token == '(':
            # print("Na stek pushujhem zagradu (")
            stack.push(token)
        elif token == ')':
            # print("Skidanje svih zbog )")
            while stack.top() != '(':
                ret.append(stack.pop())  # praznnjenje pod steka
            stack.pop()  # skidanje (
        else:
            raise MySyntaxError('Syntax error, token nije operator ni operand')
    # print("\nPraznim stek")
    while not stack.is_empty():
        if stack.top() == "(":
            break
        # print("na sol apendujem ", stack.top())
        ret.append(stack.pop())

    ret2 = []
    for elem in ret:
        if is_operator(elem):
            ret2.append(elem)
        else:
            ret2.append(give_type(elem))

    vrednost = calculate_postfix(ret2)  # sluzi samo za proveru da li stepenujem negativnim brojem

    return ret2


def calculate(num1, num2, operation):
    if operation == '+':
        return num1 + num2
    elif operation == '*':
        return num1 * num2
    elif operation == '-':
        return num1 - num2
    elif operation == '/':
        if num2 == 0:
            raise MathError("Ne moze da se deli sa nulom!")
        else:
            return num1 / num2
    elif operation == '^':
        y = num1 ** num2
        if isinstance(y, complex):
            raise MathError("U izracunavanju ste dobili komplexan broj!")
        else:
            return num1 ** num2
    else:
        print(operation)
        raise MySyntaxError("Pogresan operator")


def calculate_postfix(token_list):
    stek = Stack()
    for token in token_list:
        if not is_operator(token):
            stek.push(token)
        else:
            if stek.is_empty():
                raise StackError("Greska prilikom racunanja, previse operatora")
            top_most1 = stek.pop()
            if token == '!':
                stek.push(-1 * top_most1)
            else:
                if stek.is_empty():
                    raise StackError("Greska prilikom racunanja, previse operatora")
                top_most2 = stek.pop()
                stek.push(calculate(top_most2, top_most1, token))

    if stek.is_empty():
        raise StackError("Greska prilikom izracunavanja")
    else:
        ret = stek.pop()
        # print("ret == ", ret)
        if not stek.is_empty():
            raise StackError("Premalo operatora")
        return ret


def calculate_infix(expression):
    tokens = tokenizer.tokenize(expression)
    value_stack = Stack()
    operator_stack = Stack()
    previous_elem = '('
    for i in range(len(tokens)):
        if tokens[i] == '-' and previous_elem == '(':
            tokens[i] = '!'
        previous_elem = tokens[i]
    is_all_good(tokens)
    for token in tokens:
        if is_operand(token):  # broj
            value_stack.push(give_type(token))
        elif token == '(':
            operator_stack.push('(')
        elif token == ')':
            naso = False
            while not operator_stack.is_empty():
                operation = operator_stack.pop()
                if operation == '(':
                    naso = True
                    break
                if value_stack.is_empty():
                    raise StackError("Greska prilikom racunanja, previse operatora")
                top_most1 = value_stack.pop()
                if operation == '!':
                    value_stack.push(-top_most1)
                else:
                    if value_stack.is_empty():
                        raise StackError("Greska prilikom racunanja, previse operatora")
                    top_most2 = value_stack.pop()
                    value_stack.push(calculate(top_most2, top_most1, operation))
            if not naso:
                raise BracketsError("Pogresna upotreba zagrada")
            # print_stack(operator_stack)
        elif is_operator(token):
            if operator_stack.is_empty():
                operator_stack.push(token)
                continue
            while not operator_stack.is_empty():
                operation = operator_stack.top()
                if get_priority(token) > get_priority(operation):
                    break
                operator_stack.pop()

                if value_stack.is_empty():
                    raise StackError("Greska prilikom racunanja, previse operatora")
                top_most1 = value_stack.pop()
                if operation == '!':
                    value_stack.push(-top_most1)
                else:
                    if value_stack.is_empty():
                        raise StackError("Greska prilikom racunanja, previse operatora")
                    top_most2 = value_stack.pop()
                    value_stack.push(calculate(top_most2, top_most1, operation))
            operator_stack.push(token)
        else:
            raise MySyntaxError("Greska, izraz je pogresno napisan")  # mislim da se ovo nikad ni nece desiti al aj

    if operator_stack.is_empty():
        sol = value_stack.pop()
        if not value_stack.is_empty():
            raise WrongNumberOperatorsError("Fali operatora, greska")
        else:
            return sol
    else:
        while not operator_stack.is_empty():
            operation = operator_stack.top()
            if value_stack.is_empty():
                raise StackError("Greska prilikom racunanja, previse operatora")
            operator_stack.pop()
            top_most1 = value_stack.pop()
            if operation == '!':
                value_stack.push(-top_most1)
            else:
                if value_stack.is_empty():
                    raise StackError("Greska prilikom racunanja, previse operatora")
                top_most2 = value_stack.pop()
                value_stack.push(calculate(top_most2, top_most1, operation))
    sol = value_stack.pop()
    if not value_stack.is_empty():
        while not value_stack.is_empty():
            print(value_stack.pop())
        raise WrongNumberOperatorsError("Fali operatora, greska")
    else:
        return sol

