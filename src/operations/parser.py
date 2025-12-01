#Parser con Ply
import ply.yacc as yacc
from lexer import tokens  # Importa los tokens desde el lexer
import math

#   REGLAS DE PRECEDENCIA
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

#     REGLAS DEL PARSER

def p_expression_binop(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
    '''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_expression_group(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    p[0] = p[2]

def p_expression_number(p):
    '''
    expression : NUMBER
    '''
    p[0] = p[1]

def p_expression_uminus(p):
    '''
    expression : MINUS expression %prec UMINUS
    '''
    p[0] = -p[2]

def p_expression_abs(p):
    '''
    expression : ABS LPAREN expression RPAREN
    '''
    p[0] = abs(p[3])

def p_expression_sqrt(p):
    '''
    expression : SQRT LPAREN expression RPAREN
    '''
    p[0] = math.sqrt(p[3])

def p_expression_exp(p):
    '''
    expression : EXP LPAREN expression RPAREN
    '''
    p[0] = math.exp(p[3])

def p_error(p):
    print("Error de sintaxis en:", p)

#     CONSTRUIR EL PARSER
parser = yacc.yacc()

#      PRUEBAS RÁPIDAS
if __name__ == "__main__":
    while True:
        try:
            s = input("expr > ")
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print("Resultado:", result)
