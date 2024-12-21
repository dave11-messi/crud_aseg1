from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mi_fulbito'

mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM equipos')
    equipos = cursor.fetchall()
    return render_template('index.html', equipos=equipos)

@app.route('/add', methods=['GET', 'POST'])
def add_equipo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        entrenador = request.form['entrenador']
        ciudad = request.form['ciudad']
        estadio = request.form['estadio']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO equipos (nombre, entrenador, ciudad, estadio) VALUES (%s, %s, %s, %s)', (nombre, entrenador, ciudad, estadio))
        mysql.connection.commit()
        flash('Equipo agregado exitosamente')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_equipo(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        nombre = request.form['nombre']
        entrenador = request.form['entrenador']
        ciudad = request.form['ciudad']
        estadio = request.form['estadio']
        cursor.execute('UPDATE equipos SET nombre = %s, entrenador = %s, ciudad = %s, estadio = %s WHERE id = %s', (nombre, entrenador, ciudad, estadio, id))
        mysql.connection.commit()
        flash('Equipo actualizado exitosamente')
        return redirect(url_for('index'))
    cursor.execute('SELECT * FROM equipos WHERE id = %s', (id,))
    equipo = cursor.fetchone()
    return render_template('edit.html', equipo=equipo)

@app.route('/delete/<id>', methods=['GET'])
def delete_equipo(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM equipos WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Equipo eliminado exitosamente')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
