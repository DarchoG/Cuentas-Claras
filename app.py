from flask import Flask, render_template #type: ignore

app = Flask(__name__)

@app.route("/")
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

if __name__ == "__main__":

    app.run(debug = True)