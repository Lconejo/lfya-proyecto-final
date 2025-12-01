import flet as ft

# Intentamos importar las funciones necesarias
try:
    from src.excel_reader import excelReader
    from src.parser import evaluar_expresion
except ImportError:
    # Fallback si estás ejecutando desde dentro de la carpeta src
    from excel_reader import excelReader
    from parser import evaluar_expresion

def main(page: ft.Page):
    # --- Configuración Inicial ---
    page.title = "Evaluador de expresiones"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 700
    page.window.height = 800
    page.padding = 20

    # Variable de estado para el path
    selected_file_path = ft.Text("Ningún archivo seleccionado", color="grey")

    # --- Elementos UI ---
    header = ft.Text("Evaluador de expresiones", size=24, weight="bold")
    
    # Tabla de resultados
    results_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Entrada (Excel)")),
            ft.DataColumn(ft.Text("Resultado parser")),
        ],
        rows=[],
        border=ft.border.all(1, "grey"),
        vertical_lines=ft.border.all(1, "grey"),
        heading_row_color=ft.Colors.BLUE_50,
        expand=True
    )
    
    # Contenedor con scroll para la tabla
    table_container = ft.Column(
        controls=[results_table], 
        scroll=ft.ScrollMode.AUTO, 
        expand=True
    )

    # --- Funciones Lógicas ---
    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            path = e.files[0].path
            selected_file_path.value = path
            selected_file_path.color = "black"
            process_btn.disabled = False # Habilitar botón
            page.update()

    def on_process_click(e):
        path = selected_file_path.value
        results_table.rows.clear()
        
        # 1. Leer Excel
        datos = excelReader(path)
        
        if not datos:
            page.snack_bar = ft.SnackBar(ft.Text("Archivo vacío o error de lectura"))
            page.snack_bar.open = True
            page.update()
            return

        errores = 0
        
        # 2. Procesar cada dato (AQUÍ ES DONDE OCURRE LA MAGIA)
        for expr in datos:
            res_texto = ""
            color = "black"
            
            try:
                # --- AQUÍ LLAMAMOS A TU PARSER ---
                val = evaluar_expresion(expr)
                
                # Formateo si es float
                if isinstance(val, float):
                    res_texto = f"{val:.4f}"
                else:
                    res_texto = str(val)
                    
            except Exception as error:
                # Captura errores de sintaxis o matemáticos
                res_texto = f"Error: {error}"
                color = "red"
                errores += 1
            
            # Agregar fila
            results_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(expr)),
                    ft.DataCell(ft.Text(res_texto, color=color))
                ])
            )

        results_table.update()

        # Feedback final
        msg = "¡Proceso terminado!" if errores == 0 else f"Terminado con {errores} errores."
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

    # --- Configuración de Controles ---
    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    pick_btn = ft.ElevatedButton(
        "Cargar Excel", 
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(allowed_extensions=["xlsx", "xls"])
    )

    process_btn = ft.ElevatedButton(
        "Ejecutar análisis", 
        icon=ft.Icons.PLAY_ARROW,
        disabled=True,
        on_click=on_process_click
    )

    # --- Layout Final ---
    page.add(
        header,
        ft.Divider(),
        ft.Row([pick_btn, selected_file_path], alignment="start"),
        ft.Container(height=10),
        process_btn,
        ft.Divider(),
        ft.Text("Resultados del Análisis:", size=16, weight="bold"),
        table_container
    )