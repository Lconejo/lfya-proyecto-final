import ply.yacc as yacc
import math

# --- IMPORTACIÓN DE TOKENS ---
# Esta lógica permite que el parser encuentre el lexer sin importar
# si ejecutas el código desde la carpeta raíz o desde src.
try:
    from src.lexer import tokens
except ImportError:
    try:
        from lexer import tokens
    except ImportError:
        from .lexer import tokens

# --- REGLAS DE PRECEDENCIA ---
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

# --- REGLAS GRAMATICALES ---

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
        if p[3] == 0:
            raise ValueError("División por cero")
        p[0] = p[1] / p[3]

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = p[1]

def p_expression_uminus(p):
    '''expression : MINUS expression %prec UMINUS'''
    p[0] = -p[2]

def p_expression_abs(p):
    '''expression : ABS LPAREN expression RPAREN'''
    p[0] = abs(p[3])

def p_expression_sqrt(p):
    '''expression : SQRT LPAREN expression RPAREN'''
    if p[3] < 0:
        raise ValueError("Raíz negativa")
    p[0] = math.sqrt(p[3])

def p_expression_exp(p):
    '''expression : EXP LPAREN expression RPAREN'''
    p[0] = math.exp(p[3])

# --- MANEJO DE ERRORES ---
def p_error(p):
    if p:
        # Lanzamos error para que la interfaz lo detecte y pinte rojo
        raise SyntaxError(f"Error de sintaxis en token '{p.value}'")
    else:
        raise SyntaxError("Error de sintaxis: Entrada incompleta")

# --- CONSTRUCCIÓN DEL PARSER ---
parser = yacc.yacc()

# --- FUNCIÓN PÚBLICA (ESTA ES LA QUE FALTABA) ---
def evaluar_expresion(cadena):
    """
    Recibe una cadena (ej: '5 + 5') y retorna el resultado numérico.
    Es la función que llama 'interfaz.py'.
    """
    if not cadena: 
        return ""
    # Reiniciamos el parser para evitar conflictos
    return parser.parse(cadena)