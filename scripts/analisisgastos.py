from flask import Flask, render_template, send_file, redirect,url_for, session, request
import io
import base64
from flask import send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns

def obtenerInformacion(conexion):

    cursor = conexion.cursor()
    # cursor.execute('SELECT * FROM movimientos;')
    # usuarios = cursor.fetchall()
    cursor.close()

def graficar(conexion):

    obtenerInformacion(conexion)

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