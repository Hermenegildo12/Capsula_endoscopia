from  código.analisis import *
from código.limpieza import *

#Función: Recibe una columna de la base de datos y le suma los hallazgos de hernia de hiato totales
#Parámetros: fila: Columna donde poner la suma
def hernia (fila):
    a='Hernia_hiato_esof'
    b='Hernia_hiato_estom'
    if fila[a]==fila[b]:
        return fila[a]
    elif fila[a]<fila[b]:
        return fila[b]
    else:
        return fila[a]

