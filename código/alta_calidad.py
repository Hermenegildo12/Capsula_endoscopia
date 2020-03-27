from limpieza import *
from indicacion import *
#Pacientes cuya cápsula tiene criterios de alta calidad
#Definimos que debe cumplir la lectura de una pancapsulosendoscópia para considerarse de calidad:
#- Calidad de preparación excelente o buena.
#- Presencia de burbujas insignificante
#- Tener todas las zonas evaluadas
#- Tener todas las zonas informadas
#- Visión de al menos 4 estructuras básicas (definidas en el párrafo inferior)
#- Visión del recto

"""Agrupo en una única variable la visión de las estructuras básicas para saber que la cápsula ha evaluado lo principal
de cada paciente. Quedando esta columna con los siguientes valores:
- 5: Se ha visualizado todas las estructuras fundamentales
- 4: Se visualizan 4.
- Así hasta 0. Que indicaría que no se ve ninguna estructura fundamental"""

#Agrupo las columnas con las variables que representan las estructuras básicas
#Dada su controversia se decide quitar las flexuras (hepática, esplénica)
basicos=['Linea_Z',
 'Ampolla_vater',
 'Válvula_ileocecal',
 'Orificio_apendicular',
 'Recto']

#Agrupo en una única variable las visión de las estructuras básicas para saber que la cápsula ha evaluado lo principal
#de cada paciente. Quedando esta columna
datos["Básico"] = datos[basicos].sum(axis=1)

#Igualmente agrupo en una variable las columnas que representan si el doctor informo o no cada parte del tracto digestivo
datos["No_info"] = datos[no_informado].sum(axis=1)

#Pacientes que tienen como minimo 5 estructuras fundamentales de las 7 indicadas visibles en el procedimiento y que
#se vea el recto. No necesariamente que se expulse porque si se llega a visualizar el recto sería una evaluación
#completa
c_basicos=datos[( (datos["Básico"]==5)| (datos["Básico"]==4)) & (datos["Recto"]==1) & (datos["No_info"]==0) &
               (datos["Calidad_preparación"]>=2)]

#Agrupo en una única variable, todas las columnas que indican la evaluación o no de las zonas GI
c_basicos["No evaluación completa"] = c_basicos[no_evaluable].sum(axis=1)

#De dichos pacientes, cuales son los que NO tienen ninguna ZONA del tracto digestivo NO EVALUABLE
c_eva_total=c_basicos[c_basicos["No evaluación completa"]==0]

#De los pacientes sin ninguna zona no evaluada, cuales son los que no presentan ningún hallazgo.
c_eva_total["Hz_Tta"] = c_eva_total[hz_Tta].sum(axis=1)

c_eva_total["Hz_prueba"]=c_eva_total[hz_prueba].sum(axis=1)


#Pacientes con altos criterios de calidad con distintos tipos de hallazgos
Tta_total=c_eva_total[c_eva_total["Hz_Tta"]>=1]
Prueba_total=c_eva_total[c_eva_total["Hz_prueba"]>=1]

#Pacientes con altos criterios de calidad sin hallazgos patologicos
sanos_total=c_eva_total[(c_eva_total["Hz_Tta"]==0) & (c_eva_total["Hz_prueba"]==0) ]


#Cuadro resumen de pacientes con informes de alta calidad
cuadro("Alta calidad",len(c_eva_total),1,
       "No hallazgo patológicos",len(sanos_total),1,
       "Hallazgo de tratamiento", len(Tta_total),1,
      "Hallazgo de prueba",len(Prueba_total),1)