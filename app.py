from flask import Flask, render_template, request,redirect,url_for
import psycopg2

app = Flask(__name__)


# Configuración de conexión con PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port="5433",
    dbname="selfbank",
    user="postgres",
    password="1234",
    options="-c client_encoding=UTF8"
)

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        # Obtener datos del formulario
        nombre = request.form["name"]  # Nombre del usuario
        correo = request.form["email"]  # Correo del usuario
        contrasena = request.form["password"]  # Contraseña
        ciudad = request.form["profileImage"]  # Ruta de la imagen seleccionada
        status = True  # Estado inicial por defecto

        try:
            # Insertar datos en la tabla 'usuarios'
            cursor = conn.cursor()
            query = """
                INSERT INTO usuarios (nombre_usuario, correo, contraseña, ciudad, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, correo, contrasena, ciudad, status))
            conn.commit()
            cursor.close()
            return redirect(url_for('login'))
        except Exception as e:
            print("Error al registrar usuario:", e)
            return "Ocurrió un error durante el registro"
    return render_template("registro.html")


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

if __name__ == "__main__":

    app.run(debug = True)