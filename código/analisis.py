import pandas as pd
import numpy as np
import operator
import matplotlib.pyplot as plt
import seaborn as sns
import math
import código
from limpieza import *
from funcion import *
from hallazgos_zona import *
from yeyuno_ileon import *
from criterios import *
from alta_calidad import *


#NÚMERO DE PACIENTES POR CENTRO, SEXO Y TRAMOS DE EDAD

#Número de pacientes total: 251

print("Número de pacientes pertenecientes a CIDMA {}".format(len(datos[datos["Médico"]==0]))+" pacientes")
print("Número de pacientes pertenecientes al hospital Italiano {}".format(len(datos[datos["Médico"]==1]))+" pacientes")

print("Número de mujeres totales {}".format(len(datos[datos["Sexo"]==0])))
print("Número de varónes totales {}".format(len(datos[datos["Sexo"]==1])))

print("Número de mujeres en Cidma {}".format(len(datos[(datos["Médico"]==0) & (datos["Sexo"]==0)])))
print("Número de mujeres en hospital Italiano {}".format(len(datos[(datos["Médico"]==1) & (datos["Sexo"]==0)])))

print("Número de varones en Cidma {}".format(len(datos[(datos["Médico"]==0) & (datos["Sexo"]==1)])))
print("Número de varones en hospital Italiano {}".format(len(datos[(datos["Médico"]==1) & (datos["Sexo"]==1)])))

#Distribución de la edad según la frecuencia
sns.violinplot("Edad", hue="Sexo", data=datos, split=True)

#Uso seaborn para ver las edades de cada centro
d=datos[datos["Médico"]==0]
c=datos[datos["Médico"]==1]
f, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect("equal")
ax = sns.kdeplot(c.Edad, c.Edad,
                 cmap="Reds", shade=True, shade_lowest=False)
ax = sns.kdeplot(d.Edad, d.Edad,
                 cmap="Blues", shade=False, shade_lowest=False)

# Add labels to the plot
red = sns.color_palette("Reds")[-2]
blue = sns.color_palette("Blues")[-2]
ax.text(2.5, 50, "CIDMA", size=16, color=blue)
ax.text(100, 100, "Italiano", size=16, color=red)

#Así quedaria la representación de la base de datos
partida=pd.DataFrame({"Pacientes":[[108,str(round((108*100/251),2))+" %"],[143,str(round((143*100/251),2))+" %"],251],
                     "Mujeres":[[65,str(round((65*100/108),2))+" %"],[70,str(round((70*100/143),2))+" %"],[135,str(round((135*100/251),2))+" %"]],
                     "Varones":[[43,str(round((43*100/108),2))+" %"],[73,str(round((73*100/143),2))+" %"],[116,str(round((116*100/251),2))+" %"]],
                     "Edad (<30 años)":[[cidma_30,str(round((cidma_30*100/108),2))+" %"],[u_30,str(round((u_30*100/143),2))+" %"],[32,str(round((32*100/251),2))+" %"]],
                     "Edad [30-45 años]":[[cidma_30_45,str(round((cidma_30_45*100/108),2))+" %"],[u_30_45,str(round((u_30_45*100/143),2))+" %"],[28,str(round((28*100/251),2))+" %"]],
                     "Edad (45-65 años]":[[cidma_45_65,str(round((cidma_45_65*100/108),2))+" %"],[u_45_65,str(round((u_45_65*100/143),2))+" %"],[90,str(round((90*100/251),2))+" %"]],
                     "Edad (65-80 años]":[[cidma_65_80,str(round((cidma_65_80*100/108),2))+" %"],[u_65_80,str(round((u_65_80*100/143),2))+" %"],[71,str(round((71*100/251),2))+" %"]],
                     "Edad (>80 años)":[[cidma_80,str(round((cidma_80*100/108),2))+" %"],[u_80,str(round((u_80*100/143),2))+" %"],[30,str(round((30*100/251),2))+" %"]]}
                     ,index=["CIDMA","Uruguay","Total"])

#PACIENTES QUE NO EXPULSA CÁPSULA

print("De los {} pacientes, no llegan a expulsar la cápsula".format(len(datos)))
print("    - CIDMA: {} pacientes".format(len(cidma_no_ex)))
print("    - Hospital Italiano: {} pacientes".format(len(u_no_ex)))
print("    - Total: {} pacientes".format(no_ex_total))

#Ahora voy a ver en que parte del tracto digestivo la cápsula se quedo retenida.

cuadro("No expulsadas",len(cidma_no_ex),len(u_no_ex),"Retención en colon",cidma_colon,u_colon,"No llega al colon",cidma_no_colon,u_no_colon,
      "No visión recto",c_no_recto,u_no_recto)

print("Edad media de los pacientes que no expulsaron la cápsula en CIDMA {}".format(cidma_no_ex["Edad"].mean()))
print("Edad media de los pacientes que no expulsaron la cápsula en Uruguay {}".format(u_no_ex["Edad"].mean()))

#Pacientes menores de 30 años de cidma con calidad de preparación inferior a excelente
len(cidma_no_ex[((cidma_no_ex['Calidad_preparación']==0) | (cidma_no_ex['Calidad_preparación']==1)
                 |(cidma_no_ex['Calidad_preparación']==2))
                   & (cidma_no_ex['Edad_inter']==0) ])

#RESULTADO:
#Como se observa 73 cápsulas no han sido expulsadas, suponiendo el 29% del total de los pacientes.
# Destacando la elevada retención de ellas en el colon el 79,4%, las cuales llegan a distintas alturas del colon.
#Llama la antención que el 69,8% no llega a visionar el recto.
#En cuanto a la edad media de los pacientes, que no llegaron a expulsar es de 50 y 65 años, en CIDMA y
# el hospital italiano respectivamente. Lo que nos indica que puede exitir un sesgo importante, al equivaler la población en dicho rango de edad al 63% del tamaño muestral.
# Por ello decido analizar los diferentes rangos de edad.
#Observandose que efectivamente el hospital italiano tiene tan solo 5 cápsulas fuera del intervalo 45-80 años.
# Sin embargo la distribución de la edad en CIDMA es mas rica, teniendo dos picos de 11 pacientes cada uno, el primero por debajo de 30 años y el otro entre 65-80 años.
#Lo que llama la atención es que prácticamente la mitad de los pacientes de menos de 30 años de cidma, no hayan llegado a expulsar las cápsulas. a diferencia con los pacientes menores de 30 del hospital italiano, donde todos llegaron expulsarla.
#Buscando posibles causas, evaluo las indicaciones de estos pacientes (No expulsa + <30 años) 8 de ellos vienen por dolor abdominal.
# Ninguno tuvo cirugía previa y solo 2 tomaban algún tipo de medicación previa destacable.
# Por lo que el motivo principal puede ser la calidad de la preparación, donde se ve que 7 tienen un calidad entre pobre y buena,
# de los cuales 2 no llegaron a hacer una limpieza de colon adecuada.
#Esto podría explicarse por la corta edad de los pacientes, con una edad media de 22 años.

#Resultado de alguna indicación
print(pregunta_1)

#Resultado de los hallazgos patologicos según la región del tracto GI
print(HZ_ZONAS)

#Resultado de los hallazgos encontrados en yeyuno e íleon
print(oculto)

#Resultados de algunos criterios de calidad
print(union)

#Resultados de alta calidad
print(cuadro)