from flask import Flask, render_template, send_file, redirect, url_for, session, request

def loginStatus(conexion):
    if request.method == "POST":
        # Obtener los datos del formulario
        correo = request.form["email"]
        contrasena = request.form["password"]

        try:
            cursor = conexion.cursor()
            
            # Consulta para validar las credenciales del usuario
            query = "SELECT * FROM usuarios WHERE correo = %s AND contraseña = %s"
            cursor.execute(query, (correo, contrasena))
            usuario = cursor.fetchone()

            if usuario:
                # Establecer sesión para el usuario
                session['user_id'] = usuario[0]
                session['correo'] = correo
                session['tarjeta'] = 'Débito'  # Tarjeta por defecto

                # Consulta para obtener el id_tarjeta de tipo 'Débito' por defecto
                query_tarjeta = """
                    SELECT id_tarjeta 
                    FROM usuariotarjetas 
                    WHERE correo = %s AND tipo_tarjeta = 'Débito' 
                    LIMIT 1
                """
                cursor.execute(query_tarjeta, (correo,))
                id_tarjeta = cursor.fetchone()
                session['id_tarjeta'] = int(id_tarjeta[0])# Establecer el id_tarjeta en la sesión

                return redirect(url_for('index'))
            else:
                return "Credenciales incorrectas, intenta de nuevo."

        except Exception as e:
            print("Error al iniciar sesión:", e)
            return "Ocurrió un error durante el inicio de sesión"

    return render_template("login.html")
