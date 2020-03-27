from limpieza import *
from alta_calidad import *
import pandas as pd

# Calidad de los informes

#Quiero saber de que calidad de datos globales disponemos,
# por si es suficientemente buena como para afirmar que es una buena ayuda al diagnóstico del tracto digestivo.

#Unifico en una única variable, todas las columnas que reflejen la capacidad de evaluar las distintas áeras del
#tracto GI, tomando los siguietes valores:
# 0: No tiene zonas NO evaluadas. Es decir TODO ha sido evaluado
# 1-4 según la cantidad de zonas no evaluadas

datos["No evaluación completa"] = datos[no_evaluable].sum(axis=1)

eva_comp=datos[datos["No evaluación completa"]==0]

#Paso las columnas por la función
a=resumen(datos,"Calidad_preparación",2,">")
b=resumen(datos,"Burbujas",1,"=")
c=resumen(datos,'No evaluación completa',0,"=")
d=resumen(datos,'No_info',0,"=")
e=resumen(datos,'Básico',4,">")
f=resumen(datos,'Recto',1,"=")

#Unifico en una única tabla usando como enlace la columna unión
union=pd.merge(a, b, on='unión')
union=pd.merge(union,c,on='unión')
union=pd.merge(union,d,on='unión')
union=pd.merge(union,e,on='unión')
union=pd.merge(union,f,on='unión')

#retoco la tabla para dejarla mas intuitiva
union.drop(columns=["unión"],inplace=True)
union.rename(columns={"Calidad_preparación":"Calidad preparación (excelente o buena)","Burbujas":"Burbujas insignificante",
                     "No evaluación completa":"Evaluación completa","No_info":"Informadas en la totalidad del tracto GI",
                     "Básico":"Estructuras de alto valor","Recto":"Visón de recto"}, inplace=True)
union.index=['Cidma', 'Uruguay', 'Total']
