from flask import Flask, render_template, send_file, request,redirect,url_for, session  

def obtenerPerfil(conexion):

    user_id = session['user_id']  # Obtener el ID del usuario desde la sesión
    usuario = None
    mensaje_error = None

    try:
        cursor = conexion.cursor()
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