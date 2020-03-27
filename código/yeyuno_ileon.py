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

c_vision_del=len(datos[((datos["No_evaluable_del"]==0)& (datos['No_informado_del']==0)) &
                     ((datos['Médico']==0)) ])
u_vision_del=len(datos[((datos["No_evaluable_del"]==0)& (datos['No_informado_del']==0)) &
                     ((datos['Médico']==1)) ])

c_vision_del_por=por(len(datos[datos["Médico"]==0]),c_vision_del)
u_vision_del_por=por(len(datos[datos["Médico"]==1]),u_vision_del)

print("El intestino delgado se visualizo e informo en {} pacientes, equivaliendo al {}% del total".format(c_vision_del,u_vision_del_por))

oculto["Evaluado e informado "]= [[c_vision_del,c_vision_del_por],
                                  [u_vision_del, u_vision_del_por],[c_vision_del+u_vision_del,
                                por(len(datos),c_vision_del+u_vision_del)]]

#Resultado yeyuno e íleon
#Como se ve en la tabla, CIDMA en el hallazgo de esa zona en conjunto tiene un 10% mas de hallazgos
# frente al hospital Italiano. Lo que puede deberse a que en este último suele usarse la cápsula COLON2 con el modo por defecto,
# lo cual programa la cápsula para que se apague hasta llegar al colon,
