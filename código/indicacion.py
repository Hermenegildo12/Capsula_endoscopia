from limpieza import *
from funcion import *
import pandas as pd
# Porcentaje de pacientes que vinieron con síntomas de dolor abdominal y tuvieron hallazgos en la cápsula.
# Diferenciando entre el centro en el que fue realizada la prueba.

#Para ello, agrupo primero todas las varibles que representan hallazgos en la cápsula endoscopica. Los agrupo en dos
#tipos:
#- Hallazgos que permiten tratamiento sin la necesidad de pruebas complementarias
#- Hallazgos que harían necesaria la realización de pruebas complementaris para el diagnostico completo.

#También defino otros conceptos:
#- Normal: Paciente sin hallazgos patológicos
#- No evaluable: Por diversos motivos, no se pudo estudiar algun trazo del tracto gastrointestinal completamente.

hz_Tta=["Hernia_hiato_total",
 'RGE_esof',
 'Erosiones_esof',
 'Erosiones_estom',
 'Pólipo_estom',
 'Telangiectasias_yey',
 'Linfagiectasias_yey',
 'Pólipo_yey',
 'Diverticulo_íleon',
'Erosiones_del',
 'Diverticulo_del',
 'Enteritis_del',
 'Pólipo_del',
 'Otros_del',
 'Hemorroides',
 'Diverticulo_col',
 'Diverticulo_C_drch',
 'Diverticulo_sig',
 'Diverticulo_C_izq',
 'Sigmoiditis',
 'Proctitis',
 'Angiodisplasia_col',
 'Pólipo_col',
 'Pólipo_C_drch',
 'Pólipo_C_asce',
 'Pólipo_C_trans',
 'Pólipo_C_izq',
 'Pólipo_C_desc',
 'Pólipo_ciego',
 'Pólipo_sig',
 'Pólipo_recto',
 'Melanosis',
 'Otras_col']

hz_prueba=['Trast_tránsito_esof',  'Barret_esof',  'Esof_eosinofilica_esof',  'Estenosis_extr_esof',
           'Trast_motilidad_estom','Gastritis_estom',  'Yeyunitis',  'Erosiones_yey',  'Ileitis',
           'Erosiones_íleon',  'Pólipo_íleon',  'Erosiones_col', 'Otros_estom',]

#En cuanto a las variables otros hallazgos de estómago, delgado y colon decido incluirlas en hz_Tta porque en su
#mayoria son de este tipo, aunque según resultados posteriores decidire si sacarlas, en base a posibles alteraciones
#en el analisis final.

cidma_dolor = datos[(datos['Médico']==0) &
                (datos['Dolor_abd']==1)]

#Número de pacientes con hallazgos para futuras terapías
cidma_dolor["Hz_Tta"] = cidma_dolor[hz_Tta].sum(axis=1)
c_pcts_Tta=cidma_dolor[cidma_dolor["Hz_Tta"]>=1]

#Número de pacientes con hallazgos para futuros estudios
cidma_dolor["Hz_Prueba"] = cidma_dolor[hz_prueba].sum(axis=1)
c_pcts_prueba=cidma_dolor[cidma_dolor["Hz_Prueba"]>=1]

#Número de pacientes con hallazgos compatibles con la normalidad
pct_normal=cidma_dolor[(cidma_dolor["Hz_Tta"]==0)&
(cidma_dolor["Hz_Prueba"]==0)]

no_evaluable=['No_evaluable_esof','No_evaluable_estom','No_evaluable_del','No_evaluable_col']

#Número de pacientes con zonas del tracto GI sin posible evaluación
no_visi=[]
No_visi=[]
for e in no_evaluable:
    a=cidma_dolor[e].isin([1])
    for i in a:
        if i==1:
            b=cidma_dolor[e][a].index
            no_visi.append(b)
        elif len(no_visi)>=1:
            for j in no_visi:
                for x in j:
                    No_visi.append(x)
        elif len(no_visi)==0:
            No_visi=[]

NO_VISIBLE=set(No_visi)

#Pacientes sin hallazgos patologicos con zonas del tracto gigestivo no evaluables
for e in NO_VISIBLE:
    for i in pct_normal.index:
        if e==i:
            e

#Todos los pacientes con zonas no evaluables
c_no_evaluado=cidma_dolor[(cidma_dolor['No_evaluable_esof']==1) | (cidma_dolor["No_evaluable_estom"]==1)
       | (cidma_dolor['No_evaluable_del']==1) | (cidma_dolor['No_evaluable_col']==1)][no_evaluable]

