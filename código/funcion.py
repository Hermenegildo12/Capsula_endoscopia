
import pandas as pd
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