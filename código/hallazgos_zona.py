from limpieza import *
from yeyuno_ileon import *
# ¿ Cuales son los hallazgos más frecuentes en las distintas zonas del tracto gastrointestinal ?

#Antes de comenzar con este analisis decido cuales van a ser las columnas a analizar.
# Para ellos, reviso todos los hallazgos.Para poder distinguir de forma global que variables son las indicadas o cuales deben ser modificadas.
#Quito las columnas que indican normalidad, no evaluación o que no han sido informadas.
# Junto a esas elimino la de hallazgos yeyuno e íleon, ya que simplemente agrupan el conjuto de los hallazgos encontrados en dichas regiones.
#En cuanto a la duda principal es que hacer con las variables "Pólipos colon" y "Diverticulos colon" ya que agrupan
# tanto hallazgos especificos como hallazgos donde no se indicaba en que región especifica del colon se encontraba la lesión.
#Quedando los hallazgos organizados según la región anatómica

esofago=['RGE_esof',
 'Trast_tránsito_esof',
 'Erosiones_esof',
 'Barret_esof',
 'Esof_eosinofilica_esof',
 'Estenosis_extr_esof']

estomago=['Hernia_hiato_total',
'Trast_motilidad_estom',
 'Erosiones_estom',
 'Gastritis_estom',
 'Pólipo_estom',
 'Otros_estom']

duodeno=[ 'Erosiones_del',
 'Diverticulo_del',
 'Enteritis_del',
 'Pólipo_del',
 'Otros_del']

yeyuno=[ 'Yeyunitis',
 'Erosiones_yey',
 'Telangiectasias_yey',
 'Linfagiectasias_yey',
 'Pólipo_yey']

ileon=[ 'Ileitis',
 'Diverticulo_íleon',
 'Erosiones_íleon',
 'Pólipo_íleon']

colon_de=['Melanosis','Angiodisplasia_col', 'Pólipo_ciego','Pólipo_C_drch',
          'Pólipo_C_asce','Diverticulo_C_drch',"Erosion_c_de"]

colon_iz=[ 'Pólipo_C_trans', 'Pólipo_C_desc',
          'Pólipo_C_izq', 'Diverticulo_C_izq','Otras_col',"Erosion_c_iz"]

colon_sig=['Sigmoiditis','Pólipo_sig','Diverticulo_sig',
"Erosion_c_sig"]

recto=['Hemorroides','Proctitis','Pólipo_recto',
"Erosion_recto"]

#Comienzo con los pólipos de colon

polipos_anonimo=datos[(datos["Pólipo_col"]==1) & (datos['Pólipo_C_drch']==0) & (datos['Pólipo_C_asce']==0) &
        (datos['Pólipo_C_trans']==0) & (datos['Pólipo_C_izq']==0)& (datos['Pólipo_C_desc']==0) &
        (datos['Pólipo_ciego']==0) & (datos['Pólipo_sig']==0)& (datos['Pólipo_recto']==0)]

"""Tras su estudio veo que solo 9 de los 58 valores no tienen especificado en que región del colon se encentran dichos pólipos. 
Siendo 2 de CIDMA y 7 del hospital Italiano. Para su correcta localización reviso los informes con el digestivo del proyecto. 
Tras el analisis los cambios quedan:
- 6: colon izquierdo (colon transverso y descendente)
- 13: colon izquierdo (colon transverso)
- 97: Pólipo colon izquierdo (colon descendente)
- 176: colon derecho e izquierdo (colon ascendente y transverso)
- 177: colon izquierdo y sigmoides
- 205: colon sigmoides
- 214: colon izquierdo (colon transverso y descendente)
- 231: colon derecho e izquierdo (ciego, transverso y descendente)
- 235: colon sigmoides"""

datos["Pólipo_C_trans"][5]=1
datos['Pólipo_C_desc'][5]=1
datos["Pólipo_C_trans"][12]=1
datos['Pólipo_C_desc'][96]=1
datos["Pólipo_C_trans"][175]=1
datos['Pólipo_C_asce'][175]=1
datos['Pólipo_sig'][176]=1
datos['Pólipo_C_izq'][176]=1
datos['Pólipo_sig'][204]=1
datos["Pólipo_C_trans"][213]=1
datos['Pólipo_C_desc'][213]=1
datos["Pólipo_C_trans"][230]=1
datos['Pólipo_C_desc'][230]=1
datos['Pólipo_ciego'][230]=1
datos['Pólipo_sig'][234]=1

