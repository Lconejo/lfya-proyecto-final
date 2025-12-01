import flet as ft

# IMPORTANTE:
# Como main.py está DENTRO de la carpeta 'src', 
# debemos importar 'interfaz' directamente como un vecino, 
# SIN poner 'src.interfaz'.

try:
    from interfaz import main as iniciar_interfaz
except ImportError as e:
    # Si esto falla, imprimimos ayuda para depurar
    print(f"Error importando la interfaz: {e}")
    # Intento de fallback por si acaso se ejecuta desde fuera
    try:
        from src.interfaz import main as iniciar_interfaz
    except:
        raise e

if __name__ == "__main__":
    print("Iniciando aplicación desde src/main.py ...")
    ft.app(target=iniciar_interfaz)