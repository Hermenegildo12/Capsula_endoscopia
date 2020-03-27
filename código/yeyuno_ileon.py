from limpieza import *
from alta_calidad import *
from funcion import *
import pandas as pd

# ¿Qué porcentaje de hallazgos de yeyuno e íleon existe?

#Esto es importante ya que ni la gastroscopia ni la colonoscopia son capaces de evaluar dichas porciones del tracto digestivo
#Para ver hallazgos, sin discriminar cuales son los más frecuentes miro la columnas
# de "Hz_yeuno" y la de "Hz_íleon" las cuales recogen sin discriminar el tipo.

#Uso la función definida anteriormente
hz_y=resumen(datos,"Hz_yeyuno",1,"=")
hz_i=resumen(datos,"Hz_íleon",1,"=")

#Las uno y limpio
oculto=pd.merge(hz_y, hz_i, on='unión')
oculto.drop(columns=["unión"],inplace=True)
oculto.index=['Cidma', 'Uruguay', 'Total']

# Calculo una nueva columna con el total en su conjunto
juntos=datos[(datos["Hz_yeyuno"]==1) & (datos["Hz_íleon"]==1)]
T_oculto=(oculto["Hz_yeyuno"]["Total"][0]+oculto["Hz_íleon"]["Total"][0])-len(juntos)
T_p_oculto=por(len(datos["Médico"]),T_oculto)

#Cuadro resumen de hallazgos yeyuno e íleon
oculto["Total"]=[[oculto["Hz_íleon"]["Total"][0],por(len(datos[datos["Médico"]==0]),oculto["Hz_íleon"]["Total"][0])],
                 [oculto["Hz_yeyuno"]["Uruguay"][0]+oculto["Hz_íleon"]["Uruguay"][0],por(len(datos[datos["Médico"]==1]),
                oculto["Hz_yeyuno"]["Uruguay"][0]+oculto["Hz_íleon"]["Uruguay"][0])],
                 [T_oculto,T_p_oculto]]

