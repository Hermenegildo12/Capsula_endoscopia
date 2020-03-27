from limpieza import *
from funcion import *
from hallazgos_zona import *
import pandas as pd

# Analisis de los tiempos de tránsitos

#Agrupo todos los tiempos en una variable. Divido la base por centro y escojo solo los pacientes que han expulsado la cápsula.
# Ya que el resto tienen unos tiempos mal asignados, en base a si el médico puso donde se quedo sin bateria o
# si al quedarse sin bateria solo decia que no llegaba y no hizo suma.
#La idea a ver es si la velocidad de tránsito influye en la cantidad de hallazgos encontrados.
# Para ello divido en tránsito rápido y lento, seleccionando los pacientes más extremos de los dos grupos y comparandolos entre ellos.
#Comienzo preparando las columnas del tiempo de expulsión, la cual recoge la suma de los otros tiempos

tiempos=['T_estómago',
 'T_ID_total',
 'T_colon_total']

datos["T_expulsión"]=datos["T_expulsión"].apply(recodificar)
datos["T_expulsión"]= datos["T_expulsión"].astype('int64')

datos["T_estómago"]=datos["T_estómago"].apply(recodificar)
datos["T_estómago"]= datos["T_estómago"].astype('int64')

datos['T_ID_total']=datos['T_ID_total'].apply(recodificar)
datos['T_ID_total']= datos['T_ID_total'].astype('int64')

datos["T_colon_total"]=datos["T_colon_total"].apply(recodificar)
datos["T_colon_total"]= datos["T_colon_total"].astype('int64')

# CIDMA
#Miro el número de pacientes que expulsan y tienen los tiempos correctamente añadidos.
# Siendo el total de 69 pacientes. Tras evaluar la variabilidad de los tiempos de expulsión,
# selecciono 12 pacientes en cada extremo quedando:
"""- Rápido: Expulsaron la cápsula en menos de 200 minutos. (Rango del intervalo; 103)
- Lento: Expulsaron la cápsula en mas de 530 minutos. (Rango de intervalo; 260)"""

c_expulsa=datos[(datos["Médico"]==0) & (datos['Expulsa_cápsula']==1)]

c_rap=c_expulsa[c_expulsa["T_expulsión"]<200]
c_len=c_expulsa[c_expulsa["T_expulsión"]>530]

#Unifico todos los hallazgos juntos
hz_todos=['RGE_esof',
 'Trast_tránsito_esof',
 'Erosiones_esof',
 'Barret_esof',
 'Esof_eosinofilica_esof',
 'Estenosis_extr_esof',
'Hernia_hiato_total',
'Trast_motilidad_estom',
 'Erosiones_estom',
 'Gastritis_estom',
 'Pólipo_estom',
 'Otros_estom',
"Erosiones_del",
 'Diverticulo_del',
 'Enteritis_del',
 'Pólipo_del',
 'Otros_del',
'Yeyunitis',
 'Erosiones_yey',
 'Telangiectasias_yey',
 'Linfagiectasias_yey',
 'Pólipo_yey',
'Ileitis',
 'Diverticulo_íleon',
 'Erosiones_íleon',
 'Pólipo_íleon',
'Melanosis','Angiodisplasia_col', 'Pólipo_ciego','Pólipo_C_drch',
'Pólipo_C_asce','Diverticulo_C_drch',"Erosion_c_de",
'Pólipo_C_trans', 'Pólipo_C_desc',
'Pólipo_C_izq', 'Diverticulo_C_izq','Otras_col',"Erosion_c_iz",
'Sigmoiditis','Pólipo_sig','Diverticulo_sig',
"Erosion_c_sig",
'Hemorroides','Proctitis','Pólipo_recto',
"Erosion_recto"]

cidma_transito=velocidad(c_rap,c_len,hz_todos)

#Resultado:
#Los pacientes con tránsito rápido tuvieron mas hallazgos en todas las regiones
# del trácto digestivo salvo en yeyuno, íleon y colon izquierdo.

#Evaluo todas las regiones del tracto digestivo por separado para ir viendo donde destacan las diferencias.
#Las miro para analisis y lo borro posteriormente para facilitar la lectura
velocidad(c_rap,c_len,esofago)

#Resultado:
"""Como se ve la mayoria de los pacientes de tránsito rápido tienen entre 45-65 años (7 pacientes), 
solo hay un menor de 30 años y no hay ninguno de mas de 80. Tieniendo como media de edad 52 años y mediana de 53.
En cuanto a los pacientes del otro extremo hay 3 menores de 30 y dos mayores de 80 años. 
Teniendo como media de edad 54 con una mediana de 62 años. Lo que se puede ver que en su conjunto son mayores que los de tránsito rápido"""

"""#Hospital Italiano
Ahora hago lo mismo con Urguay. Donde de los 110 pacientes que expulsan la cápsula unos 44 no tienen los tiempos
correctramente recogidos. Lo que puede deberse a que esos pacientes tuvieran tiempos más largos 
y no se calculasen o simplemente no se transcribio al informe, ¿posible sesgo?.
En cuanto al resto de los pacientes (66), mido como se comportan los tiempos de expulsión para seleccionar a los pacientes 
que expulsaron más rápido y más lento. Quedando 10 pacientes en cada extremo, según la siguiente forma: 
- Rápido: Expulsaron la cápsula en menos de 153 minutos. (Rango del intervalo; 92)
- Lento: expulsaron la cápsula en mas de 440 minutos. (Rango del intervalo; 337)
La disparidad de rangos, se debe a que a mayor tiempo mayor variabilidad de tiempos. 
Según resultado veré si es necesario disminuir la n para maximizar la diferencia"""

#Uruguay
u_ex=datos[(datos["Médico"]==1) & (datos['Expulsa_cápsula']==1)]
u_expulsa=u_ex[u_ex["T_expulsión"]>=1]

u_rap=u_expulsa[u_expulsa["T_expulsión"]<=153]
u_len=u_expulsa[u_expulsa["T_expulsión"]>=440]

uruguay_transito=velocidad(u_rap,u_len,hz_todos)


