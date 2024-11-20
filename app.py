from flask import Flask, render_template, request,redirect,url_for, session
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

# Configurar clave secreta para las sesiones
app.secret_key = 'mi_clave_secreta'

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/login", methods=["GET", "POST"])  # Ruta para el login
def login_post():
    if request.method == "POST":
        # Obtener los datos del formulario
        correo = request.form["email"]
        contrasena = request.form["password"]

        try:
            # Verificar las credenciales en la base de datos
            cursor = conn.cursor()
            query = "SELECT * FROM usuarios WHERE correo = %s AND contraseña = %s"
            cursor.execute(query, (correo, contrasena))
            usuario = cursor.fetchone()  # Buscar el primer usuario que coincida

            if usuario:
                # Si el usuario existe, almacenar su ID en la sesión
                session['user_id'] = usuario[0]  # Almacenar el ID del usuario en la sesión
                return redirect(url_for('index'))  # Redirigir al índice (página principal)
            else:
                return "Credenciales incorrectas, intenta de nuevo."

        except Exception as e:
            print("Error al iniciar sesión:", e)
            return "Ocurrió un error durante el inicio de sesión"

    return render_template("login.html")

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
    if 'user_id' not in session:  # Verificar si el usuario está autenticado
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado
    return render_template('index.html')

@app.route("/notificaciones")
def notificaciones():
    if 'user_id' not in session:  # Verificar si el usuario está autenticado
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado
    return render_template("notificaciones.html")

@app.route("/movimientos")
def movimientos():
    if 'user_id' not in session:  # Verificar si el usuario está autenticado
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado
    return render_template("movimientos.html")

@app.route("/analisisgastos")
def analisis_gastos():
    if 'user_id' not in session:  # Verificar si el usuario está autenticado
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado
    return render_template("analisisgastos.html")

@app.route("/ahorros")
def ahorros():
    if 'user_id' not in session:  # Verificar si el usuario está autenticado
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado
    return render_template("ahorros.php")

@app.route("/pagos")
def pagos():
    if 'user_id' not in session:  # Verificar si el usuario está autenticado
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado
    return render_template("pagos.html")

@app.route("/logout")
def logout():
    session.pop('user_id', None)  # Eliminar el ID de usuario de la sesión
    return redirect(url_for('login'))  # Redirigir al login

@app.route("/usuario_modifica")
def usuario_modifica():
    if 'user_id' not in session:  # Verificar si el usuario está autenticado
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado
    return render_template('usuario_modifica.html')

@app.route("/perfil_user")
def perfil_user():
    if 'user_id' not in session:  # Verificar si el usuario está autenticado
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado
    return render_template('perfil_user.html')

if __name__ == "__main__":

    app.run(debug = True)