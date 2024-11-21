from flask import Flask, render_template, send_file, request,redirect,url_for, session
from scripts.analisisgastos import graficar 
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

app.secret_key = 'mi_clave_secreta'

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/login", methods=["GET", "POST"])  
def login_post():
    if request.method == "POST":
        # Obtener los datos del formulario
        correo = request.form["email"]
        contrasena = request.form["password"]

        try:
            cursor = conn.cursor()
            query = "SELECT * FROM usuarios WHERE correo = %s AND contraseña = %s"
            cursor.execute(query, (correo, contrasena))
            usuario = cursor.fetchone()  # Buscar el primer usuario que coincida

            if usuario:
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
        nombre = request.form["name"]  
        correo = request.form["email"]  
        contrasena = request.form["password"]  
        ciudad = request.form["profileImage"] 
        status = True 

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

@app.route("/registro_movimiento")
def registro_movimiento():
    if 'user_id' not in session:  # Verificar si el usuario está autenticado
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado
    return render_template("registro_movimiento.html")

@app.route("/analisisgastos")
def analisis_gastos():
    if 'user_id' not in session:  # Verificar si el usuario está autenticado
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado
    return render_template("analisisgastos.html")

@app.route("/grafica")
def graficarRuta():

    return graficar()

@app.route("/ahorros")
def ahorros():
    if 'user_id' not in session:  # Verificar si el usuario está autenticado
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado
    return render_template("ahorros.html")

@app.route("/pagos")
def pagos():
    if 'user_id' not in session:  # Verificar si el usuario está autenticado
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado
    return render_template("pagos.html")

@app.route("/logout")
def logout():
    session.pop('user_id', None)  # Eliminar el ID de usuario de la sesión
    return redirect(url_for('login'))  # Redirigir al login

@app.route("/usuario_modifica", methods=["GET", "POST"])
def usuario_modifica():
    if 'user_id' not in session:  # Verificar si el usuario está autenticado
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado

    user_id = session['user_id']
    try:
        # Obtener los datos actuales del usuario
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
        usuario = cursor.fetchone()  # Obtener la información del usuario
        cursor.close()

        if request.method == "POST":
            nombre = request.form["name"]
            correo = request.form["email"]
            contrasena = request.form["password"]
            icono = request.form["profileImage"]
            status = True if 'deactivate_account' not in request.form else False  # Desactivar la cuenta si está marcado

            # Actualizar la información en la base de datos
            cursor = conn.cursor()
            query = """
                UPDATE usuarios
                SET nombre_usuario = %s, correo = %s, contraseña = %s, ciudad = %s, status = %s
                WHERE id_usuario = %s
            """
            cursor.execute(query, (nombre, correo, contrasena, icono, status, user_id))
            conn.commit()
            cursor.close()

            # Si el usuario desactivó su cuenta, cerrar sesión y redirigir al login
            if not status:
                session.pop('user_id', None)  # Eliminar el ID de usuario de la sesión
                return redirect(url_for('login'))  # Redirigir al login si el estado es 'false'

            return redirect(url_for('perfil_user'))

    except Exception as e:
        print("Error al modificar los datos del usuario:", e)
        return "Ocurrió un error al modificar los datos del perfil"

    return render_template("usuario_modifica.html", usuario=usuario)


@app.route("/perfil_user")
def perfil_user():
    if 'user_id' not in session:  # Verificar si el usuario está autenticado
        return redirect(url_for('login'))  # Redirigir al login si no está autenticado
    
    user_id = session['user_id']  # Obtener el ID del usuario desde la sesión
    usuario = None
    mensaje_error = None

    try:
        cursor = conn.cursor()
        query = "SELECT nombre_usuario, correo, ciudad FROM usuarios WHERE id_usuario = %s"
        cursor.execute(query, (user_id,))
        usuario = cursor.fetchone()
        cursor.close()
    except Exception as e:
        print("Error al recuperar datos del usuario:", e)
        mensaje_error = "Ocurrió un error al recuperar los datos del perfil."

    if usuario is None:
        mensaje_error = mensaje_error or "No se encontró el usuario."

    # Renderizar el template con los datos o con un mensaje de error
    return render_template('perfil_user.html', usuario=usuario, error=mensaje_error)

if __name__ == "__main__":

    app.run(debug = True)
