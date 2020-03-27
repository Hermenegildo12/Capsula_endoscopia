
import pandas as pd
import operator
#Función: Recibe una columna de la base de datos y le suma los hallazgos de hernia de hiato totales
#Parámetros: fila: Columna donde poner la suma
def hernia (fila):
    a='Hernia_hiato_esof'
    b='Hernia_hiato_estom'
    if fila[a]==fila[b]:
        return fila[a]
    elif fila[a]<fila[b]:
        return fila[b]
    else:
        return fila[a]

#Función: Unificar en una variable (Crohn y EII)
#Parámteros: Recibe la fila donde hacer la suma
def EII(fila):
    a='EII'
    b='Crohn'
    if fila[a]==fila[b]:
        return fila[a]
    elif fila[a]<fila[b]:
        return fila[b]
    else:
        return fila[a]

#Función: Función para recodificar la edad en intervalos
#Parámetros: datos:[base de datos]// cent: centro a recalcular// limi_inf, limi_sup: Limites para recalcular
#simbolo: menor(<), mayor(>), entre: Incluyer los dos límites, entre_no: No coge el límite inferior
def edades (datos,cent,limi_inf,simbolo,limi_sup=0):
    centro=datos[datos["Médico"]==cent]
    if simbolo=="<":
        numero=len(centro[centro["Edad"]<limi_inf])
        return numero
    elif simbolo=="entre":
        numero=len(centro[(centro["Edad"]>=limi_inf) & (centro["Edad"]<=limi_sup)])
        return numero
    elif simbolo=="entre_no":
        numero=len(centro[(datos["Edad"]>limi_inf) & (centro["Edad"]<=limi_sup)])
        return numero
    elif simbolo==">":
        numero=len(centro[(centro["Edad"]>limi_inf)])
        return numero

# Función: Crea una nueva variable con los intervalos de edad.
#Parámetros: e:[edad de los pacientes]
def intervalos (e):
    if e<30:
        return 0
    elif 30<=e<=45:
        return 1
    elif 45<e<=65:
        return 2
    elif 65<e<=80:
        return 3
    else:
        return 4

#Función: Calcular el porcentaje.
#Parámetros: a(Es el valor que equilvadría al 100%) + b(La submuestra que queremos concer su %)
def por(a,b):
    x=round((b*100/a),2)
    return x

#Función: Hacer un cuadro para presentar los datos:
#Parámetros: c_t: CIDMA total // u_t: Uruguay total // primera: nombre 1º columna // c_p: CIDMA primer valor // u_p: Uruguay primer valor
# segunda: (c_s, u_s) // tercera: (c_ter, u_ter)
def cuadro(tema,c_t,u_t,primera,c_p,u_p,segunda,c_s,u_s,tercera=0,c_ter=0,u_ter=0):
    x=pd.DataFrame({tema:[c_t,u_t],
                    primera:[[c_p,por(c_t,c_p)],[u_p,por(u_t,u_p)]],
                         segunda:[[c_s,por(c_t,c_s)],[u_s,por(u_t,u_s)]],
                       tercera:[[c_ter,por(c_t,c_ter)],[u_ter,por(u_t,u_ter)]],}
                        ,index=["Cidma","Uruguay"])
    return x


