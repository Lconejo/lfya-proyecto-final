import flet as ft

def main(page: ft.Page):
    # --- Configuración de la Página ---
    page.title = "Evaluador de expresiones" # Título de la ventana
    page.theme_mode = ft.ThemeMode.LIGHT # Modo claro
    page.window.width = 600 # Ancho de la ventana
    page.window.height = 700 # Alto de la ventana
    page.padding = 20 # Padding alrededor del contenido

    selected_file_path = ft.Text(value="Ningún archivo seleccionado", color="grey") # Muestra la ruta del archivo seleccionado
    
    # --- Componentes de la Interfaz ---    
    # 1. Título
    header = ft.Text("Evaluador de expresiones, proyecto final", size=24, weight=ft.FontWeight.BOLD)

    # 2. Tabla de Resultados
    results_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Expresión (Columna A)")), # Columna A
            ft.DataColumn(ft.Text("Resultado Evaluado")), # Columna de resultados evaluados, aquí va la lógica
        ],
        rows=[], # Filas vacías al inicio
        border=ft.border.all(1, "grey"), # Borde de la tabla
        vertical_lines=ft.border.all(1, "grey"), # Líneas verticales
        heading_row_color="lightblue", # Color de la fila de encabezado
        width=550, # Ancho de la tabla
    )    

    # Contenedor con scroll por si el Excel es muy largo
    table_container = ft.Column( 
        controls=[results_table],
        scroll=ft.ScrollMode.ALWAYS,
        expand=True
    )

    # --- Manejadores de Eventos ---

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files: # Si el usuario selecciona un archivo
            path = e.files[0].path # Tomamos la ruta del primer archivo
            selected_file_path.value = path # Actualizamos el texto con la ruta
            selected_file_path.color = "black" # Cambiamos el color para indicar que hay archivo
            
            # Habilitar el botón de procesar si ya hay archivo
            process_btn.disabled = False # Habilitar el botón
            process_btn.update() # Actualizar el botón
            selected_file_path.update() # Actualizar el texto con la ruta
        else:
            # Si el usuario cancela
            pass

    def on_process_click(e):
        # --- AQUÍ VA LA LÓGICA DE PROCESAMIENTO --- #
        # Por ahora, simularemos que carga datos para ver que la UI funciona.
        
        path = selected_file_path.value
        print(f"Procesando archivo: {path}") # Debug en consola

        # --- SIMULACIÓN --- #
        # DESPUÉS YA SE LE PONEN LOS CÁLCULOS REALES AQUÍ #
        results_table.rows.clear() # Limpiamos filas anteriores
        datos_simulados = [ 
            ("5 + 5", "10"),
            ("SQRT(16)", "4"),
            ("2 * (3 + 2)", "10"),
        ]
        
        for expr, res in datos_simulados: # Agregamos filas simuladas
            results_table.rows.append( # Agregar fila a la tabla
                ft.DataRow(cells=[ft.DataCell(ft.Text(expr)), ft.DataCell(ft.Text(res))]) # Celda con expresión y resultado
            )
        # ------------------------------------------------------

        results_table.update() # Actualizamos la tabla para mostrar resultados
        page.snack_bar = ft.SnackBar(ft.Text("¡Evaluación completada!")) # Mensaje de éxito
        page.snack_bar.open = True # Mostrar el SnackBar
        page.update() # Actualizar la página para reflejar cambios iniciales

    # --- Configuración del FilePicker ---
    file_picker = ft.FilePicker(on_result=on_file_picked) # Manejador de selección de archivo
    page.overlay.append(file_picker) # Agregar el FilePicker a la página

    # --- Botones ---
    pick_file_btn = ft.ElevatedButton(
        "📁 Seleccionar Excel",
        on_click=lambda _: file_picker.pick_files( # Abrir diálogo de selección de archivo
            allow_multiple=False,  # Solo un archivo
            allowed_extensions=["xlsx", "xls"] # Filtramos solo Excel
        )
    )

    process_btn = ft.ElevatedButton( # Botón para procesar el archivo
        "🔢 Evaluar Expresiones", 
        disabled=True, # Deshabilitado hasta que elijan archivo
        on_click=on_process_click # Manejador de clics
    )

    # --- Armado del Layout ---
    page.add(
        header,
        ft.Divider(), # Separador
        ft.Row([pick_file_btn, selected_file_path], alignment=ft.MainAxisAlignment.START), # Fila con botón y ruta del archivo
        ft.Container(height=10), # Espaciador
        process_btn, # Botón de procesar
        ft.Divider(), # Separador
        ft.Text("Resultados:", weight=ft.FontWeight.BOLD), # Título de resultados
        table_container # Contenedor de la tabla con scroll
    )

ft.app(target=main)