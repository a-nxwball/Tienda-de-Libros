from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import boto3
import logging
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config.from_object('config')

# Configuración de pymysql
def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor
    )

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
    connection = get_db_connection()
    try:
        if request.method == 'POST':
            nombre = request.form['nombre']
            email = request.form['email']
            telefono = request.form['telefono']
            with connection.cursor() as cur:
                cur.execute("INSERT INTO usuarios (nombre, email, telefono) VALUES (%s, %s, %s)", (nombre, email, telefono))
                connection.commit()
            flash('Usuario agregado exitosamente', 'success')
            return redirect(url_for('usuarios'))
        with connection.cursor() as cur:
            cur.execute("SELECT * FROM usuarios")
            usuarios = cur.fetchall()
        return render_template('usuarios.html', usuarios=usuarios)
    except Exception as e:
        logging.error(f"Error en la ruta /usuarios: {e}")
        flash('Ocurrió un error al procesar la solicitud', 'danger')
        return redirect(url_for('inicio'))
    finally:
        connection.close()

@app.route('/usuarios/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    connection = get_db_connection()
    try:
        if request.method == 'POST':
            nombre = request.form['nombre']
            email = request.form['email']
            telefono = request.form['telefono']
            with connection.cursor() as cur:
                cur.execute("UPDATE usuarios SET nombre=%s, email=%s, telefono=%s WHERE id=%s", (nombre, email, telefono, id))
                connection.commit()
            flash('Usuario actualizado exitosamente', 'success')
            return redirect(url_for('usuarios'))
        with connection.cursor() as cur:
            cur.execute("SELECT * FROM usuarios WHERE id=%s", (id,))
            usuario = cur.fetchone()
        return render_template('editar_usuario.html', usuario=usuario)
    except Exception as e:
        logging.error(f"Error en la ruta /usuarios/{id}: {e}")
        flash('Ocurrió un error al procesar la solicitud', 'danger')
        return redirect(url_for('usuarios'))
    finally:
        connection.close()

@app.route('/usuarios/eliminar/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cur:
            cur.execute("DELETE FROM usuarios WHERE id=%s", (id,))
            connection.commit()
        flash('Usuario eliminado exitosamente', 'success')
        return redirect(url_for('usuarios'))
    except Exception as e:
        logging.error(f"Error en la ruta /usuarios/eliminar/{id}: {e}")
        flash('Ocurrió un error al procesar la solicitud', 'danger')
        return redirect(url_for('usuarios'))
    finally:
        connection.close()

@app.route('/libros', methods=['GET', 'POST'])
def libros():
    connection = get_db_connection()
    try:
        if request.method == 'POST':
            titulo = request.form['titulo']
            autor = request.form['autor']
            precio = request.form['precio']
            fecha_publicacion = request.form['fecha_publicacion']
            with connection.cursor() as cur:
                cur.execute("INSERT INTO libros (titulo, autor, precio, fecha_publicacion) VALUES (%s, %s, %s, %s)", (titulo, autor, precio, fecha_publicacion))
                connection.commit()
            flash('Libro agregado exitosamente', 'success')
            return redirect(url_for('libros'))
        with connection.cursor() as cur:
            cur.execute("SELECT * FROM libros")
            libros = cur.fetchall()
        return render_template('libros.html', libros=libros)
    except Exception as e:
        logging.error(f"Error en la ruta /libros: {e}")
        flash('Ocurrió un error al procesar la solicitud', 'danger')
        return redirect(url_for('inicio'))
    finally:
        connection.close()

@app.route('/libros/<int:id>', methods=['GET', 'POST'])
def editar_libro(id):
    connection = get_db_connection()
    try:
        if request.method == 'POST':
            titulo = request.form['titulo']
            autor = request.form['autor']
            precio = request.form['precio']
            fecha_publicacion = request.form['fecha_publicacion']
            with connection.cursor() as cur:
                cur.execute("UPDATE libros SET titulo=%s, autor=%s, precio=%s, fecha_publicacion=%s WHERE id=%s", (titulo, autor, precio, fecha_publicacion, id))
                connection.commit()
            flash('Libro actualizado exitosamente', 'success')
            return redirect(url_for('libros'))
        with connection.cursor() as cur:
            cur.execute("SELECT * FROM libros WHERE id=%s", (id,))
            libro = cur.fetchone()
        return render_template('editar_libro.html', libro=libro)
    except Exception as e:
        logging.error(f"Error en la ruta /libros/{id}: {e}")
        flash('Ocurrió un error al procesar la solicitud', 'danger')
        return redirect(url_for('libros'))
    finally:
        connection.close()

@app.route('/libros/eliminar/<int:id>', methods=['POST'])
def eliminar_libro(id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cur:
            cur.execute("DELETE FROM libros WHERE id=%s", (id,))
            connection.commit()
        flash('Libro eliminado exitosamente', 'success')
        return redirect(url_for('libros'))
    except Exception as e:
        logging.error(f"Error en la ruta /libros/eliminar/{id}: {e}")
        flash('Ocurrió un error al procesar la solicitud', 'danger')
        return redirect(url_for('libros'))
    finally:
        connection.close()

@app.route('/prestamos', methods=['GET', 'POST'])
def prestamos():
    connection = get_db_connection()
    try:
        if request.method == 'POST':
            cliente_id = request.form['cliente_id']
            libro_id = request.form['libro_id']
            fecha_venta = request.form['fecha_venta']
            cantidad = request.form['cantidad']
            with connection.cursor() as cur:
                cur.execute("SELECT precio FROM libros WHERE id=%s", (libro_id,))
                precio_libro = cur.fetchone()['precio']
                total = precio_libro * int(cantidad)
                cur.execute("INSERT INTO prestamos (cliente_id, libro_id, fecha_venta, cantidad, total) VALUES (%s, %s, %s, %s, %s)", (cliente_id, libro_id, fecha_venta, cantidad, total))
                connection.commit()
            flash('Préstamo agregado exitosamente', 'success')
            return redirect(url_for('prestamos'))
        with connection.cursor() as cur:
            cur.execute("SELECT * FROM prestamos")
            prestamos = cur.fetchall()
        return render_template('prestamos.html', prestamos=prestamos)
    except Exception as e:
        logging.error(f"Error en la ruta /prestamos: {e}")
        flash('Ocurrió un error al procesar la solicitud', 'danger')
        return redirect(url_for('inicio'))
    finally:
        connection.close()

@app.route('/prestamos/<int:id>', methods=['GET', 'POST'])
def editar_prestamo(id):
    connection = get_db_connection()
    try:
        if request.method == 'POST':
            cliente_id = request.form['cliente_id']
            libro_id = request.form['libro_id']
            fecha_venta = request.form['fecha_venta']
            cantidad = request.form['cantidad']
            with connection.cursor() as cur:
                cur.execute("SELECT precio FROM libros WHERE id=%s", (libro_id,))
                precio_libro = cur.fetchone()['precio']
                total = precio_libro * int(cantidad)
                cur.execute("UPDATE prestamos SET cliente_id=%s, libro_id=%s, fecha_venta=%s, cantidad=%s, total=%s WHERE id=%s", (cliente_id, libro_id, fecha_venta, cantidad, total, id))
                connection.commit()
            flash('Préstamo actualizado exitosamente', 'success')
            return redirect(url_for('prestamos'))
        with connection.cursor() as cur:
            cur.execute("SELECT * FROM prestamos WHERE id=%s", (id,))
            prestamo = cur.fetchone()
        return render_template('editar_prestamo.html', prestamo=prestamo)
    except Exception as e:
        logging.error(f"Error en la ruta /prestamos/{id}: {e}")
        flash('Ocurrió un error al procesar la solicitud', 'danger')
        return redirect(url_for('prestamos'))
    finally:
        connection.close()

@app.route('/prestamos/eliminar/<int:id>', methods=['POST'])
def eliminar_prestamo(id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cur:
            cur.execute("DELETE FROM prestamos WHERE id=%s", (id,))
            connection.commit()
        flash('Préstamo eliminado exitosamente', 'success')
        return redirect(url_for('prestamos'))
    except Exception as e:
        logging.error(f"Error en la ruta /prestamos/eliminar/{id}: {e}")
        flash('Ocurrió un error al procesar la solicitud', 'danger')
        return redirect(url_for('prestamos'))
    finally:
        connection.close()

@app.route('/chatbot', methods=['POST'])
def chatbot():
    connection = get_db_connection()
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
                with connection.cursor() as cur:
                    cur.execute("INSERT INTO usuarios (nombre, email, telefono) VALUES (%s, %s, %s)", (nombre, email, telefono))
                    connection.commit()
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
                with connection.cursor() as cur:
                    if campo.lower() == "correo":
                        cur.execute("UPDATE usuarios SET email=%s WHERE nombre=%s", (valor, nombre))
                    elif campo.lower() == "teléfono":
                        cur.execute("UPDATE usuarios SET telefono=%s WHERE nombre=%s", (valor, nombre))
                    elif campo.lower() == "nombre":
                        cur.execute("UPDATE usuarios SET nombre=%s WHERE nombre=%s", (valor, nombre))
                    connection.commit()
                mensaje_respuesta += " - Usuario actualizado exitosamente."
            else:
                mensaje_respuesta += " - Faltan datos para actualizar el usuario."
        
        socketio.emit('chatbot_response', {'message': mensaje_respuesta})
        return mensaje_respuesta
    except Exception as e:
        logging.error(f"Error en la ruta /chatbot: {e}")
        return "Ocurrió un error al procesar la solicitud", 500
    finally:
        connection.close()

if __name__ == '__main__':
    socketio.run(app, debug=True)