# Función que recibe una indicación y mira el número de pacientes (CIDMA, Uruguay) y calcular (número y porcentaje)
# de hallazgos terapéutico, pruebas complementarias y no evaluables.
# Junto a eso también porporciona los hallazgos más frecuentes y si de los pacientes sin hallazgos clasificados como
# Normal tienen zonas no evaluadas.
#Parámetros: datos(Base de datos), hz_Tta, hz_prueba, no_evaluable: variables que agrupran dichas columnas
#indicacion: Indicación a evaluar
# NOTA: Para entender la función, se desgrana mejor apartir del else, el resto es lo mismo pero mas agrupado y
# recortado
def porcentajes(datos,hz_Tta,hz_prueba,no_evaluable,indicacion):
    cidma_a = datos[(datos['Médico'] == 0) & (datos[indicacion] == 1)]
    uruguay_b = datos[(datos['Médico'] == 1) & (datos[indicacion] == 1)]
    paciente_indicacion = len(cidma_a)
    paciente_indicacion_uru = len(uruguay_b)

    if paciente_indicacion == 0:
        uruguay_b["Hz_Tta"] = uruguay_b[hz_Tta].sum(axis=1)
        hzgs_T_uruguay = len(uruguay_b[uruguay_b["Hz_Tta"] >= 1])
        uruguay_b["Hz_Prueba"] = uruguay_b[hz_prueba].sum(axis=1)
        hzgs_P_uruguay = len(uruguay_b[uruguay_b["Hz_Prueba"] >= 1])
        norml_uruguay = uruguay_b[(uruguay_b["Hz_Tta"] == 0) &
                                  (uruguay_b["Hz_Prueba"] == 0)]
        normal_uruguay = len(norml_uruguay)
        no_visi_uruguay = []
        No_visi_uruguay = []
        for e in no_evaluable:
            a_uru = uruguay_b[e].isin([1])
            for i in a_uru:
                if i == 1:
                    b_uru = uruguay_b[e][a_uru].index
                    no_visi_uruguay.append(b_uru)
                elif len(no_visi_uruguay) >= 1:
                    for j in no_visi_uruguay:
                        for x in j:
                            No_visi_uruguay.append(x)
                elif len(no_visi_uruguay) == 0:
                    No_visi_uruguay = []
        NO_VISIBLE_uruguay = set(No_visi_uruguay)
        no_eva_uruguay = len(NO_VISIBLE_uruguay)
        N_No_eva_urugua = []
        for e in NO_VISIBLE_uruguay:
            for i in norml_uruguay.index:
                if e == i:
                    N_No_eva_urugua.append(e)
        N_No_eva_uruguay = len(N_No_eva_urugua)
        dic_b = {}
        for e in hz_Tta:
            b = uruguay_b[e].value_counts()
            dic_b[e] = b
        hz_Tta_frec_uruguay = {}
        for e in hz_Tta:
            if len(dic_b[e]) > 1:
                hz_Tta_frec_uruguay[e] = dic_b[e][1]
            elif len(dic_b[e]) == 1:
                if dic_b[e].keys() == 0:
                    del dic_b[e]
            else:
                hz_Tta_frec_uruguay[e] = dic_b[e][1]
        hz_Tta_frec_uruguay = sorted(hz_Tta_frec_uruguay.items(), key=operator.itemgetter(1), reverse=True)
        for e in hz_prueba:
            c = uruguay_b[e].value_counts()
            dic_b[e] = c
        hz_prueba_frec_uruguay = {}
        for e in hz_prueba:
            if len(dic_b[e]) > 1:
                hz_prueba_frec_uruguay[e] = dic_b[e][1]
            elif len(dic_b[e]) == 1:
                if dic_b[e].keys() == 0:
                    del dic_b[e]
            else:
                hz_prueba_frec_uruguay[e] = dic_b[e][1]
        hz_prueba_frec_uruguay = sorted(hz_prueba_frec_uruguay.items(), key=operator.itemgetter(1), reverse=True)

        pregunta = pd.DataFrame({"Pacientes": ["NO", paciente_indicacion_uru],
                                 "Normal": [["NO"], [normal_uruguay, str(
                                     round((normal_uruguay * 100 / paciente_indicacion_uru), 2)) + " %"]],
                                 "No evaluable": [["NO"], [no_eva_uruguay, str(
                                     round((no_eva_uruguay * 100 / paciente_indicacion_uru), 2)) + " %"]],
                                 "Hz Pruebas": [["NO"], [hzgs_P_uruguay, str(
                                     round((hzgs_P_uruguay * 100 / paciente_indicacion_uru), 2)) + " %"]],
                                 "Hz Tratamiento": [["NO"], [hzgs_T_uruguay, str(
                                     round((hzgs_T_uruguay * 100 / paciente_indicacion_uru), 2)) + " %"]]}
                                , index=["Cidma", "Uruguay"])

        return (
        pregunta, "{} Uruguay hallazgos terapeúticos más frecuentes {}".format(indicacion, hz_Tta_frec_uruguay[0:3]),
        "{} Uruguay hallazgos pruebas complementarias {}".format(indicacion, hz_prueba_frec_uruguay[0:3]),
        "Uruguay pacientes sin hallazgos patológicos con áreas del tracto digestivo no evaluables {}".format(
            N_No_eva_uruguay),
        "No CIDMA", "No CIDMA", "No CIDMA")


    elif paciente_indicacion_uru == 0:
        cidma_a["Hz_Tta"] = cidma_a[hz_Tta].sum(axis=1)
        hzgs_T_cidma = len(cidma_a[cidma_a["Hz_Tta"] >= 1])
        cidma_a["Hz_Prueba"] = cidma_a[hz_prueba].sum(axis=1)
        hzgs_P_cidma = len(cidma_a[cidma_a["Hz_Prueba"] >= 1])
        norml_cidma = cidma_a[(cidma_a["Hz_Tta"] == 0) & (cidma_a["Hz_Prueba"] == 0)]
        normal_cidma = len(norml_cidma)
        no_visi_cidma = []
        No_visi_cidma = []
        for e in no_evaluable:
            a = cidma_a[e].isin([1])
            for i in a:
                if i == 1:
                    b = cidma_a[e][a].index
                    no_visi_cidma.append(b)
                elif len(no_visi_cidma) >= 1:
                    for j in no_visi_cidma:
                        for x in j:
                            No_visi_cidma.append(x)
                elif len(no_visi_cidma) == 0:
                    No_visi_cidma = []
        NO_VISIBLE_cidma = set(No_visi_cidma)
        no_eva_cidma = len(NO_VISIBLE_cidma)
        N_No_eva_cidm = []
        for e in NO_VISIBLE_cidma:
            for i in norml_cidma.index:
                if e == i:
                    N_No_eva_cidm.append(e)
        N_No_eva_cidma = len(N_No_eva_cidm)
        dic = {}
        for e in hz_Tta:
            b = cidma_a[e].value_counts()
            dic[e] = b
        hz_Tta_frec_cidma = {}
        for e in hz_Tta:
            if len(dic[e]) > 1:
                hz_Tta_frec_cidma[e] = dic[e][1]
            elif len(dic[e]) == 1:
                if dic[e].keys() == 0:
                    del dic[e]
            else:
                hz_Tta_frec_cidma[e] = dic[e][1]
        hz_Tta_frec_cidma = sorted(hz_Tta_frec_cidma.items(), key=operator.itemgetter(1), reverse=True)
        dic = {}
        for e in hz_prueba:
            b = cidma_a[e].value_counts()
            dic[e] = b
        dic_b = {}
        hz_prueba_frec_cidma = {}
        for e in hz_prueba:
            if len(dic[e]) > 1:
                hz_prueba_frec_cidma[e] = dic[e][1]
            elif len(dic[e]) == 1:
                if dic[e].keys() == 0:
                    del dic[e]
            else:
                hz_prueba_frec_cidma[e] = dic[e][1]
        hz_prueba_frec_cidma = sorted(hz_prueba_frec_cidma.items(), key=operator.itemgetter(1), reverse=True)

        pregunta = pd.DataFrame({"Pacientes": [paciente_indicacion, "NO"],
                                 "Normal": [
                                     [normal_cidma, str(round((normal_cidma * 100 / paciente_indicacion), 2)) + " %"],
                                     ["NO"]],
                                 "No evaluable": [
                                     [no_eva_cidma, str(round((no_eva_cidma * 100 / paciente_indicacion), 2)) + " %"],
                                     ["NO"]],
                                 "Hz Pruebas": [
                                     [hzgs_P_cidma, str(round((hzgs_P_cidma * 100 / paciente_indicacion), 2)) + " %"],
                                     ["NO"]],
                                 "Hz Tratamiento": [
                                     [hzgs_T_cidma, str(round((hzgs_T_cidma * 100 / paciente_indicacion), 2)) + " %"],
                                     ["NO"]]}, index=["Cidma", "Uruguay"])

        return (
        pregunta, "{} CIDMA hallazgos terapeúticos más frecuentes {}".format(indicacion, hz_Tta_frec_cidma[0:3]),
        "{} CIDMA hallazgos pruebas complementarias {}".format(indicacion, hz_prueba_frec_cidma[0:3]),
        "CIDMA pacientes sin hallazgos patológicos con áreas del tracto digestivo no evaluables {}".format(
            N_No_eva_cidma),
        "NO Uruguay", "No Uruguay", "No Uruguay")
    else:
        # Número de pacientes con hallazgos para futuras terapías
        # CIDMA
        cidma_a["Hz_Tta"] = cidma_a[hz_Tta].sum(axis=1)
        hzgs_T_cidma = len(cidma_a[cidma_a["Hz_Tta"] >= 1])
        # Uruguay
        uruguay_b["Hz_Tta"] = uruguay_b[hz_Tta].sum(axis=1)
        hzgs_T_uruguay = len(uruguay_b[uruguay_b["Hz_Tta"] >= 1])

        # Número de pacientes con hallazgos para futuros estudios
        # CIDMA
        cidma_a["Hz_Prueba"] = cidma_a[hz_prueba].sum(axis=1)
        hzgs_P_cidma = len(cidma_a[cidma_a["Hz_Prueba"] >= 1])
        # Uruguay
        uruguay_b["Hz_Prueba"] = uruguay_b[hz_prueba].sum(axis=1)
        hzgs_P_uruguay = len(uruguay_b[uruguay_b["Hz_Prueba"] >= 1])

        # Número de pacientes con hallazgos compatibles con la normalidad
        # CIDMA
        norml_cidma = cidma_a[(cidma_a["Hz_Tta"] == 0) &
                              (cidma_a["Hz_Prueba"] == 0)]
        normal_cidma = len(norml_cidma)
        # Uruguay
        norml_uruguay = uruguay_b[(uruguay_b["Hz_Tta"] == 0) &
                                  (uruguay_b["Hz_Prueba"] == 0)]
        normal_uruguay = len(norml_uruguay)

        # Número de pacientes con zonas del tracto GI sin posible evaluación
        # CIDMA
        no_visi_cidma = []
        No_visi_cidma = []
        for e in no_evaluable:
            a = cidma_a[e].isin([1])
            for i in a:
                if i == 1:
                    b = cidma_a[e][a].index
                    no_visi_cidma.append(b)
                elif len(no_visi_cidma) >= 1:
                    for j in no_visi_cidma:
                        for x in j:
                            No_visi_cidma.append(x)
                elif len(no_visi_cidma) == 0:
                    No_visi_cidma = []
        NO_VISIBLE_cidma = set(No_visi_cidma)
        no_eva_cidma = len(NO_VISIBLE_cidma)

        # Pacientes sin hallazgos patologicos con zonas del tracto digestivo no evaluables
        N_No_eva_cidm = []
        for e in NO_VISIBLE_cidma:
            for i in norml_cidma.index:
                if e == i:
                    N_No_eva_cidm.append(e)
        N_No_eva_cidma = len(N_No_eva_cidm)
        # Uruguay
        no_visi_uruguay = []
        No_visi_uruguay = []
        for e in no_evaluable:
            a_uru = uruguay_b[e].isin([1])
            for i in a_uru:
                if i == 1:
                    b_uru = uruguay_b[e][a_uru].index
                    no_visi_uruguay.append(b_uru)
                elif len(no_visi_uruguay) >= 1:
                    for j in no_visi_uruguay:
                        for x in j:
                            No_visi_uruguay.append(x)
                elif len(no_visi_uruguay) == 0:
                    No_visi_uruguay = []
        NO_VISIBLE_uruguay = set(No_visi_uruguay)
        no_eva_uruguay = len(NO_VISIBLE_uruguay)

        N_No_eva_urugua = []
        for e in NO_VISIBLE_uruguay:
            for i in norml_uruguay.index:
                if e == i:
                    N_No_eva_urugua.append(e)
        N_No_eva_uruguay = len(N_No_eva_urugua)

        # Hallazgos tratamientos más frecuentes
        # CIDMA
        dic = {}
        for e in hz_Tta:
            b = cidma_a[e].value_counts()
            dic[e] = b

        hz_Tta_frec_cidma = {}
        for e in hz_Tta:
            if len(dic[e]) > 1:
                hz_Tta_frec_cidma[e] = dic[e][1]
            elif len(dic[e]) == 1:
                if dic[e].keys() == 0:
                    del dic[e]
            else:
                hz_Tta_frec_cidma[e] = dic[e][1]
        hz_Tta_frec_cidma = sorted(hz_Tta_frec_cidma.items(), key=operator.itemgetter(1), reverse=True)

        # Uruguay
        dic_b = {}
        for e in hz_Tta:
            b = uruguay_b[e].value_counts()
            dic_b[e] = b

        hz_Tta_frec_uruguay = {}
        for e in hz_Tta:
            if len(dic_b[e]) > 1:
                hz_Tta_frec_uruguay[e] = dic_b[e][1]
            elif len(dic_b[e]) == 1:
                if dic_b[e].keys() == 0:
                    del dic_b[e]
            else:
                hz_Tta_frec_uruguay[e] = dic[e][1]
        hz_Tta_frec_uruguay = sorted(hz_Tta_frec_uruguay.items(), key=operator.itemgetter(1), reverse=True)

        # Hallazgos pruebas complementarias mas frecuentes
        # CIDMA
        dic = {}
        for e in hz_prueba:
            b = cidma_a[e].value_counts()
            dic[e] = b
        hz_prueba_frec_cidma = {}
        for e in hz_prueba:
            if len(dic[e]) > 1:
                hz_prueba_frec_cidma[e] = dic[e][1]
            elif len(dic[e]) == 1:
                if dic[e].keys() == 0:
                    del dic[e]
            else:
                hz_prueba_frec_cidma[e] = dic[e][1]
        hz_prueba_frec_cidma = sorted(hz_prueba_frec_cidma.items(), key=operator.itemgetter(1), reverse=True)

        # Uruguay
        dic_b = {}
        for e in hz_prueba:
            c = uruguay_b[e].value_counts()
            dic_b[e] = c
        hz_prueba_frec_uruguay = {}
        for e in hz_prueba:
            if len(dic_b[e]) > 1:
                hz_prueba_frec_uruguay[e] = dic_b[e][1]
            elif len(dic_b[e]) == 1:
                if dic_b[e].keys() == 0:
                    del dic_b[e]
            else:
                hz_prueba_frec_uruguay[e] = dic_b[e][1]
        hz_prueba_frec_uruguay = sorted(hz_prueba_frec_uruguay.items(), key=operator.itemgetter(1), reverse=True)

        pregunta = pd.DataFrame({"Pacientes": [paciente_indicacion, paciente_indicacion_uru],
                                 "Normal": [
                                     [normal_cidma, str(round((normal_cidma * 100 / paciente_indicacion), 2)) + " %"],
                                     [normal_uruguay,
                                      str(round((normal_uruguay * 100 / paciente_indicacion_uru), 2)) + " %"]],
                                 "No evaluable": [
                                     [no_eva_cidma, str(round((no_eva_cidma * 100 / paciente_indicacion), 2)) + " %"],
                                     [no_eva_uruguay,
                                      str(round((no_eva_uruguay * 100 / paciente_indicacion_uru), 2)) + " %"]],
                                 "Hz Pruebas": [
                                     [hzgs_P_cidma, str(round((hzgs_P_cidma * 100 / paciente_indicacion), 2)) + " %"],
                                     [hzgs_P_uruguay,
                                      str(round((hzgs_P_uruguay * 100 / paciente_indicacion_uru), 2)) + " %"]],
                                 "Hz Tratamiento": [
                                     [hzgs_T_cidma, str(round((hzgs_T_cidma * 100 / paciente_indicacion), 2)) + " %"],
                                     [hzgs_T_uruguay,
                                      str(round((hzgs_T_uruguay * 100 / paciente_indicacion_uru), 2)) + " %"]]}
                                , index=["Cidma", "Uruguay"])

        return (
        pregunta, "{} CIDMA hallazgos terapeúticos más frecuentes {}".format(indicacion, hz_Tta_frec_cidma[0:3]),
        "{} CIDMA hallazgos pruebas complementarias {}".format(indicacion, hz_prueba_frec_cidma[0:3]),
        "CIDMA pacientes sin hallazgos patológicos con áreas del tracto digestivo no evaluables {}".format(
            N_No_eva_cidma),
        "{} Uruguay hallazgos terapeúticos más frecuentes {}".format(indicacion, hz_Tta_frec_uruguay[0:3]),
        "{} Uruguay hallazgos pruebas complementarias más frecuentes {}".format(indicacion,
                                                                                hz_prueba_frec_uruguay[0:3]),
        "Uruguay pacientes sin hallazgos patológicos con áreas del tracto digestivo no evaluables {}".format(
            N_No_eva_uruguay))


