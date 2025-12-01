#En este archivo se abre el excel con las operaciones y se manejan los datos
import openpyxl 
from interfaz import path #supongamos que ya tenemos el path
#Abriremos el archivo usando el Path que se solicitó en la interfaz

def excelReader(path : str) -> list:

    #intentamos abrir el archivo
    try:
        workBook = openpyxl.load_workbook(path)
        sheet = workBook.active
    
    except Exception as e:
        print(f"Error al intentar abrir el archivo . . .: \n {e}")
        return []
    
    contenido = [] #Aquí guardaremos las expresiones de la celda

    for row in sheet.iter_rows(min_row=1, max_col=1):
        for cell in row:
            if cell.value is not None:
                contenido.append(cell.value.lower())
    
    workBook.close()
    return contenido 