#Como se ve solo dos pacientes no presentarian hallazgos patológicos y tendrían alguna zona del tracto digestivo sin poder evaluar (delgado, colon).
# En cuanto al resto de pacientes con zonas no evaluables, destacar la zona colónica como la principal área no evaluada con hasta 11 pacientes.

#Ahora veré cuales son los pricipales hallazgos de dichos pacientes.
#En primer lugar los hallazgos para tratamiento

dic={}
for e in hz_Tta:
    b=cidma_dolor[e].value_counts()
    dic[e]=b

hz_Tta_frec={}
for e in hz_Tta:
    if len(dic[e])>1:
        hz_Tta_frec[e]=dic[e][1]
sorted(hz_Tta_frec.items(), key=operator.itemgetter(1),reverse=True)

#Resultado:
#Como se observa los tres hallazgos principales son:
#- Diverticulos en colon
#- Hernia de hiato
#- Hemorroides

dic = {}
for e in hz_prueba:
    b = cidma_dolor[e].value_counts()
    dic[e] = b

#En cuanto a los hallazgos para completar estudio
hz_prueba_frec = {}
for e in hz_prueba:
    if len(dic[e]) > 1:
        hz_prueba_frec[e] = dic[e][1]
sorted(hz_prueba_frec.items(), key=operator.itemgetter(1),reverse=True)

#Resultado
#Principales hallazgos que necesitaran nuevas pruebas, destacan:
#- Gastritis (Este triplica la frecuencia del segundo)
#- Yeyunitis
#- Trastornos del tránsito esofágico

#Ahora analizaré las mismas variables en el hospital Italiano

uruguay_dolor = datos[(datos['Médico']==1) &
                (datos['Dolor_abd']==1)]

#Número de pacientes con hallazgos para futuras terapías
uruguay_dolor["Hz_Tta"] = uruguay_dolor[hz_Tta].sum(axis=1)
u_pcts_Tta=uruguay_dolor[uruguay_dolor["Hz_Tta"]>=1]

#Número de pacientes con hallazgos para estudios complementarios
uruguay_dolor["Hz_Prueba"] = uruguay_dolor[hz_prueba].sum(axis=1)
u_pcts_prueba=uruguay_dolor[uruguay_dolor["Hz_Prueba"]>=1]

#Número de pacientes con hallazgos compatibles con la normalidad
pct_normal_uru=uruguay_dolor[(uruguay_dolor["Hz_Tta"]==0)&
(uruguay_dolor["Hz_Prueba"]==0)]

#Número de pacientes con zonas del tracto GI sin posible evaluación (1)
#Como se ve uno de los pacientes (65) que no tiene hallazgos, tiene el esófago y el estómago sin evaluar.

#Hallazgos para posterior estuido complementario
#Hallazgos más frecuentes:
#- Hz Tratamiento: Pólipos en colon (4), sigmoiditis, resto todos con 1.
#- Hz Pruebas: Erosiones (Yeyuno, colon), ileitis.

#Cuadro resumen de los dos centros sobre la indicación de dolor abdominal
pregunta_1=pd.DataFrame({"Pacientes":[53,8],"Normal":[[6,str(round((6*100/53),2))+" %"],[3,str(round((3*100/8),2))+" %"]],
                         "No evaluable":[[15,str(round((15*100/53),2))+" %"],[1,str(round((1*100/8),2))+" %"]],
                       "Hz Pruebas":[[33,str(round((33*100/53),2))+" %"],[3,str(round((3*100/8),2))+" %"]],
                         "Hz Tratamiento":[[39,str(round((39*100/53),2))+" %"],[5,str(round((5*100/8),2))+" %"]]}
                        ,index=["Cidma","Uruguay"])

#RESULTADO
#Número de pacientes y porcentajes
# Se observa que un 88,68% de los pacientes de CIDMA a los que se le hizo la cápsula por síntomas de dolor abdominal presentaron hallazgos de algún tipo.
# Destacando el 73,58% que recibieron un diagnostico definitivo, sin necesidad de pruebas complementarias.
# Sin embargo ese porcentaje cae al 62,5% en los pacientes del hospital Italiano,
# pero que aún así permite observar una capacidad de deteción de hallazgos de mas del 60%.