#Función: para pasar todos analizar porcentajes según centro de los criterios de calidad
#Función que recibe como parámetros:
#Indicacion: Columna a analizar // valor: Valor apartir del cual queremos seleccionar // signo: Para distinguir entre
#Mayor e igual al valor introducido
#Devuelve 2 columnas, una es la indicacion y la otra seria la unión, que permitiria unir a futuras tablas.
def resumen (datos,indicacion,valor,signo):
    c_a = datos[datos['Médico']==0]
    u_b= datos[datos['Médico']==1]
    c_T=len(c_a)
    u_T=len(u_b)
    if signo==">":
        c_sub=c_a[c_a[indicacion]>=valor]
        u_sub=u_b[u_b[indicacion]>=valor]
    elif signo=="=":
        c_sub=c_a[c_a[indicacion]==valor]
        u_sub=u_b[u_b[indicacion]==valor]
    x=pd.DataFrame({"unión":[1,2,3],
                    indicacion:[[len(c_sub),por(108,len(c_sub))],[len(u_sub),por(143,len(u_sub))],
                                [len(c_sub)+len(u_sub),por(251,len(c_sub)+len(u_sub))]]}
                        ,index=["Cidma","Uruguay","Total"])
    return x

# Función que recibe los hallazgos de una zona del tracto digestivo Y el centro médico donde se realizo la prueba
#y devuelve la suma de todos los hallazgos encontrados en ella. Ya sea en el centro o sino se le dice, devuelve la suma
# zona: Hallazgo a sumar valores // valor: 0(CIDMA);1(Uruguay);2(Ambos POR DEFECTO)
def hz (datos,zona,valor=2):
    if valor<=1:
        base=datos[datos["Médico"]==valor]
        hz_total=0
        a=base[zona].sum()
        for e in a:
            if type(e)==int:
                hz_total=hz_total+e
        return hz_total
    elif valor>1:
        hz_total=0
        a=datos[zona].sum()
        for e in a:
            if type(e)==int:
                hz_total=hz_total+e
        return hz_total


