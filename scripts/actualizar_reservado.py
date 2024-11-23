from flask import Flask, render_template, send_file, request, redirect, url_for, session
from datetime import datetime

def actualizar_dinero_reservado(conexion):
    user_id = session['user_id']
    if request.method == 'POST':
        # Obtener el nuevo valor de 'dinero_reservado' desde el formulario
        dinero_reservado = request.form['dinero_reservado']
        fecha_actual = datetime.now()
        fecha_formateada = fecha_actual.strftime('%d/%m/%Y')

        # Actualizar el valor en la base de datos
        cursor = conexion.cursor()
        query = "UPDATE tarjetas SET dinero_reservado = %s WHERE id_tarjeta = 1 and tipo_tarjeta = 'Débito'"
        cursor.execute(query, (dinero_reservado,))
        conexion.commit()

        # Registrar el movimiento (si es necesario)
        query = """
            INSERT INTO movimientos (id_usuario, id_tarjeta, ingresos, egresos, descripcion_movimiento, fecha, tipo_tarjeta,reservado)
            VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
        """
        cursor.execute(query, (user_id, 1, 0, 0, 'Dinero reservado actualizado', fecha_formateada, 'Débito',True))
        conexion.commit()

        # Redirigir de vuelta a la página de ahorros
        return redirect(url_for('ahorros'))