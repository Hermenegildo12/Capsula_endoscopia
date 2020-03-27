from código.analisis import *
from código.funcion import *
import pandas as pd
import numpy as np
import operator
import matplotlib.pyplot as plt
import seaborn as sns
import math

# Importo la base de datos de los pacientes, recogida en SPSS y pasada posteriormente a documento csv. Para su analisis
datos = pd.read_csv("../Analisis_ano.csv", sep=";")
datos.head()
datos.shape
datos.dtypes[:]
columnas = datos.columns

# Como se ve no hay ninguna variable, con valores nulos en toda la base de datos
incompletas = []
for e in columnas:
    if datos[e].isnull().sum() >= 1:
        incompletas.append(e)
columnas = datos.columns

# Borro la variable Dianoscitos porque sería un hallazgo compatible con la normalidad.
datos.drop(columns=['Dianocitos'], axis=0, inplace=True)

# Uno en una única variable las hernias de hiato de esófago y estomago. Al ser el mismo diagnostico, simplemente puesto
# en esófago o estomago según el momento de la cápsula en el que se diagnosticaba.
# Quedando unificada en la variable "Hernia_hiato_total"
datos["Hernia_hiato_total"]=datos.apply(lambda fila: hernia(fila), axis=1)

comp=datos[['Hernia_hiato_esof','Hernia_hiato_estom',"Hernia_hiato_total"]].sort_values(by="Hernia_hiato_total"),
ascending=True
