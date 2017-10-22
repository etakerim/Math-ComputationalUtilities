#TODO redukovanie prázdnych listov / shunting yard

class Uzol:
    OPERATOR = 'op'
    PREMENNA = 'var'
    ODKAZ    = 'ref'
    def __init__(self, lex=None, lavy=None, pravy=None):
        self.lex = lex
        self.negacia = False
        self.lavy = lavy
        self.pravy = pravy
        self.otec = None

    def pridaj_list(self, data=None):
        syn = Uzol(lex=data)

        if self.lavy == None:
            self.lavy = syn
            return self.lavy

        elif not self.lavy.lex and self.lavy.negacia:
            self.lavy.lex = data
            return self.lavy

        elif self.pravy == None:
            self.pravy = syn
            return self.pravy

        elif not self.pravy.lex and self.pravy.negacia:
            self.pravy.lex = data
            return self.pravy

    def __repr__(self):
        if self.negacia:
            return repr(self.lex) + '~'
        else:
            return repr(self.lex)


def vypis(koren, spc=0):
    print("{}-{}".format(' ' * spc, koren))
    spc += 2
    if koren.lavy != None:
        vypis(koren.lavy, spc)
    if koren.pravy != None:
        vypis(koren.pravy, spc)


def parser(koren, vyraz):
    i = 0
    while i < len(vyraz):
        symbol = vyraz[i]

        if symbol.isspace():
            pass

        elif symbol == '(':
            tmp = koren.pridaj_list()
            tmp.otec = koren
            koren = tmp

        elif symbol == ')':
            koren = koren.otec

        elif symbol == '~':
            tmp = koren.pridaj_list()
            tmp.negacia = True

        elif symbol in ['&', '|']:
            # Ak uz je obsadene syntax error
            koren.lex = [koren.OPERATOR, symbol]

        elif symbol in ['=', '<']:
            token = '=>' if symbol == '=' else '<=>'

            # Technika lookahead pre viacznakové symboly
            if len(vyraz) - i >= len(token):
                if vyraz[i: i + len(token)] == token:
                    koren.lex = [koren.OPERATOR, token]
            i += len(token) - 1

        elif symbol.isalpha():
            koren.pridaj_list([koren.PREMENNA, symbol])
            # Syntax chyba(priveľa sym)
        else:
            pass # Chyba neočakavaný token
        i += 1

vstup = input('> ')
strom = Uzol()
parser(strom, vstup)
vypis(strom)
# Čo ak A & B | C - zavádzajúce poradie


