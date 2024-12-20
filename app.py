from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import boto3
import logging
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config.from_object('config')

mysql = MySQL(app)

# Configuración de Amazon Lex V2
lex_client = boto3.client('lexv2-runtime')

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)

socketio = SocketIO(app)

@app.route('/')
def inicio():
    return render_template('base.html')

@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    try:
        if request.method == 'POST':
            nombre = request.form['nombre']
            email = request.form['email']
            telefono = request.form['telefono']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO usuarios (nombre, email, telefono) VALUES (%s, %s, %s)", (nombre, email, telefono))
            mysql.connection.commit()
            cur.close()
            flash('Usuario agregado exitosamente', 'success')
            return redirect(url_for('usuarios'))
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios")
        usuarios = cur.fetchall()
        cur.close()
        return render_template('usuarios.html', usuarios=usuarios)
    except Exception as e:
        logging.error(f"Error en la ruta /usuarios: {e}")
        flash('Ocurrió un error al procesar la solicitud', 'danger')
        return redirect(url_for('inicio'))

@app.route('/usuarios/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    try:
        if request.method == 'POST':
            nombre = request.form['nombre']
            email = request.form['email']
            telefono = request.form['telefono']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE usuarios SET nombre=%s, email=%s, telefono=%s WHERE id=%s", (nombre, email, telefono, id))
            mysql.connection.commit()
            cur.close()
            flash('Usuario actualizado exitosamente', 'success')
            return redirect(url_for('usuarios'))
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE id=%s", (id,))
        usuario = cur.fetchone()
        cur.close()
        return render_template('editar_usuario.html', usuario=usuario)
    except Exception as e:
        logging.error(f"Error en la ruta /usuarios/{id}: {e}")
        flash('Ocurrió un error al procesar la solicitud', 'danger')
        return redirect(url_for('usuarios'))

@app.route('/usuarios/eliminar/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM usuarios WHERE id=%s", (id,))
        mysql.connection.commit()
        cur.close()
        flash('Usuario eliminado exitosamente', 'success')
        return redirect(url_for('usuarios'))
    except Exception as e:
        logging.error(f"Error en la ruta /usuarios/eliminar/{id}: {e}")
        flash('Ocurrió un error al procesar la solicitud', 'danger')
        return redirect(url_for('usuarios'))

@app.route('/libros', methods=['GET', 'POST'])
def libros():
    try:
        if request.method == 'POST':
            titulo = request.form['titulo']
            autor = request.form['autor']
            precio = request.form['precio']
            fecha_publicacion = request.form['fecha_publicacion']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO libros (titulo, autor, precio, fecha_publicacion) VALUES (%s, %s, %s, %s)", (titulo, autor, precio, fecha_publicacion))
            mysql.connection.commit()
            cur.close()
            flash('Libro agregado exitosamente', 'success')
            return redirect(url_for('libros'))
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM libros")
        libros = cur.fetchall()
        cur.close()
        return render_template('libros.html', libros=libros)
    except Exception as e:
        logging.error(f"Error en la ruta /libros: {e}")
        flash('Ocurrió un error al procesar la solicitud', 'danger')
        return redirect(url_for('inicio'))

@app.route('/libros/<int:id>', methods=['GET', 'POST'])
def editar_libro(id):
    try:
        if request.method == 'POST':
            titulo = request.form['titulo']
            autor = request.form['autor']
            precio = request.form['precio']
            fecha_publicacion = request.form['fecha_publicacion']
            cur = mysql.connection.cursor()
            cur.execute("UPDATE libros SET titulo=%s, autor=%s, precio=%s, fecha_publicacion=%s WHERE id=%s", (titulo, autor, precio, fecha_publicacion, id))
            mysql.connection.commit()
            cur.close()
            flash('Libro actualizado exitosamente', 'success')
            return redirect(url_for('libros'))
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM libros WHERE id=%s", (id,))
        libro = cur.fetchone()
        cur.close()
        return render_template('editar_libro.html', libro=libro)
    except Exception as e:
        logging.error(f"Error en la ruta /libros/{id}: {e}")
        flash('Ocurrió un error al procesar la solicitud', 'danger')
        return redirect(url_for('libros'))

@app.route('/libros/eliminar/<int:id>', methods=['POST'])
def eliminar_libro(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM libros WHERE id=%s", (id,))
        mysql.connection.commit()
        cur.close()
        flash('Libro eliminado exitosamente', 'success')
        return redirect(url_for('libros'))
    except Exception as e:
        logging.error(f"Error en la ruta /libros/eliminar/{id}: {e}")
        flash('Ocurrió un error al procesar la solicitud', 'danger')
        return redirect(url_for('libros'))

@app.route('/prestamos', methods=['GET', 'POST'])
def prestamos():
    try:
        if request.method == 'POST':
            cliente_id = request.form['cliente_id']
            libro_id = request.form['libro_id']
            fecha_venta = request.form['fecha_venta']
            cantidad = request.form['cantidad']
            cur = mysql.connection.cursor()
            cur.execute("SELECT precio FROM libros WHERE id=%s", (libro_id,))
            precio_libro = cur.fetchone()[0]
            total = precio_libro * int(cantidad)
            cur.execute("INSERT INTO prestamos (cliente_id, libro_id, fecha_venta, cantidad, total) VALUES (%s, %s, %s, %s, %s)", (cliente_id, libro_id, fecha_venta, cantidad, total))
            mysql.connection.commit()
            cur.close()
            flash('Préstamo agregado exitosamente', 'success')
            return redirect(url_for('prestamos'))
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM prestamos")
        prestamos = cur.fetchall()
        cur.close()
        return render_template('prestamos.html', prestamos=prestamos)
    except Exception as e:
        logging.error(f"Error en la ruta /prestamos: {e}")
        flash('Ocurrió un error al procesar la solicitud', 'danger')
        return redirect(url_for('inicio'))

@app.route('/prestamos/<int:id>', methods=['GET', 'POST'])
def editar_prestamo(id):
    try:
        if request.method == 'POST':
            cliente_id = request.form['cliente_id']
            libro_id = request.form['libro_id']
            fecha_venta = request.form['fecha_venta']
            cantidad = request.form['cantidad']
            cur = mysql.connection.cursor()
            cur.execute("SELECT precio FROM libros WHERE id=%s", (libro_id,))
            precio_libro = cur.fetchone()[0]
            total = precio_libro * int(cantidad)
            cur.execute("UPDATE prestamos SET cliente_id=%s, libro_id=%s, fecha_venta=%s, cantidad=%s, total=%s WHERE id=%s", (cliente_id, libro_id, fecha_venta, cantidad, total, id))
            mysql.connection.commit()
            cur.close()
            flash('Préstamo actualizado exitosamente', 'success')
            return redirect(url_for('prestamos'))
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM prestamos WHERE id=%s", (id,))
        prestamo = cur.fetchone()
        cur.close()
        return render_template('editar_prestamo.html', prestamo=prestamo)
    except Exception as e:
        logging.error(f"Error en la ruta /prestamos/{id}: {e}")
        flash('Ocurrió un error al procesar la solicitud', 'danger')
        return redirect(url_for('prestamos'))

@app.route('/prestamos/eliminar/<int:id>', methods=['POST'])
def eliminar_prestamo(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM prestamos WHERE id=%s", (id,))
        mysql.connection.commit()
        cur.close()
        flash('Préstamo eliminado exitosamente', 'success')
        return redirect(url_for('prestamos'))
    except Exception as e:
        logging.error(f"Error en la ruta /prestamos/eliminar/{id}: {e}")
        flash('Ocurrió un error al procesar la solicitud', 'danger')
        return redirect(url_for('prestamos'))

@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        mensaje_usuario = request.form['message']
        response = lex_client.recognize_text(
            botId='MXTYHRLQFY',
            botAliasId='TSTALIASID',
            localeId='es_US',
            sessionId='User',
            text=mensaje_usuario
        )
        mensaje_respuesta = response['messages'][0]['content']
        
        # Lógica para aplicar cambios a la base de datos basada en los intents de Amazon Lex
        intent_name = response['interpretations'][0]['intent']['name']
        slots = response['interpretations'][0]['intent']['slots']
        
        if intent_name == "CrearUsuario":
            nombre = slots['nombre']['value']['interpretedValue'] if slots['nombre'] and 'interpretedValue' in slots['nombre']['value'] else None
            email = slots['email']['value']['interpretedValue'] if slots['email'] and 'interpretedValue' in slots['email']['value'] else None
            telefono = slots['telefono']['value']['interpretedValue'] if slots['telefono'] and 'interpretedValue' in slots['telefono']['value'] else None
            if nombre and email and telefono:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO usuarios (nombre, email, telefono) VALUES (%s, %s, %s)", (nombre, email, telefono))
                mysql.connection.commit()
                cur.close()
                mensaje_respuesta += " - Usuario agregado exitosamente."
            else:
                mensaje_respuesta += " - Faltan datos para agregar el usuario."
        elif intent_name == "EditarUsuario":
            logging.debug(f"EditarUsuario - Slots: {slots}")
            nombre = slots['nombre']['value']['interpretedValue'] if slots['nombre'] and 'interpretedValue' in slots['nombre']['value'] else None
            campo = slots['campo']['value']['interpretedValue'] if slots['campo'] and 'interpretedValue' in slots['campo']['value'] else slots['campo']['value']['originalValue'] if slots['campo'] and 'originalValue' in slots['campo']['value'] else None
            valor = slots['valor']['value']['interpretedValue'] if slots['valor'] and 'interpretedValue' in slots['valor']['value'] else slots['valor']['value']['originalValue'] if slots['valor'] and 'originalValue' in slots['valor']['value'] else None

            logging.debug(f"EditarUsuario - Nombre: {nombre}, Campo: {campo}, Valor: {valor}")

            if nombre and campo and valor:
                cur = mysql.connection.cursor()
                if campo.lower() == "correo":
                    cur.execute("UPDATE usuarios SET email=%s WHERE nombre=%s", (valor, nombre))
                elif campo.lower() == "teléfono":
                    cur.execute("UPDATE usuarios SET telefono=%s WHERE nombre=%s", (valor, nombre))
                elif campo.lower() == "nombre":
                    cur.execute("UPDATE usuarios SET nombre=%s WHERE nombre=%s", (valor, nombre))
                mysql.connection.commit()
                cur.close()
                mensaje_respuesta += " - Usuario actualizado exitosamente."
            else:
                mensaje_respuesta += " - Faltan datos para actualizar el usuario."
        
        socketio.emit('chatbot_response', {'message': mensaje_respuesta})
        return mensaje_respuesta
    except Exception as e:
        logging.error(f"Error en la ruta /chatbot: {e}")
        return "Ocurrió un error al procesar la solicitud", 500

if __name__ == '__main__':
    socketio.run(app, debug=True)