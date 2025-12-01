import flet as ft
# Importamos tu nueva función desde el archivo excel_reader.py
# (Asegúrate de que excel_reader.py esté en la misma carpeta 'src')
from excel_reader import excelReader

def main(page: ft.Page):
    # --- Configuración de la Página ---
    page.title = "Evaluador de expresiones"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 600
    page.window.height = 700
    page.padding = 20

    selected_file_path = ft.Text(value="Ningún archivo seleccionado", color="grey")
    
    # --- Componentes de la Interfaz ---    
    header = ft.Text("Evaluador de expresiones, proyecto final", size=24, weight=ft.FontWeight.BOLD)

    results_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Expresión (Excel)")),
            ft.DataColumn(ft.Text("Resultado")),
        ],
        rows=[],
        border=ft.border.all(1, "grey"),
        vertical_lines=ft.border.all(1, "grey"),
        heading_row_color="lightblue",
        width=550,
    )    

    table_container = ft.Column( 
        controls=[results_table],
        scroll=ft.ScrollMode.ALWAYS,
        expand=True
    )

    # --- Manejadores de Eventos ---

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            path = e.files[0].path
            selected_file_path.value = path
            selected_file_path.color = "black"
            
            process_btn.disabled = False
            process_btn.update()
            selected_file_path.update()
        else:
            pass

    def on_process_click(e):
        path = selected_file_path.value
        print(f"Procesando archivo real: {path}")

        # 1. Limpiamos la tabla visual
        results_table.rows.clear()
        
        # 2. LLAMAMOS A TU FUNCIÓN DE EXCEL
        # Esto lee el archivo real seleccionado por el usuario
        lista_expresiones = excelReader(path)

        if not lista_expresiones:
            page.snack_bar = ft.SnackBar(ft.Text("El archivo está vacío o no se pudo leer."))
            page.snack_bar.open = True
            page.update()
            return

        # 3. Procesamos cada expresión leída
        for expresion in lista_expresiones:
            # --- AQUÍ IRÁ TU ANALIZADOR LÉXICO/SINTÁCTICO ---
            # Por ahora, simulamos el resultado poniendo "Pendiente"
            resultado_simulado = "Pendiente de evaluar" 
            
            # Agregamos la fila a la tabla con los datos reales del Excel
            results_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(expresion)), 
                    ft.DataCell(ft.Text(resultado_simulado))
                ])
            )

        results_table.update()
        page.snack_bar = ft.SnackBar(ft.Text(f"Se cargaron {len(lista_expresiones)} expresiones."))
        page.snack_bar.open = True
        page.update()

    # --- Configuración del FilePicker ---
    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    # --- Botones ---
    pick_file_btn = ft.ElevatedButton(
        "📁 Seleccionar Excel",
        on_click=lambda _: file_picker.pick_files(
            allow_multiple=False, 
            allowed_extensions=["xlsx", "xls"]
        )
    )

    process_btn = ft.ElevatedButton(
        "🔢 Evaluar Expresiones", 
        disabled=True,
        on_click=on_process_click
    )

    # --- Armado del Layout ---
    page.add(
        header,
        ft.Divider(),
        ft.Row([pick_file_btn, selected_file_path], alignment=ft.MainAxisAlignment.START),
        ft.Container(height=10),
        process_btn,
        ft.Divider(),
        ft.Text("Resultados:", weight=ft.FontWeight.BOLD),
        table_container
    )