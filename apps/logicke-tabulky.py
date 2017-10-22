OPERATOR = 'op'
PREMENNA = 'var'
ODKAZ    = 'ref'
ZATVORKA = 'par'

def lex_nacitaj(vyraz):
    i = 0
    while i < len(vyraz):
        symbol = vyraz[i]

        if symbol.isspace():
            pass

        elif symbol.isalpha():
            ident = ""
            while i < len(vyraz) and vyraz[i].isalpha():
                ident += vyraz[i]
                i += 1
            i -= 1
            yield [PREMENNA, ident]

        elif symbol in ['~', '&', '|']:
            yield [OPERATOR, symbol]

        elif symbol in ['=', '<']:
            token = '=>' if symbol == '=' else '<=>'

            # Technika lookahead pre viacznakové symboly
            if len(vyraz) - i >= len(token):
                if vyraz[i: i + len(token)] == token:
                    yield [OPERATOR, token]
            i += len(token) - 1

        elif symbol in ['(', ')']:
            yield [ZATVORKA, symbol]

        else:
            pass # Chyba neočakavaný token
        i += 1

def posledny(tokeny):
    if len(tokeny) < 1:
        return ''
    else:
        return tokeny[-1][1]

def shunting_yard(vyraz):
    fronta = []
    opzasobnik = []

    for lex in lex_nacitaj(vstup):
        if lex[0] == PREMENNA:
            fronta.append(lex)
            if posledny(opzasobnik) == '~':
                fronta.append(opzasobnik.pop())
        elif lex[0] == OPERATOR:
            opzasobnik.append(lex)
        elif lex[1] == '(':
            opzasobnik.append(lex)
        elif lex[1] == ')':
            while posledny(opzasobnik) != '(':
                fronta.append(opzasobnik.pop())
            opzasobnik.pop()

    for op in reversed(opzasobnik):
        fronta.append(op)
    return fronta

def tab_symbolov(rpn):
    symtab = []
    # Získa všetky premenné
    for i in range(len(rpn)):
        if rpn[i][0] == PREMENNA and rpn[i][1] not in symtab:
            symtab.append(rpn[i][1])
    symtab.sort()

    symdict = {symtab[i]: i for i in range(len(symtab))}
    for i in range(len(rpn)):
        if rpn[i][0] == PREMENNA:
            rpn[i] = [ODKAZ, symdict[rpn[i][1]]]

    print(rpn)
    n = 2 ** len(symtab)
    zmena = n // 2
    stav = True

    # Striedavo generuje 0/1 aby vycerpal vsetky kombinacie
    for i in range(len(symtab)):
        symtab[i] = [symtab[i], []]
        for o in range(n):
            if o % zmena == 0:
                stav = not stav
            symtab[i][1].append(stav)
        zmena //= 2
    return symtab

def v_not(A):
    return [not A[i] for i in range(len(A))]

def v_and(A, B):
    if len(A) == len(B):
        return [(A[i] and B[i]) for i in range(len(A))]

def v_or(A, B):
    if len(A) == len(B):
        return [(A[i] or B[i]) for i in range(len(A))]

def v_impl(A, B):
    if len(A) == len(B):
        return [((not A[i]) or B[i]) for i in range(len(A))]

def v_ekviv(A, B):
    if len(A) == len(B):
        return [(A[i] and B[i]) or (not A[i] and not B[i])
                for i in range(len(A))]

def vyries_logiku(rpn):
    var = []
    logickatab = tab_symbolov(rpn)
    # Okrem toho rpn -> refrpn
    for lex in rpn:
        if lex[0] == ODKAZ:
            var.append(lex[1])
        if lex[0] == OPERATOR:
            if lex[1] == '~':
                c = v_not(logickatab[var.pop()][1])

            elif lex[1] == '&':
                c = v_and(logickatab[var.pop()][1], logickatab[var.pop()][1])

            elif lex[1] == '|':
                print(var[-1], var[-2])
                c = v_or(logickatab[var.pop()][1], logickatab[var.pop()][1])

            elif lex[1] == '=>':
                op1 = var.pop()
                c = v_impl(logickatab[var.pop()][1], logickatab[op1][1])

            elif lex[1] == '<=>':
                c = v_ekviv(logickatab[var.pop()][1], logickatab[var.pop()][1])

            var.append(len(logickatab))
            logickatab.append([len(logickatab), c])
    return logickatab

def vytlac_stlpce(logtab):
    for i in logtab:
        print('|{:^10.10}'.format(str(i[0])), end="")
    print('|\n' + '-' * (12 * len(logtab)))

    for s in range(len(logtab[0][1])):
        for r in range(len(logtab)):
            print('|{:^10.10}'.format(str(int(logtab[r][1][s]))), end="")
        print('|')


vstup = input('> ')
rpn = shunting_yard(vstup)
print(rpn)
# print()
# t = tab_symbolov(rpn)
# print(t)
# print()
# print(rpn)
#print(t[0][1], t[1][1])
#print(v_and(t[0][1], t[1][1]))
#print(v_or(t[0][1], t[1][1]))
#print(v_impl(t[0][1], t[1][1]))
#print(v_ekviv(t[0][1], t[1][1]))
#print(v_not(t[0][1]))
vytlac_stlpce(vyries_logiku(rpn))
