from flask import Flask,render_template,request,url_for,redirect
import psycopg2
from psycopg2 import sql
import psycopg2.extras
import matplotlib.pyplot as plt
import numbers as np
app = Flask(__name__)



def get_db_connection():
    connection = psycopg2.connect(
        host='localhost',
        user='postgres',       # Asegúrate de que sea el usuario correcto
        password='depajo',     # Asegúrate de que la contraseña sea correcta
        database='SelfBank'    # Nombre de tu base de datos
    )
    return connection

@app.route('/ahorros', endpoint='ahorros')
def ahorros():
    #return "<h1>Hola mundo</h1>"
    cursor = get_db_connection().cursor(cursor_factory=psycopg2.extras.DictCursor) # se utiliza para obtener los datos en forma de diccionarios
    query = "SELECT * FROM vista_ahorros_usuario WHERE id_usuario = 1 and tipo_tarjeta = 'Débito'"
    cursor.execute(query)
    res = cursor.fetchall()                 # Asi como en php se obtiene el contenedor de datos
    dinero_reservado_list = [row['dinero_reservado'] for row in res]# Asi como en php se obtiene la columna de la consulta
    dinero_disponible_list = [row['dinero_disponible'] for row in res]
    tipo_tarjeta = [row['tipo_tarjeta'] for row in res]
    data = {
        "dinero_reservado": dinero_reservado_list,
        "dinero_disponible": dinero_disponible_list,
        "tipo_tarjeta": tipo_tarjeta
        
    }

    return render_template('ahorros.html',data=data)

def graficoCircular():
    cursor = get_db_connection().cursor(cursor_factory=psycopg2.extras.DictCursor)
    query = "SELECT * FROM vista_ahorros_usuario WHERE id_usuario = 1 and tipo_tarjeta = 'Débito'"
    cursor.execute(query)
    res = cursor.fetchall()                 # Asi como en php se obtiene el contenedor de datos
    tipo_tarjeta = "Débito"
    dinero_reservado= sum(row['dinero_reservado'] for row in res)# Asi como en php se obtiene la columna de la consulta
    dinero_disponible = sum(row['dinero_disponible'] for row in res)
    Ahorro = sum(row['ahorro_total'] for row in res)
    ingresos = sum(row['ingresos'] for row in res)
    gastos = sum(row['gastos'] for row in res)
    

    if(tipo_tarjeta=='Credito'):
        colores = [
        (52/255, 152/255, 219/255),  # Azul claro
        (231/255, 76/255, 60/255),   # Rojo coral
        
        ]
        data_grafica = [dinero_disponible,gastos]
        #nombres = ['dinero disponible', 'gastos']
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(data_grafica,colors =colores,autopct='%1.1f%%')
        ax.set_facecolor('none')
        
        plt.savefig(r"app\static\img\credito.png",transparent=True)
        
    elif(tipo_tarjeta=='Débito'):
        colores = [
        (52/255, 152/255, 219/255),  # Azul claro
        (46/255, 204/255, 113/255),  # Verde menta
        (241/255, 196/255, 15/255),  # Amarillo suave
        (231/255, 76/255, 60/255),   # Rojo coral
        (155/255, 89/255, 182/255)   # Púrpura pastel
        ]
        data_grafica = [dinero_disponible, dinero_reservado,Ahorro,ingresos,gastos]
        #nombres = ['dinero disponible','dinero reservado','Ahorro', 'ingresos', 'gastos']
        #labels=nombres
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(data_grafica,colors =colores,autopct='%1.1f%%')
        ax.set_facecolor('none')
        
        plt.savefig(r"app\static\img\grafico.png", transparent=True)

graficoCircular()   


@app.route('/dinero_reservado_actualizar', methods=['POST'])# Recibe el identificador del formulario del archivo html de donde se crea y solo es para tarejtas de debito
def actualizar_dinero_reservado():
    
    if request.method == 'POST':
        # Obtener el nuevo valor de 'dinero_reservado' desde el formulario
        dinero_reservado = request.form['dinero_reservado']
        # Lógica para actualizar el valor en la base de datos
        connection = get_db_connection()
        cursor = connection.cursor()
        # Actualizamos el valor de 'dinero_reservado' en la base de datos
        query = "UPDATE tarjetas SET dinero_reservado = %s  WHERE id_tarjeta = 1 and tipo_tarjeta = 'Débito'"
        cursor.execute(query, (dinero_reservado,))
        connection.commit() # se utiliza para confirmar consultas de tipo insert, update y delete, obligatorio para realizarlas
        query = "INSERT INTO movimientos (id_usuario, id_tarjeta, ingresos, egresos, descripcion_movimiento, fecha, tipo_tarjeta) VALUES (1, 1, 0, 0, 'Dinero reservado actualizado', '2024-11-18', 'Débito')"

        cursor.execute(query,)
        connection.commit()
        return redirect(url_for('ahorros'))


#def pagina_no_econtradas(error):
    #return render_template('404.html'), 404
 #   return redirect(url_for('ahorros'))

if __name__ == '__main__':
  #  app.register_error_handler(404,pagina_no_econtradas)
    
    app.run(debug=True)