"""Evaluó los diverticulos:
- 18: Divertículos colon sigmoides. 
- 34: Divertículos colon sigmoides. 
- 52: Divertículos colon sigmoides. 
- 55: Divertículos colon sigmoides. 
- 56: Divertículos colon sigmoides. 
- 61: Divertículos colon sigmoides. 
- 68: Divertículos colon sigmoides. 
- 72: Divertículos colon sigmoides. 
- 96: Divertículos colon sigmoides. 
- 131: Divertículos colon derecho, izquierdo y sigmoides. 
- 133:  Divertículos colon derecho, izquierdo y sigmoides. 
- 148: Divertículos colon derecho y sigmoides. 
- 170: Divertículos colon derecho. 
- 176: Divertículos colon izquierdo. 
- 185: Divertículos colon derecho (ciego). 
- 204: Divertículos colon izquierdo y sigmoides. 
- 205: Divertículos colon izquierdo. 
- 212: Divertículos colon izquierdo y sigmoides. 
- 226: Divertículos colon sigmoides. 
- 234: Divertículos colon izquierdo y sigmoides. 
- 241: Divertículos colon sigmoides. """

diverticulo=['Diverticulo_col','Diverticulo_C_drch','Diverticulo_C_izq','Diverticulo_sig']

#Compruebo las variables y veo que el 84 tiene el valor erroneo
datos['Diverticulo_sig'][84]=1
#La convierto en int la columna
datos['Diverticulo_sig'] = datos['Diverticulo_sig'].astype('int64')

diverticulo_anonimo=datos[(datos['Diverticulo_col']==1) & (datos['Diverticulo_C_drch']==0) &
                          (datos['Diverticulo_sig']==0) & (datos['Diverticulo_C_izq']==0)]

datos['Diverticulo_sig'][18]=1
datos['Diverticulo_sig'][34]=1
datos['Diverticulo_sig'][52]=1
datos['Diverticulo_sig'][55]=1
datos['Diverticulo_sig'][56]=1
datos['Diverticulo_sig'][61]=1
datos['Diverticulo_sig'][68]=1
datos['Diverticulo_sig'][72]=1
datos['Diverticulo_sig'][96]=1
datos['Diverticulo_sig'][131]=1
datos['Diverticulo_C_drch'][131]=1
datos['Diverticulo_C_izq'][131]=1
datos['Diverticulo_sig'][133]=1
datos['Diverticulo_C_drch'][133]=1
datos['Diverticulo_C_izq'][133]=1
datos['Diverticulo_sig'][148]=1
datos['Diverticulo_C_drch'][148]=1
datos['Diverticulo_C_drch'][170]=1
datos['Diverticulo_C_izq'][176]=1
datos['Diverticulo_C_drch'][185]=1
datos['Diverticulo_C_izq'][204]=1
datos['Diverticulo_sig'][204]=1
datos['Diverticulo_C_izq'][205]=1
datos['Diverticulo_sig'][212]=1
datos['Diverticulo_C_izq'][212]=1
datos['Diverticulo_sig'][226]=1
datos['Diverticulo_sig'][234]=1
datos['Diverticulo_C_izq'][234]=1
datos['Diverticulo_sig'][241]=1

#Reviso los informes de angiodisplasia y veo que todos están localizadas en el colon derecho (ciego).
# Por ello dejo la columna para introducirla en la variable colon derecho.

"""Por último evaluare la erosión de colon, decidiendo dividirla en 4 variables diferentes. 
(erosion_c_de // erosion_c_iz, // erosion_c_sig // erosion_recto Situando a los pacientes de la columna como sigue:
- 2: Mal ubicado, es lesión en yeyuno
- 10: Colon derecho
- 41: colon sigmoides
- 66: colon derecho
- 122: colon derecho
- 146: colon derecho
- 169: recto
- 171: recto
- 199: colon izquierdo
- 213: No tiene erosiones
- 219: colon derecho
- 245: recto"""

#Creo las nuevas variables
datos["Erosion_c_de"]=pd.Series(0)
datos["Erosion_c_de"]=datos["Erosion_c_de"].fillna(0)

datos["Erosion_c_iz"]=pd.Series(0)
datos["Erosion_c_iz"]=datos["Erosion_c_iz"].fillna(0)

datos["Erosion_c_sig"]=pd.Series(0)
datos["Erosion_c_sig"]=datos["Erosion_c_sig"].fillna(0)

datos["Erosion_recto"]=pd.Series(0)
datos["Erosion_recto"]=datos["Erosion_recto"].fillna(0)

#Modifico los positivos en sus respectivas filas
datos["Erosion_c_de"][10]=1
datos["Erosion_c_sig"][41]=1
datos["Erosion_c_de"][66]=1
datos["Erosion_c_de"][122]=1
datos["Erosion_c_de"][146]=1
datos["Erosion_recto"][169]=1
datos["Erosion_recto"][171]=1
datos["Erosion_c_iz"][199]=1
datos["Erosion_c_de"][219]=1
datos["Erosion_recto"][245]=1

