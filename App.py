from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonPrueba'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM libros')
    data = cur.fetchall()
    return render_template('Index.html', libros = data)

@app.route('/Agregar_Libro', methods=['POST'])
def add_book():
    if request.method == 'POST':
        titulo = request.form['titulo']
        iSSN = request.form['iSSN']
        autor = request.form['autor']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO libros (titulo, issn, autor) VALUES (%s, %s, %s)', (titulo, iSSN, autor))
        mysql.connection.commit()
        flash('Libro Agregado')

        return redirect(url_for('Index'))

@app.route('/Editar_Libro/<id>')
def get_libro(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM libros WHERE id = %(Id)s', {'Id':id})
    data = cur.fetchall()
    print(data[0])
    return render_template('editar_libro.html', libro = data[0])

@app.route('/update/<string:id>', methods = ['POST'])
def update_libro(id):
    if request.method == 'POST':
        titulo = request.form['titulo']
        iSSN = request.form['iSSN']
        autor = request.form['autor']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE libros
            SET titulo = %s,
                iSSN = %s,
                autor = %s
            WHERE id = %s
        """,(titulo, iSSN, autor, id))
        cur.connection.commit()
        flash('actualizado')
        return redirect(url_for('Index'))

@app.route('/Eliminar_Libro/<string:id>')
def delete_book(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM libros WHERE id = %(Id)s', {'Id':id})
    mysql.connection.commit()
    flash('El libro fue removido')
    return redirect(url_for('Index'))

@app.route('/Busqueda')
def Busqueda():
    return render_template('busqueda.html')

@app.route('/Buscar', methods = ['POST'])
def Buscar():
    if request.method == 'POST':
        busqueda = request.form['busqueda']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM libros WHERE titulo = %(busca)s", {'busca':busqueda})
        data = cur.fetchall()
        print(data)
        return render_template('busqueda.html', libros = data)

if __name__ == '__main__':
    app.run(port = 3000, debug = True)