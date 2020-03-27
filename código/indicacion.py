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