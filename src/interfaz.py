# Importar la librería Flet para crear la interfaz gráfica
import flet as ft

# Este archivo solo contiene la definición de la interfaz y su lógica.

def main_interfaz(page: ft.Page): # Función principal que crea y configura la interfaz gráfica
    # --- CONFIGURACIÓN DE LA PÁGINA ---
    # Establecer el título de la ventana de la aplicación
    page.title = "Evaluador de expresiones"    
    # Establecer el tema de la aplicación en modo claro (blanco)
    page.theme_mode = ft.ThemeMode.LIGHT    
    # Establecer el ancho de la ventana a 600 píxeles
    page.window.width = 600    
    # Establecer el alto de la ventana a 700 píxeles
    page.window.height = 700    
    # Establecer el espaciado interno de la página a 20 píxeles
    page.padding = 20    
    # Crear un widget de texto que muestra la ruta del archivo seleccionado, inicialmente en gris
    selected_file_path = ft.Text(value="Ningún archivo seleccionado", color="grey")    
    # - - - - - - - - - - - - - - #


    # --- COMPONENTES DE LA INTERFAZ ---   
    # 1. Crear un encabezado/título para la aplicación
    header = ft.Text("Evaluador de expresiones, proyecto final", size=24, weight=ft.FontWeight.BOLD)

    # 2. Crear una tabla de resultados con dos columnas: expresión y resultado evaluado
    results_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Expresión (Columna A)")),  # Primera columna: Expresión
            ft.DataColumn(ft.Text("Resultado evaluado")),  # Segunda columna: Resultado
        ],
        rows=[],  # Inicialmente sin filas de datos
        border=ft.border.all(1, "grey"),  # Borde gris de 1 píxel alrededor de la tabla
        vertical_lines=ft.border.all(1, "grey"),  # Líneas verticales grises entre columnas
        heading_row_color="lightblue",  # Color del encabezado en azul claro
        width=550,  # Ancho de la tabla
    )    

    # Crear un contenedor (columna) con scroll para la tabla, permitiendo desplazamiento vertical
    table_container = ft.Column( 
        controls=[results_table],  # Agregar la tabla como control
        scroll=ft.ScrollMode.ALWAYS,  # Habilitar scroll siempre
        expand=True  # Expandir para ocupar espacio disponible
    )
    # - - - - - - - - - - - - - - #

    # --- MANEJADORES DE EVENTOS ---
    # Definir función manejadora que se ejecuta cuando se selecciona un archivo
    def on_file_picked(e: ft.FilePickerResultEvent):
        # Verificar si se seleccionó algún archivo
        if e.files:
            # Obtener la ruta del primer archivo seleccionado
            path = e.files[0].path
            # Actualizar el widget de texto con la ruta del archivo
            selected_file_path.value = path
            # Cambiar el color del texto a negro para indicar que hay un archivo seleccionado
            selected_file_path.color = "black"
            
            # Habilitar el botón de procesamiento (antes estaba deshabilitado)
            process_btn.disabled = False
            # Actualizar visualmente el botón en la interfaz
            process_btn.update()
            # Actualizar visualmente el widget de texto de la ruta
            selected_file_path.update()
        else:
            # Si no se selecciona archivo, no hacer nada
            pass

    # Definir función manejadora que se ejecuta cuando se hace clic en el botón de procesar
    def on_process_click(e):
        # Obtener la ruta del archivo desde el widget de texto
        path = selected_file_path.value
        # Mostrar en consola que se está procesando el archivo
        print(f"Procesando archivo: {path}")

        # --- SIMULACIÓN ---
        # Limpiar todas las filas existentes en la tabla de resultados
        results_table.rows.clear()
        # Crear datos simulados con pares (expresión, resultado)
        # Estos son ejemplos de prueba, no son reales
        datos_simulados = [ 
            ("5 + 5", "10"),  # Expresión: 5 + 5, Resultado: 10
            ("SQRT(16)", "4"),  # Expresión: SQRT(16), Resultado: 4
            ("2 * (3 + 2)", "10"),  # Expresión: 2 * (3 + 2), Resultado: 10
        ]
        
        # Iterar sobre cada par de expresión y resultado en los datos simulados
        for expr, res in datos_simulados:
            # Crear una fila de la tabla con dos celdas: expresión y resultado
            results_table.rows.append(
                ft.DataRow(cells=[ft.DataCell(ft.Text(expr)), ft.DataCell(ft.Text(res))])
            )

        # Actualizar la tabla visualmente para mostrar las nuevas filas
        results_table.update()
        # Crear una notificación (snackbar) para informar que se completó la evaluación
        page.snack_bar = ft.SnackBar(ft.Text("¡Evaluación completada!"))
        # Mostrar la notificación
        page.snack_bar.open = True
        # Actualizar la página para mostrar los cambios
        page.update()

    # --- Configuración del FilePicker ---
    # Crear un selector de archivos que ejecuta on_file_picked cuando se selecciona un archivo
    file_picker = ft.FilePicker(on_result=on_file_picked)
    # Agregar el selector de archivos a la capa de superposición de la página
    page.overlay.append(file_picker)

    # --- Botones ---
    # Crear botón para seleccionar archivo Excel
    # Al hacer clic, abre el diálogo de selección de archivos
    pick_file_btn = ft.ElevatedButton(
        "📁 Seleccionar Excel",  # Texto del botón con emoji
        on_click=lambda _: file_picker.pick_files(  # Ejecutar pick_files cuando se haga clic
            allow_multiple=False,  # No permitir seleccionar múltiples archivos
            allowed_extensions=["xlsx", "xls"]  # Solo permitir archivos Excel
        )
    )

    # Crear botón para procesar/evaluar las expresiones
    process_btn = ft.ElevatedButton(
        "🔢 Evaluar Expresiones",  # Texto del botón con emoji
        disabled=True,  # Inicialmente deshabilitado (se habilita cuando se selecciona archivo)
        on_click=on_process_click  # Ejecutar on_process_click cuando se haga clic
    )

    # --- Armado del Layout ---
    # Agregar todos los componentes a la página en orden vertical
    page.add(
        header,  # Agregar el título
        ft.Divider(),  # Agregar una línea divisoria
        ft.Row([pick_file_btn, selected_file_path], alignment=ft.MainAxisAlignment.START),  # Fila con botón y ruta
        ft.Container(height=10),  # Contenedor vacío de 10 píxeles para espaciado
        process_btn,  # Agregar botón de procesamiento
        ft.Divider(),  # Agregar otra línea divisoria
        ft.Text("Resultados:", weight=ft.FontWeight.BOLD),  # Agregar etiqueta "Resultados"
        table_container  # Agregar el contenedor con la tabla de resultados
    )