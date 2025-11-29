import flet as ft

# Este archivo solo contiene la definición de la interfaz y su lógica.
# No ejecutamos 'ft.app' aquí directamente, sino que exportamos la función 'main_interfaz'.

def main_interfaz(page: ft.Page):
    # --- Configuración de la Página ---
    page.title = "Evaluador de expresiones"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 600
    page.window.height = 700
    page.padding = 20

    selected_file_path = ft.Text(value="Ningún archivo seleccionado", color="grey")
    
    # --- Componentes de la Interfaz ---    
    # 1. Título
    header = ft.Text("Evaluador de expresiones, proyecto final", size=24, weight=ft.FontWeight.BOLD)

    # 2. Tabla de Resultados
    results_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Expresión (Columna A)")),
            ft.DataColumn(ft.Text("Resultado Evaluado")),
        ],
        rows=[],
        border=ft.border.all(1, "grey"),
        vertical_lines=ft.border.all(1, "grey"),
        heading_row_color="lightblue",
        width=550,
    )    

    # Contenedor con scroll
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
        print(f"Procesando archivo: {path}")

        # --- SIMULACIÓN ---
        results_table.rows.clear()
        datos_simulados = [ 
            ("5 + 5", "10"),
            ("SQRT(16)", "4"),
            ("2 * (3 + 2)", "10"),
        ]
        
        for expr, res in datos_simulados:
            results_table.rows.append(
                ft.DataRow(cells=[ft.DataCell(ft.Text(expr)), ft.DataCell(ft.Text(res))])
            )

        results_table.update()
        page.snack_bar = ft.SnackBar(ft.Text("¡Evaluación completada!"))
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