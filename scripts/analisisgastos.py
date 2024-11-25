from flask import Flask, render_template, send_file, redirect,url_for, session, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.pagesizes import letter
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import io
import os

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

def obtenerDatosPDF(conexion):

    cursor = conexion.cursor()
    cursor.execute('SELECT nombre_usuario, correo FROM usuarios WHERE id_usuario = %s;', (session.get('user_id'),))
    usuario = cursor.fetchall()
    cursor.execute('SELECT tipo_tarjeta, numero_tarjeta, dinero_disponible FROM tarjetas WHERE id_usuario = %s AND status;', (session.get('user_id'),))
    tarjetas = cursor.fetchall()
    cursor.execute('SELECT ingresos, descripcion_movimiento, fecha FROM movimientos WHERE id_usuario = %s AND ingresos != 0;', (session.get('user_id'),))
    ingresos = cursor.fetchall()
    cursor.execute('SELECT egresos, descripcion_movimiento, fecha FROM movimientos WHERE id_usuario = %s AND egresos != 0;', (session.get('user_id'),))
    egresos = cursor.fetchall()
    cursor.close()

    return usuario, tarjetas, ingresos, egresos

def organizarMovimientos(ingresos, egresos):

    movimientos = []

    for monto, movimiento, fecha in ingresos:

        movimientos.append([fecha, movimiento, monto])
    
    for monto, movimiento, fecha in egresos:

        movimientos.append([fecha, movimiento, monto * -1])

    ordenarMovimientos = sorted(movimientos, key=lambda x: x[0])

    return ordenarMovimientos

def generarPDF(conexion):

    fecha = datetime.now()
    resultado = f"_{fecha.year}_{fecha.month:02d}_{fecha.day:02d}_{fecha.hour:02d}_{fecha.minute:02d}_{fecha.second:02d}"
    filename = (f"Estado_Cuenta{resultado}.pdf")

    doc = SimpleDocTemplate(
        filename, 
        pagesize=letter,
        leftMargin=72,  
        rightMargin=72, 
        topMargin=72,    
        bottomMargin=72 
    )

    elements = []

    # --- Usuarios --- #

    usuario, tarjetas, ingresos, egresos = obtenerDatosPDF(conexion)
    movimientos = organizarMovimientos(ingresos, egresos)

    nombreUsuario, correoUsuario = usuario[0]

    usuarioData = [
        ['Nombre', nombreUsuario],
        ['Correo', correoUsuario],
    ]

    usuarioTable = Table(usuarioData)

    style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'), 
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'), 
        ])

    usuarioTable.setStyle(style)

    # ---- Tarjetas ---- #

    tarjetasData = [
        ['Tarjeta', 'Tipo', 'Saldo Disponible'],
    ]
    
    for tipo, numero, saldo in tarjetas:

        numero = numero[-4:]

        tarjetasData.append([f"*{numero}", tipo, f"${saldo:.2f}"])

    tarjetasTable = Table(tarjetasData)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), (0.5, 0.5, 0.5)),
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), (1, 1, 1)),
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
    ])

    tarjetasTable.setStyle(style)

    usuarioTarjetas = Table([[usuarioTable, tarjetasTable]], colWidths=[300, 200])

    usuarioTarjetas.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),   # Primera tabla alineada a la izquierda
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'), # Segunda tabla alineada a la derecha
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    # --- Movimientos --- #

    dataMovimientos= [['Fecha', 'Descripción', 'Monto']]

    for movimiento in movimientos:

        fecha = movimiento[0].strftime("%Y-%m-%d")
        descripcion = movimiento[1]

        if(movimiento[2] >= 0):   
            monto = f"${abs(movimiento[2]):,.2f}"
        else:
            monto = f"-${abs(movimiento[2]):,.2f}"

        dataMovimientos.append([fecha, descripcion, monto])

    table = Table(dataMovimientos)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), (0.5, 0.5, 0.5)),
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centrado para las otras columnas
        ('ALIGN', (2, 1), (-1, -1), 'LEFT'),  # Alineación a la izquierda solo para la columna 'Monto'
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), (1, 1, 1)),
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))
    ])

    table.setStyle(style)

    elements.append(usuarioTarjetas)
    elements.append(Spacer(1, 40))
    elements.append(table)

    # Generar el PDF
    doc.build(elements)

    os.startfile(filename)