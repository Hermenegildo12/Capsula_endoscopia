from funcion import *
import pandas as pd
import numpy as np
import operator
import matplotlib.pyplot as plt
import seaborn as sns
import math

# Importo la base de datos de los pacientes, recogida en SPSS y pasada posteriormente a documento csv. Para su analisis

datos = pd.read_csv("../Analisis_ano.csv", sep=";")


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

#Compruebo que la reoorganización se ha realizado correctamente
comp=datos[['Hernia_hiato_esof','Hernia_hiato_estom',"Hernia_hiato_total"]].sort_values(by="Hernia_hiato_total"),
ascending=True

#Tras asegurarme, elimino las dos variables sobrantes
datos.drop(columns=['Hernia_hiato_esof','Hernia_hiato_estom'],axis=0, inplace=True)

#Decido unir en una única variable las columnas "EEI" y "Crohn" ya que son pocos valores y tienen cierta relación
#que permitiria su analisis en conjunto sin modificar resultados. Quedando unidas en la variable "Enf_II"
datos["Enf_II"]=datos.apply(lambda fila: EII(fila),axis=1)
datos["Enf_II"].value_counts()

#Para calcular la edad media y poder dividir dicha variable en distintos tramos de edad. Evaluo la columna
#Viendo que se considera string por ello decido arreglar los valores mal asignados para poder transformalo a int

#Veo que hay datos no cogidos. Que impiden que pueda pasar a int la variable

#Como se ve arriba el problema esta en los pacientes 8 y 72, que sus edades se han cogido erronamente.
# Pero como veo que tienen la fecha de nacimiento hare una aproximación de edad en base a la fecha del procedimiento de los pacientes mas cercanos.
# Ya que no tendría sentido calcular la edad a fecha actual


#Una vez que se la edad aproximada de estos pacientes la modifico en su lugar correspondiente.
datos["Edad"].loc[8]=60
datos["Edad"].loc[72]=84

datos['Edad'] = datos['Edad'].astype('int64')

#Ahora sí miro como se comporta la edad en la muestra de pacientes

#Calculo el coeficiente de variación de Pearson para saber la dispersión de la variable edad, de cara a agruparla
#de la mejor forma posible.
CV=20.141148/abs(58.466135)

#Decido dividir las edades en base a posibles patologias y comorbilidades quedando así en 5 intervalos.
#Para ello creo una función que recibe como parametros;
#- El centro al que calcular la edad
#- Limiti inferior/superior
#- Simbolo para indicar si es (<,>,entre, etc...)

#Calculo los porcentajes de edad para CIDMA
cidma_30=(edades(datos,0,30,"<"))
cidma_30_45=edades(datos,0,30,"entre",45)
cidma_45_65=edades(datos,0,45,"entre_no",65)
cidma_65_80=edades(datos,0,65,"entre_no",80)
cidma_80=(edades(datos,0,80,">"))

#Calculo los porcentajes de edad para el hospital Italiano
u_30=(edades(datos,1,30,"<"))
u_30_45=edades(datos,1,30,"entre",45)
u_45_65=edades(datos,1,45,"entre_no",65)
u_65_80=edades(datos,1,65,"entre_no",80)
u_80=(edades(datos,1,80,">"))

datos["Edad_inter"]=datos["Edad"].apply(intervalos)

#Pacientes que no expulsan la cápsula

#Agrupo variables no evaluables
no_evaluable=['No_evaluable_esof','No_evaluable_estom','No_evaluable_del','No_evaluable_col']

#Al ver que hay un valor no recogido y tras analizarlo.Veo que la paciente no llego a expulsar la cápsula y por ello
#lo pongo correctamente
datos['Expulsa_cápsula'].loc[79]=0

#La convierto en int la columna
datos['Expulsa_cápsula'] = datos['Expulsa_cápsula'].astype('int64')

cidma_no_ex=datos[(datos['Médico']==0) & (datos['Expulsa_cápsula']==0)]
u_no_ex=datos[(datos['Médico']==1) & (datos['Expulsa_cápsula']==0)]

no_ex_total=len(cidma_no_ex)+len(u_no_ex)

#Ahora voy a ver en que parte del tracto digestivo la cápsula se quedo retenida, sin bateria etc...
#Para ello agrupo las variables de los tiempos de tránsito
tiempos=['T_estómago',
 'T_ID_total',
 'T_colon_total',
 'T_expulsión']

#Al ser pocos datos y no haber un criterio unificador de los tiempos, decido analizar las columnas y contarlo
#manualmente
cidma_colon=34
cidma_no_colon=5
u_colon=24
u_no_colon=9

#Número de pacientes en los que no se llega a ver el recto
c_no_recto=len(cidma_no_ex[cidma_no_ex["Recto"]==0])
u_no_recto=len(u_no_ex[u_no_ex["Recto"]==0])

#Agrupo las columnas medicamento en una única variable para su mejor análisis
medicacion=['Laxantes'
    ,'Antidiabético',
 'AINE',
 'Antiagregante',
 'Anticoagulante',
 'Benzodiacepina',
 'ARAII',
 'IBP',
 'Inmunosupresores',
 'Diurético',
 'Antiemético',
 'Vitaminas',
 'Antimicrobiano',
 'Otros_med']

