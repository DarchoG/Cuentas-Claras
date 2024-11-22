from flask import Flask, render_template, send_file, redirect,url_for, session, request

def loginStatus(conexion):

    if request.method == "POST":
        # Obtener los datos del formulario
        correo = request.form["email"]
        contrasena = request.form["password"]

        try:
            cursor = conexion.cursor()
            query = "SELECT * FROM usuarios WHERE correo = %s AND contraseña = %s"
            cursor.execute(query, (correo, contrasena))
            usuario = cursor.fetchone()

            if usuario:
                session['user_id'] = usuario[0]
                return redirect(url_for('index'))
            else:
                return "Credenciales incorrectas, intenta de nuevo."

        except Exception as e:
            print("Error al iniciar sesión:", e)
            return "Ocurrió un error durante el inicio de sesión"

    return render_template("login.html")