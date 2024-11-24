from flask import Flask, render_template, send_file, redirect,url_for, session, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import io

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

    img = io.BytesIO()
    fig.savefig(img, format="png", bbox_inches="tight", transparent=True)
    img.seek(0)

    return send_file(img, mimetype="image/png")

def graficar(conexion):

    ingresos, egresos = obtenerInformacion(conexion)
    meses = obtenerMeses(ingresos)

    ingresosMeses = agruparIngresos(ingresos)
    reservadoMeses, egresosMeses =  agruparEgresos(egresos)

    print("Ingresos: ", ingresosMeses)
    print("Reservado: ", reservadoMeses)
    print("Egresos:", egresosMeses)
    print("Meses:", meses)
        
    fig, ax = plt.subplots(figsize=(3.5, 6))
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

    img = io.BytesIO()
    fig.savefig(img, format="png", bbox_inches="tight", transparent=True)
    img.seek(0)

    return send_file(img, mimetype="image/png")

def graficarStatus(conexion):

    ingresos, egresos = obtenerInformacion(conexion)
    _ , egresosMeses =  agruparEgresos(egresos)

    ingresosTotales = sum(monto for monto, _ in ingresos)
    egresosTotales = sum(egresosMeses)

    montoTotal = ingresosTotales + egresosTotales
    porcentajeIngresos = egresosTotales / montoTotal

    segmentos = [0.2, 0.2, 0.2, 0.2, 0.2]
    colores = ['#6fbf44', '#efb025', '#f08036', '#ef4b3f', '#ce2335']
    imagenes = ['static/img/Emoji1.png', 'static/img/Emoji2.png', 'static/img/Emoji3.png', 'static/img/Emoji4.png', 'static/img/Emoji5.png']
    flecha = 'static/img/Flecha.png'

    posiciones = []
    acumulador = 0

    for segmento in segmentos:

        posiciones.append(acumulador)
        acumulador += segmento

    fig, ax = plt.subplots(figsize=(8, 2))

    for i, (inicio, ancho, color) in enumerate(zip(posiciones, segmentos, colores)):
        ax.barh(y=0, width=ancho, left=inicio, color=color, height=1)

        img = mpimg.imread(imagenes[i])
        image_box = OffsetImage(img, zoom=0.4)  # Ajusta el tamaño con zoom
        ab = AnnotationBbox(image_box, (inicio + ancho / 2, 2), frameon=False, box_alignment=(0.5, 0.5))
        ax.add_artist(ab)
        
    img_flecha = mpimg.imread(flecha)
    image_box_flecha = OffsetImage(img_flecha, zoom=0.05)  # Ajusta el tamaño de la flecha

    ab_flecha = AnnotationBbox(image_box_flecha, (porcentajeIngresos, -2), frameon=False, box_alignment=(0.5, 0.5))
    ax.add_artist(ab_flecha)

    ax.set_xlim(0, 1)
    ax.set_ylim(-3.5, 3.5)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.axis('off')

    img = io.BytesIO()
    fig.savefig(img, format="png", bbox_inches="tight", transparent=True)
    img.seek(0)

    return send_file(img, mimetype="image/png")