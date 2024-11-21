from flask import Flask, render_template, send_file, Response #type: ignore
from scripts.analisisgastos import graficar 

app = Flask(__name__)

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/registro")
def registro():
    return render_template('registro.html')

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/notificaciones")
def notificaciones():
    return render_template("notificaciones.html")

@app.route("/movimientos")
def movimientos():
    return render_template("movimientos.html")

@app.route("/analisisgastos")
def analisis_gastos():
    return render_template("analisisgastos.html")

@app.route("/ahorros")
def ahorros():
    return render_template("ahorros.php")

@app.route("/pagos")
def pagos():
    return render_template("pagos.html")

@app.route("/grafica")
def graficarRuta():

    return graficar()

if __name__ == "__main__":

    app.run(debug = True)