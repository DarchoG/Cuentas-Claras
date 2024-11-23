from flask import Flask, render_template, send_file, redirect,url_for, session, request
from flask import send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import matplotlib.pyplot as plt
import seaborn as sns

def obtenerInformacion(conexion):
    
    cursor = conexion.cursor()
    cursor.execute('SELECT ingresos, fecha FROM movimientos WHERE id_usuario = %s;', (session.get('user_id'),))
    ingresos = cursor.fetchall()
    cursor.execute('SELECT egresos, descripcion_movimiento, fecha FROM movimientos WHERE id_usuario = %s;', (session.get('user_id'),))
    egresos = cursor.fetchall()
    cursor.close()

    return ingresos, egresos

def agruparIngresos(tupla):

    auxiliar = []
    cantidadMes = 0
    mesAnterior = None
    cambio = None

    for monto, fecha in tupla:

        cambio = True
        cantidadMes += monto

        if(mesAnterior is None and fecha.month != mesAnterior):

            auxiliar.append(cantidadMes)
            cantidadMes = 0

        mesAnterior = fecha.month
    
    if(cambio is True): # Casos especiales para tratar un solo elemento o el último elemento en un mes no cambiante

        auxiliar.append(cantidadMes)

    return auxiliar

def agruparEgresos(tupla):

    dineroReservado = []
    egresos = []
    cadenaBusqueda = "Dinero reservado actualizado"

    reservadoMes = 0
    egresosMes = 0

    mesAnterior = None
    cambio = None

    for monto, movimiento, fecha in tupla:

        cambio = True

        if(movimiento == cadenaBusqueda):
            reservadoMes += monto
        else:
            egresosMes += monto

        if(mesAnterior is not None and fecha.month != mesAnterior): # Actualizar al detectar nuevo mes

            egresos.append(egresosMes)
            dineroReservado.append(reservadoMes)

            reservadoMes = 0
            egresosMes = 0

        mesAnterior = fecha.month

    if(cambio is True): # Casos especiales para tratar un solo elemento o el último elemento en un mes no cambiante

        egresos.append(egresosMes)
        dineroReservado.append(reservadoMes)

    return dineroReservado, egresos
        
def obtenerMeses(tupla):

    meses = {1 : "Enero", 2 : "Febrero", 3 : "Marzo", 4 : "Abril", 5 : "Mayo", 6 : "Junio", 7 : "Julio", 8 : "Agosto", 9 : "Septiembre", 10 : "Octubre", 11 : "Noviembre", 12 : "Diciembre"}
    auxiliar = []
    mesAnterior = None

    for _, fecha in tupla:

        if(fecha.month != mesAnterior):

            auxiliar.append(meses[fecha.month])

        mesAnterior = fecha.month

    return auxiliar

def graficar(conexion):

    ingresos, egresos = obtenerInformacion(conexion)
    meses = obtenerMeses(ingresos)

    ingresosMeses = agruparIngresos(ingresos)
    reservadoMeses, egresosMeses =  agruparEgresos(egresos)

    print("Ingresos: ", ingresosMeses)
    print("Reservado: ", reservadoMeses)
    print("Egresos:", egresosMeses)
    print("Meses:", meses)
        
    fig, ax = plt.subplots(figsize=(4, 7))
    sns.set_style("whitegrid") 

    x = range(len(meses))

    ax.bar(x, ingresosMeses, label="Ingresos", color="green")
    ax.bar(x, reservadoMeses, bottom=ingresosMeses, label="Reservado", color="orange")
    ax.bar(x, egresosMeses, bottom=[i + r for i, r in zip(ingresosMeses, reservadoMeses)], 
           label="Egresos", color="red")

    ax.set_xticks(x)
    ax.set_xticklabels(meses, rotation=45)
    ax.set_title("Gráfica de Gastos en Función de Ingresos")
    ax.legend()

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    canvas = plt.gcf()
    img = io.BytesIO()
    canvas.savefig(img, format="png", bbox_inches="tight", transparent=True)
    img.seek(0)

    return send_file(img, mimetype="image/png")

def graficarTotal(conexion):

    ingresos, egresos = obtenerInformacion(conexion)
    _ , egresosMeses =  agruparEgresos(egresos)

    ingresosTotales = sum(monto for monto, _ in ingresos)
    egresosTotales = sum(egresosMeses)

    fig, ax = plt.subplots(figsize=(7, 1))
    sns.set_style("whitegrid") 

    categoria = ["Ingresos", "Egresos"]
    valores = [ingresosTotales, egresosTotales]
    colores = ["green", "red"]

    ax.barh(categoria, valores, color = colores)

    ax.set_title("Total del mes")

    ax.grid(False)          
    ax.set_xticks([])   

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    canvas = plt.gcf()
    img = io.BytesIO()
    canvas.savefig(img, format="png", bbox_inches="tight", transparent=True)
    img.seek(0)

    return send_file(img, mimetype="image/png")