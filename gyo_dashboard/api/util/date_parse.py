import re

class DateParse(object):

    tokens = [
        ('NUMBER', r"^[1-9]\d*"),
        ('PERIOD', r"[MHDW]")
        ('WRONG', r".") # wrong character
    ]

    Token = namedtuple('Token', ['typ', 'val', 'column'])

    def __init__(self):
        self.token_rgx = '|'.join('(?P<%s>%s)' % named_group for named_group in self.tokens)

    def tokenize(self, tag):
        col_num = 0

        for match_obj in re.finditer(self.token_rgx, tag):
            kind = match_obj.lastgroup
            value = match_obj.group(kind)
            if kind == 'MISMATCH':
                raise ValueError('Unexpected character sequence %s, did you forget quotes around string literal?' % value)
            else:
                column = match_obj.start() - col_num
                yield self.Token(kind, value, column)