# Función: Calcular porcentajes de hallazgos por regiones del tracto GI + 3 hallazgos más frecuentes (Todo según el centro)
# Parámetros: zona:(str) Nombre de la región que quedemos analizar // hz_zona: Distintos hallazgos del área al estudio
#u_hz_T/c_hz_T: Número de hallazgos de totales de los distintos centros// datos: la base de datos
def zonas(u_hz_T,hz_total,c_hz_T,datos,zona, hz_zona):
    c = datos[datos["Médico"] == 0]
    u = datos[datos["Médico"] == 1]
    c_ = c[hz_zona].sum()
    c_hz_f = sorted(c_.items(), key=operator.itemgetter(1), reverse=True)  # Hallazgos más frecuentes de la zona CIDMA
    u_ = u[hz_zona].sum()
    u_hz_f = sorted(u_.items(), key=operator.itemgetter(1), reverse=True)  # Hallazgos más frecuentes de la zona Uruguay

    c_hz_suma = 0
    for e in c_hz_f:
        for i in e:
            if type(i) == int:
                c_hz_suma = c_hz_suma + i
    u_hz_suma = 0
    for e in u_hz_f:
        for i in e:
            if type(i) == int:
                u_hz_suma = u_hz_suma + i

    pregunta = pd.DataFrame({"Unión": [1, 2, 3],
                             zona: [[c_hz_suma, por(c_hz_T, c_hz_suma)], [u_hz_suma, por(u_hz_T, u_hz_suma)],
                                    [c_hz_suma + u_hz_suma, por(hz_total, c_hz_suma + u_hz_suma)]]
                             }, index=["Cidma", "Uruguay", "Total"])

    return (pregunta, "{} CIDMA hallazgos más frecuentes {}".format(zona, c_hz_f[0:3]),
            "{} Uruguay hallazgos más frecuentes {}".format(zona, u_hz_f[0:3]))

