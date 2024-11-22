from flask import Flask, render_template, send_file, request,redirect,url_for, session

def modificarDatos(conexion):

    user_id = session['user_id']

    try:
        # Obtener los datos actuales del usuario
        cursor = conexion.cursor()
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
            cursor = conexion.cursor()
            query = """
                UPDATE usuarios
                SET nombre_usuario = %s, correo = %s, contraseña = %s, ciudad = %s, status = %s
                WHERE id_usuario = %s
            """
            cursor.execute(query, (nombre, correo, contrasena, icono, status, user_id))
            conexion.commit()
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