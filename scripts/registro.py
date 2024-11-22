from flask import Flask, render_template, send_file, redirect,url_for, session, request

def registrar(conexion):

    if request.method == "POST":
        # Obtener datos del formulario
        nombre = request.form["name"]  
        correo = request.form["email"]  
        contrasena = request.form["password"]  
        ciudad = request.form["profileImage"] 
        status = True 

        try:
            # Insertar datos en la tabla 'usuarios'
            cursor = conexion.cursor()
            query = """
                INSERT INTO usuarios (nombre_usuario, correo, contraseña, ciudad, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, correo, contrasena, ciudad, status))
            conexion.commit()
            cursor.close()
            return redirect(url_for('login'))
        
        except Exception as e:
            print("Error al registrar usuario:", e)
            return "Ocurrió un error durante el registro"
        
    return render_template("registro.html")