#Paso las nuevas columnas a int para facilitar las operaciones
datos["Erosion_c_de"]= datos["Erosion_c_de"].astype('int64')
datos["Erosion_c_iz"]= datos["Erosion_c_iz"].astype('int64')
datos["Erosion_c_sig"]= datos["Erosion_c_sig"].astype('int64')
datos["Erosion_recto"]= datos["Erosion_recto"].astype('int64')

#Calculo los hallazgos obtenidos

hz_total=hz(datos,esofago)+hz(datos,estomago)+hz(datos,duodeno)+hz(datos,yeyuno)+hz(datos,ileon)+hz(datos,colon_de)+hz(datos,colon_iz)+hz(datos,colon_sig)+hz(datos,recto)
c_hz_T=hz(datos,esofago,0)+hz(datos,estomago,0)+hz(datos,duodeno,0)+hz(datos,yeyuno,0)+hz(datos,ileon,0)+hz(datos,colon_de,0)+hz(datos,colon_iz,0)+hz(datos,colon_sig,0)+hz(datos,recto,0)
u_hz_T=hz(datos,esofago,1)+hz(datos,estomago,1)+hz(datos,duodeno,1)+hz(datos,yeyuno,1)+hz(datos,ileon,1)+hz(datos,colon_de,1)+hz(datos,colon_iz,1)+hz(datos,colon_sig,1)+hz(datos,recto,1)
print("Número de hallazgos en el hospital Italiano {}".format(u_hz_T))
print("Número de hallazgos en CIDMA {}".format(c_hz_T))
print("Número de hallazgos total {}".format(hz_total))

HZ_ZONAS=esofago,estomago,duodeno,yeyuno,ileon,colon_de,colon_iz,colon_sig,recto
nombre=["esofago","estomago","duodeno","yeyuno","ileon","colon_de","colon_iz","colon_sig","recto"]

oculto=pd.merge(hz_y, hz_i, on='unión')
oculto.drop(columns=["unión"],inplace=True)
oculto.index=['Cidma', 'Uruguay', 'Total']

# Despliego todas las tablas para poder analizarlas y escribirlo en la explicación de word
a,b,c=zonas(u_hz_T,hz_total,c_hz_T,datos,"Esófago",esofago)
d,e,f=zonas(u_hz_T,hz_total,c_hz_T,datos,"Estómago",estomago)
g,h,i=zonas(u_hz_T,hz_total,c_hz_T,datos,"Duodeno",duodeno)
j,k,l=zonas(u_hz_T,hz_total,c_hz_T,datos,"Yeyuno",yeyuno)
m,n,o=zonas(u_hz_T,hz_total,c_hz_T,datos,"íleon",ileon)
p,q,r=zonas(u_hz_T,hz_total,c_hz_T,datos,"Colon derecho",colon_de)
s,t,y=zonas(u_hz_T,hz_total,c_hz_T,datos,"Colon izquierdo",colon_iz)
v,w,x=zonas(u_hz_T,hz_total,c_hz_T,datos,"Colon sigmoides",colon_sig)
z,a2,b2=zonas(u_hz_T,hz_total,c_hz_T,datos,"Recto",recto)

#Unifico en una única tabla los porcentajes de los hallazgos
A=pd.merge(a, d, on='Unión')
B=pd.merge(A,g,on='Unión')
C=pd.merge(B,j,on='Unión')
D=pd.merge(C,m,on='Unión')
E=pd.merge(D,p,on='Unión')
F=pd.merge(E,s,on='Unión')
G=pd.merge(F,v,on='Unión')
HZ_ZONAS=pd.merge(G,z,on='Unión')
HZ_ZONAS.Unión=["Cidma","Uruguay", "Total"]
HZ_ZONAS.rename(columns={"Unión":"Centro"},inplace=True)

"""Resultados:
En un primer vistazo se observa claramente las diferencias entre el uso de la cápsula para la visión del colon únicamente, o cuando, se usa como una pancapsuloendoscópia. 
Observandose como el aumento relativo del porcentaje de hallazgos a medida que nos acercamos al colon, 
claramente evidente en el hospital Italiano. Concentrandose el 64,29% de todos los hallazgos encontrados en dicho centro. 
Adiferencia de CIDMA, donde el colon solo equivaldría al 34,81% del total.
Estos datos nos permite ver el gran potencial de diagnostico que la evaluación completa y 
no parcial de la cápsula puede aportar tanto al médico, como al paciente.
Así mismo cabe destacar como apesar de ser una de las regiones GI con menos frecuencia de hallazgos patologicos,
 el yeyuno e íleon concentran el 12,6% de los hallazgos globales. Lo que hace pensar en el número de pacientes no diagnosticados
  correctamente por la incapacidad de acceso a dichas áreas con las técnicas endoscopicas más populares."""