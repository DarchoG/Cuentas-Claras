from flask import Flask, render_template, send_file, request, redirect, url_for, session
from datetime import datetime

def actualizar_dinero_reservado(conexion,):
    user_id = session['user_id']
    tipo_tarjeta = session['tarjeta'] 
    correo = session['correo']
    if request.method == 'POST':
        # Obtener el nuevo valor de 'dinero_reservado' desde el formulario
        dinero_reservado = request.form['dinero_reservado']
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime('%d/%m/%Y')

        #Obtener id de la tarjeta
        cursor = conexion.cursor()
        query = "SELECT id_tarjeta FROM usuariotarjetas WHERE correo=%s AND tipo_tarjeta=%s"
        cursor.execute(query, (correo, tipo_tarjeta))

        # Obtiene el resultado
        id_tarjeta = cursor.fetchone()
        # Actualizar el valor en la base de datos
        cursor = conexion.cursor()
        query = "UPDATE tarjetas SET dinero_reservado = %s WHERE id_tarjeta = %s and tipo_tarjeta = %s"
        cursor.execute(query, (dinero_reservado,id_tarjeta,tipo_tarjeta))
        conexion.commit()

        # Registrar el movimiento (si es necesario)
        query = """
            INSERT INTO movimientos (id_usuario, id_tarjeta, ingresos, egresos, descripcion_movimiento, fecha, tipo_tarjeta,reservado)
            VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
        """
        cursor.execute(query, (user_id, id_tarjeta, 0, 0, 'Dinero reservado actualizado', fecha_formateada, tipo_tarjeta,True))
        conexion.commit()

        # Redirigir de vuelta a la página de ahorros
        return redirect(url_for('ahorros'))
