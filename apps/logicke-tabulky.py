from collections import namedtuple

OPERATOR = 'op'
PREMENNA = 'var'
ODKAZ = 'ref'
ZATVORKA = 'par'
NOT = '~'
AND = '&'
OR = '|'
IMPL = '=>'
EKV = '<=>'
OTV_ZATVORKA = '('
ZAT_ZATVORKA = ')'

Token = namedtuple('Token', ['typ', 'lexem'])
TabStlpec = namedtuple('TabStlpec', ['nadpis', 'vektor'])


def token_nacitaj(vyraz):
    i = 0
    while i < len(vyraz):
        symbol = vyraz[i]

        if symbol.isspace():
            pass

        elif symbol.isalpha():
            ident = ''
            while i < len(vyraz) and vyraz[i].isalpha():
                ident += vyraz[i]
                i += 1
            i -= 1
            yield Token(PREMENNA, ident)

        elif symbol in [NOT, AND, OR]:
            yield Token(OPERATOR, symbol)

        elif symbol in [IMPL[0], EKV[0]]:
            lex = IMPL if symbol == IMPL[0] else EKV

            # Technika lookahead pre viacznakové symboly
            if len(vyraz) - i >= len(lex):
                if vyraz[i: i + len(lex)] == lex:
                    yield Token(OPERATOR, lex)
            i += len(lex) - 1

        elif symbol in [OTV_ZATVORKA, ZAT_ZATVORKA]:
            yield Token(ZATVORKA, symbol)

        else:
            pass   # Chyba neočakavaný token
        i += 1


def posledny(token):
    if len(token) < 1:
        return ''
    else:
        return token[-1].lexem


def shunting_yard(vyraz):
    fronta = []
    opzasobnik = []

    for token in token_nacitaj(vstup):
        if token.typ == PREMENNA:
            fronta.append(token)
            while posledny(opzasobnik) == NOT:
                fronta.append(opzasobnik.pop())

        elif token.typ == OPERATOR:
            opzasobnik.append(token)

        elif token.lexem == OTV_ZATVORKA:
            opzasobnik.append(token)

        elif token.lexem == ZAT_ZATVORKA:
            while posledny(opzasobnik) != OTV_ZATVORKA:
                fronta.append(opzasobnik.pop())
            opzasobnik.pop()

    for op in reversed(opzasobnik):
        fronta.append(op)

    return fronta


def tabulka_symbolov(rpn):
    symtab = []
    # Získa všetky premenné
    for i in range(len(rpn)):
        if rpn[i].typ == PREMENNA and rpn[i].lexem not in symtab:
            symtab.append(rpn[i].lexem)
    symtab.sort()

    # Nahradí ich symbolickými odkazmi na stlpce v tabulke symbolov
    symdict = {symtab[i]: i for i in range(len(symtab))}
    for i in range(len(rpn)):
        if rpn[i].typ == PREMENNA:
            rpn[i] = Token(ODKAZ, symdict[rpn[i].lexem])

    n = 2 ** len(symtab)
    zmena = n // 2
    stav = True

    # Striedavo generuje 0/1 aby vycerpal vsetky kombinacie
    for i in range(len(symtab)):
        symtab[i] = TabStlpec(symtab[i], [])
        for o in range(n):
            if o % zmena == 0:
                stav = not stav
            symtab[i].vektor.append(stav)
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


def v_ekv(A, B):
    if len(A) == len(B):
        return [(A[i] and B[i]) or (not A[i] and not B[i])
                for i in range(len(A))]


def vyries_logiku(rpn):
    var = []
    logickatab = tabulka_symbolov(rpn)
    # Okrem toho rpn -> refrpn

    for lex in rpn:
        if lex.typ == ODKAZ:
            var.append(lex.lexem)

        elif lex.typ == OPERATOR:
            op2_i = var.pop()
            op2 = logickatab[op2_i].vektor
            if lex.lexem == NOT:
                c = v_not(op2)
                fmt = '{}{}'.format(NOT, logickatab[op2_i].nadpis)
            else:
                op1_i = var.pop()
                op1 = logickatab[op1_i].vektor
                if lex.lexem == AND:
                    c = v_and(op1, op2)

                elif lex.lexem == OR:
                    c = v_or(op1, op2)

                elif lex.lexem == IMPL:
                    c = v_impl(op1, op2)

                elif lex.lexem == EKV:
                    c = v_ekv(op1, op2)
                fmt = '({} {} {})'.format(logickatab[op1_i].nadpis, lex.lexem,
                                          logickatab[op2_i].nadpis)

            var.append(len(logickatab))
            logickatab.append(TabStlpec(fmt, c))

    return logickatab


def horiz_oddelovac(sirka, n_stlpcov):
    tabsirka = (sirka + 1) * n_stlpcov - 1
    print('|' + '-' * tabsirka + '|')


def vytlac_stlpce(logtab):
    # Napíše číslovanú hlavičku
    n_stlpcov = len(logtab)

    horiz_oddelovac(6, n_stlpcov)
    for i in range(n_stlpcov):
        print('|{:^6.6}'.format(str(i)), end="")
    print('|')
    horiz_oddelovac(6, n_stlpcov)

    # Napíše do stĺpcov logické hodnoty
    for s in range(len(logtab[0].vektor)):
        for r in range(n_stlpcov):
            print('|{:^6.6}'.format(str(int(logtab[r].vektor[s]))), end="")
        print('|')
    horiz_oddelovac(6, n_stlpcov)

    # Napíše legendu k číslovaným stĺpcom
    print('\n-------Legenda--------')
    for i, stlpec in enumerate(logtab):
        print('{:6.6} | {}'.format(str(i), stlpec.nadpis))


if __name__ == '__main__':
    vstup = input('> ')
    rpn = shunting_yard(vstup)
    vytlac_stlpce(vyries_logiku(rpn))
