import flet as ft
from interfaz import main_interfaz as interfaz

if __name__ == "__main__":
    # Al estar dentro de src, recuerda ejecutarlo desde la terminal
    # estando en la raíz del proyecto con: python src/main.py
    ft.app(target=interfaz)