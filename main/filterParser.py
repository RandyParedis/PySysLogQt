
from lark import Lark, Transformer
from main.Extra import RFACS, RLEVELS

RFACSL = {k.lower(): RFACS[k] for k in RFACS}

GRAMMAR = r'''
    WS      : /[ \t\f\r\n]/+
    %ignore WS
    
    ?start  : expr
    ?expr   : ("(" expr ")") | boolean | stmt | elm
    boolean : expr bop expr
    stmt    : elm op elm
    ?bop    : AND | OR
    ?op     : EQ | NE | LT | GT | LE | GE | IN
    elm     : (NOT expr) | TODAY | NOW | NUMBER | ESCAPED_STRING | LEVEL | FACILITY | FIELD
    
    AND     : "and"i | "&&"i
    OR      : "or"i | "||"i
    NOT     : "not"i | "!"i
    EQ      : "eq"i | "=="i | "is"i
    NE      : "ne"i | "!="i
    LT      : "lt"i | "<"i
    LE      : "le"i | "<="i
    GT      : "gt"i | ">"i
    GE      : "ge"i | ">="i
    IN      : "in"i
    TODAY   : "today"i
    NOW     : "now"i
    NUMBER  : /-?([1-9][0-9]*|0)(\.[0-9]*)?/
    FIELD   : /[a-zA-Z]+/
    LEVEL   : {}
    FACILITY: {}
    
    // Strings from LARK
    _STRING_INNER: /.*?/
    _STRING_ESC_INNER: _STRING_INNER /(?<!\\)(\\\\)*?/ 
    ESCAPED_STRING : "\"" _STRING_ESC_INNER "\""
'''.format(" | ".join(['"%s"i' % str(x).lower() for x in RLEVELS.keys()]),
           " | ".join(['"%s"i' % str(x).lower().replace(" ", "").replace("-", "") for x in RFACS.keys()]))

class TreeTransformer(Transformer):
    def __init__(self, visit_tokens, fields):
        super().__init__(visit_tokens)
        self.fields = fields

    NUMBER = float

    def FIELD(self, field):
        return self.fields.get(field.lower(), None)

    def AND(self, _):
        return 'and'

    def OR(self, _):
        return 'or'

    def NOT(self, _):
        return 'not'

    def EQ(self, _):
        return "=="

    def NE(self, _):
        return "!="

    def LT(self, _):
        return "<"

    def LE(self, _):
        return "<="

    def GT(self, _):
        return ">"

    def GE(self, _):
        return ">="

    def CONT(self, _):
        return "in"

    def LEVEL(self, val):
        return RLEVELS[val.upper()]

    def FACILITY(self, val):
        return RFACSL[val]

    def TODAY(self, _):
        import datetime
        return datetime.date.today()

    def NOW(self, _):
        import datetime
        return datetime.datetime.now().replace(microsecond=0).timestamp()

    def elm(self, inp):
        if len(inp) == 2:
            return not inp[1]
        return inp[0]

    def boolean(self, inp):
        return eval(" ".join([str(x) for x in inp]))

    def stmt(self, inp):
        return eval(" ".join([str(x) for x in inp]))

_parser = Lark(GRAMMAR, parser='earley')


def parse(s):
    return _parser.parse(s)


def check(tree, fields):
    try:
        return TreeTransformer(visit_tokens=True, fields=fields).transform(tree)
    except:
        return False

if __name__ == '__main__':
    import sys
    tree = parse(sys.argv[1])
    print(check(tree, {"id": 2, "level": "'CRITICAL'"}))

