from flask import Flask, render_template, send_file, request, redirect, url_for, session
from functools import wraps
from scripts.analisisgastos import graficar
from scripts.login import loginStatus
from scripts.registro import registrar
from scripts.modificar import modificarDatos
from scripts.perfil import obtenerPerfil
import psycopg2

app = Flask(__name__)

# Configuración de conexión con PostgreSQL

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="selfbank",
    user="postgres",
    password="1234",
    options="-c client_encoding=UTF8"
)

app.secret_key = 'mi_clave_secreta'

# Decorador personalizado para verificar autenticación

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/login", methods=["GET", "POST"])  
def login_post():
    return loginStatus(conn)

@app.route("/registro", methods=["GET", "POST"])
def registro():
    return registrar(conn)

@app.route("/index")
@login_required
def index():
    return render_template('index.html')

@app.route("/notificaciones")
@login_required
def notificaciones():
    return render_template("notificaciones.html")

@app.route("/movimientos")
@login_required
def movimientos():
    return render_template("movimientos.html")

@app.route("/registro_movimiento")
@login_required
def registro_movimiento():
    return render_template("registro_movimiento.html")

@app.route("/analisisgastos")
@login_required
def analisis_gastos():
    return render_template("analisisgastos.html")

@app.route("/grafica")
def graficarRuta():
    return graficar(conn)

@app.route("/ahorros")
@login_required
def ahorros():
    return render_template("ahorros.html")

@app.route("/pagos")
@login_required
def pagos():
    return render_template("pagos.html")

@app.route("/logout")
def logout():
    session.pop('user_id', None)  # Eliminar el ID de usuario de la sesión
    return redirect(url_for('login'))

@app.route("/usuario_modifica", methods=["GET", "POST"])
@login_required
def usuario_modifica():
    return modificarDatos(conn)

@app.route("/perfil_user")
@login_required
def perfil_user():
    return obtenerPerfil(conn)

if __name__ == "__main__":
    app.run(debug=True)
