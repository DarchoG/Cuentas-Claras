from flask import Flask, render_template, send_file, redirect,url_for, session, request
from flask import send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import datetime
import matplotlib.pyplot as plt
import seaborn as sns


def obtenerInformacion(conexion):

    stringBusqueda = "Dinero reservado actualizado"

    cursor = conexion.cursor()
    cursor.execute('SELECT ingresos, fecha FROM movimientos WHERE id_usuario = %s;', (session.get('user_id'),))
    ingresos = cursor.fetchall()
    cursor.execute('SELECT egresos, fecha FROM movimientos WHERE id_usuario = %s AND descripcion_movimiento != %s;', (session.get('user_id'),stringBusqueda,))
    egresos = cursor.fetchall()
    cursor.execute('SELECT egresos, fecha FROM movimientos WHERE id_usuario = %s AND descripcion_movimiento = %s;', (session.get('user_id'),stringBusqueda,))
    dineroReservado = cursor.fetchall()
    cursor.close()

    return ingresos, dineroReservado, egresos

def agruparFecha(tupla):

    auxiliar = []
    cantidadMes = 0
    mesAnterior = None

    for monto, fecha in tupla:

        cantidadMes += monto

        if(mesAnterior is None or fecha.month != mesAnterior):

            auxiliar.append(cantidadMes)
            cantidadMes = 0

        mesAnterior = fecha.month

    return auxiliar

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

    ingresos, dineroReservado, egresos = obtenerInformacion(conexion)
    meses = obtenerMeses(ingresos)

    ingresosMeses = agruparFecha(ingresos)
    reservadoMeses = agruparFecha(dineroReservado)
    egresosMeses = agruparFecha(egresos)

    print("Ingresos: ", ingresosMeses)
    print("Reservado: ", reservadoMeses)
    print("Egresos:", egresosMeses)
    print("Meses:", meses)
        
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.set_style("darkgrid") 

    x = [i for i in range(1000)]
    y = [i for i in range(1000)]

    sns.lineplot(x=x, y=y)
    canvas = FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img, format="png")
    img.seek(0)

    return send_file(img, mimetype="image/png")