# Resto de indicaciones
#Para el resto de indicaciones decido crear una función que recibiendo como entrada la indicación a analizar, devuelva
#el cuadro con los porcentajes y hallazgos mas frecuentes

# Todas las posibles indicaciones del estudio
indicacion=['HDOO_oculta',
 'HDOO_mani',
 'Crohn',
 'Alt_tránsito',
 'Anemia',
 'Dolor_abd',
 'Estreñimiento',
 'Diarrea',
 'Vómitos',
 'Pérdida_peso',
 'EII',
"Enf_II",
 'Colono_imcp',
 'Cribado',
 'Revisión',
 'Otros_indica']

#Organizo las indicaciones en base a la literatura
indicaciones_clasicas=['HDOO_oculta','HDOO_mani',"Cribado",'Anemia','Colono_imcp',"Enf_II",'Revisión']
indicaciones_nuevas=['Alt_tránsito','Dolor_abd','Estreñimiento','Diarrea','Vómitos','Pérdida_peso','Otros_indica']

#Bucle para pasar por la función el resto de indicaciones
'''for e in indicacion:
    a,b,c,d,e,f,g=porcentajes(datos,hz_Tta,hz_prueba,no_evaluable,e)
    print(a)'''

# Cribado de cáncer colorrectal
#Al ser una índicación tan dirigida, decido cambiar el analisis para resaltar las variables que indicarián el hallazgo de dicho cáncer

cribado=['Pólipo_col',
 'Pólipo_C_drch',
 'Pólipo_C_asce',
 'Pólipo_C_trans',
 'Pólipo_C_izq',
 'Pólipo_C_desc',
 'Pólipo_ciego',
 'Pólipo_sig',
 'Pólipo_recto']

a,b,c,d,e,f,g=porcentajes(datos,hz_Tta,hz_prueba,no_evaluable,"Cribado")

cidma_cribado = datos[(datos['Médico']==0) &
                (datos['Cribado']==1)]

#Pacientes de cidma con indicación de cribado con hallazgos de pólipos
cidma_polipo=cidma_cribado[cidma_cribado["Pólipo_col"]==1]

#De esos pacientes con pólipos, número con zonas del tracto digestivo no evaluable
no_evaluable_polipo_cidma=cidma_polipo[(cidma_polipo['No_evaluable_esof']==1) | (cidma_polipo["No_evaluable_estom"]==1)
       | (cidma_polipo['No_evaluable_del']==1) | (cidma_polipo['No_evaluable_col']==1)]

#Creo la variable no informado, que agrupa todas las columnas que reflejan ausencia de datos en el informe sobre las
#distintas zonas gastrointestinales

no_informado=['No_informado_esof','No_informado_estom','No_informado_del','No_informado_col']

#De esos mismos pacientes, cuales son los que tienen alguna zona GI sin informar
c_no_info=cidma_polipo[no_informado]

uruguay_cribado = datos[(datos['Médico']==1) &
                (datos['Cribado']==1)]

#Pacientes del hospital Italiano con indicación de cribado con hallazgos de pólipos
uruguay_polipo=uruguay_cribado[uruguay_cribado["Pólipo_col"]==1]

#De esos pacientes con pólipos, número con zonas del tracto digestivo no evaluable.
no_evaluable_polipo_uru=uruguay_polipo[(uruguay_polipo['No_evaluable_esof']==1) | (uruguay_polipo["No_evaluable_estom"]==1)
       | (uruguay_polipo['No_evaluable_del']==1) | (uruguay_polipo['No_evaluable_col']==1)]

#De esos mismos pacientes, cuales son los que tienen alguna zona GI sin informar
u_no_info=uruguay_polipo[no_informado]

a["Pólipos colón"]=[[3,(str((3*100//9))+" %")],[13,(str((13*100//49))+" %")]]

#Resultado
#Como se ve en la tabla resumen, a un 33% de los pacientes que venían por cribado se les detecto pólipos en el colon en CIDMA y a un 26% en el hospital Italiano.
# Destacando que, en ninguno de los dos centros, dichos pacientes tienen zonas GI no evaluadas.
# Tan solo detacar que de los 13 pacientes del hospital Italiano con pólipos,
# solo 2 de ellos tienen informado todo el tracto intestinal.
#  estando el resto con varias zonas GI no informadas, destacando el estómago que no se informa en 11 pacientes.
