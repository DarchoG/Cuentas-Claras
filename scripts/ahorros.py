from flask import Flask,render_template,request,redirect,Blueprint,session
import psycopg2
from psycopg2 import sql
import psycopg2.extras
import matplotlib.pyplot as plt
from datetime import datetime



def ahorros_info(conexion):
   tipo = 0
   if (tipo == 0):
     
       user_id = session['user_id']
       cursor = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
       query = """SELECT * FROM vista_ahorros_usuario WHERE id_usuario = %s and tipo_tarjeta = %s and status = true """
       cursor.execute(query,(user_id,'Débito'))
       res = cursor.fetchall()
       dinero_reservado_list = [row['dinero_reservado'] for row in res]
       dinero_disponible_list = [row['dinero_disponible'] for row in res]
       tipo_tarjeta = [row['tipo_tarjeta'] for row in res]
       data = {
           "dinero_reservado": dinero_reservado_list,
           "dinero_disponible": dinero_disponible_list,
           "tipo_tarjeta": tipo_tarjeta
       }
   elif (tipo == 1):
       user_id = session['user_id']
       cursor = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
       query = """SELECT * FROM vista_ahorros_usuario WHERE id_usuario = %s and tipo_tarjeta = %s and status = true"""
       cursor.execute(query,(user_id,'Credito'))
       res = cursor.fetchall()
       dinero_reservado_list = [row['dinero_reservado'] for row in res]
       dinero_disponible_list = [row['dinero_disponible'] for row in res]
       tipo_tarjeta = [row['tipo_tarjeta'] for row in res]
       data = {
           "dinero_reservado": dinero_reservado_list,
           "dinero_disponible": dinero_disponible_list,
           "tipo_tarjeta": tipo_tarjeta
       }


    
   cursor = conexion.cursor(cursor_factory=psycopg2.extras.DictCursor)
   query = "SELECT * FROM vista_ahorros_usuario WHERE id_usuario = 1 and tipo_tarjeta = 'Débito'"
   cursor.execute(query, )
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
       
       plt.savefig(r"static\img\credito.png",transparent=True)
       
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
       
       plt.savefig(r"static\img\grafico.png", transparent=True)
   return render_template('ahorros.html', data=data)

