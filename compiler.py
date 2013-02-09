# -*- coding: utf-8 -*-
import unicodedata
import yaml

from pyparsing import *

from expr import *

def isUnicodeAlphanum(ch):
    return unicodedata.category(ch)[0] in {'N', 'L'}

def isUnicodeNum(ch):
    return unicodedata.category(ch)[0] == 'N'

alphanum = u''.join(filter(isUnicodeAlphanum,
    map(unichr,xrange(65536))))

num = u''.join(filter(isUnicodeNum,
    map(unichr,xrange(65536))))

# Маркеры
name   = Word(alphanum)
number = Word(num)

comment  = '#' + restOfLine

LP = Suppress('(')
RP = Suppress(')')
CM = Suppress(',')
EQ = Suppress('=')

# Парсер
expr    =  Forward()
factor  =  name | Group(LP + expr + RP)
fact1   =  Group(Optional('!') + factor)
term    =  Group(fact1 + ZeroOrMore( (oneOf("&") + fact1 )))
expr    << Group(term + ZeroOrMore( (oneOf("|") + term )))

tbf_head = name + Optional(LP+number + Optional(CM+number)+RP)
tbf      = Group(tbf_head + EQ + expr ^ Suppress(lineEnd | comment))

tbf_file = ZeroOrMore(tbf) + StringEnd()

class DuplicationNameError(Exception):
    pass

def compileModuleDefs(sourceText, exports):
    namespace = exports

    def compileExpr(body):
        if type(body) == str:
            return namespace[body]
        elif len(body) == 1:
            return compileExpr(body[0])
        elif len(body) == 2 and body[0] == '!':
            return Not(compileExpr(body[1]))
        elif len(body) == 3 and body[1] == '|':
            or_op = Or()
            or_op.add_operand(compileExpr(body[0]))
            or_op.add_operand(compileExpr(body[2]))
            return or_op
        elif len(body) == 3 and body[1] == '&':
            and_op = And()
            and_op.add_operand(compileExpr(body[0]))
            and_op.add_operand(compileExpr(body[2]))
            return and_op
        else:
            raise SyntaxError(body)

    ast_list = filter(lambda ast: len(ast) > 0, tbf_file.parseString(sourceText))
    for ast in ast_list:
        head = ast[:-1]
        if len(head) < 3:
            for i in range(3-len(head)):
                head.append('0')
        elif len(head) > 3:
            raise SyntaxError("len(tbf_head) > 3")
        tbf_name = head[0]
        if tbf_name in namespace:
            raise DuplicationNameError(tbf_name)
        namespace[tbf_name] = TimedValue(
                                int(head[1]),
                                int(head[2]))
    for ast in ast_list:
        compileExpr(ast[-1]).subscribe(namespace[tbf_name])
    return namespace
