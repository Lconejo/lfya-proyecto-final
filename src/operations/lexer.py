#Lexer con Ply
import ply.lex as lex

#      LISTA DE TOKENS
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'ABS',
    'SQRT',
    'EXP'
)

#   PALABRAS RESERVADAS 
reserved = {
    'abs': 'ABS',
    'sqrt': 'SQRT',
    'exp': 'EXP'
}

#     TOKENS SIMPLES
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

#    NÚMEROS 
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

#    IDENTIFICADORES
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Verificamos si es palabra reservada 
    t.type = reserved.get(t.value, 'ID')
    return t

#     IGNORAR ESPACIOS

t_ignore = ' \t'


#     MANEJO DE ERRORES

def t_error(t):
    print("Carácter ilegal:", t.value[0])
    t.lexer.skip(1)

#     CONSTRUIR EL LEXER

lexer = lex.lex()
