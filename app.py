from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__) # la constante de la aplicacion

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'myhorsenameisjimini'
app.config['MYSQL_DB'] = 'loyola_1'
mysql = MySQL(app)

#Session en localstorage
app.secret_key = 'mysupersecretkey'



@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/add', methods=['POST'])
def addAlumno():
    if request.method == 'POST':
        fullname = request.form['fullname']
        code = request.form['code']
        carrer = request.form['carrera']
        birthdate = request.form['birthdate']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO alumnos (name, code, carrer, birthdate) VALUES (%s, %s, %s, %s)', 
        (fullname, code, carrer ,birthdate))
        mysql.connection.commit()
        flash('Alumno añadido correctamente!')
        return redirect(url_for('login'))

@app.route('/log', methods=['POST'])
def log():
    if request.method == 'POST':
        fullname = request.form['fullname']
        code = request.form['code']
        cur = mysql.connection.cursor()
        query= "SELECT * FROM alumnos WHERE name='{}' and code='{}'".format(fullname, code)
        #cur.execute('SELECT * FROM alumnos WHERE name=%s and code=%s', (fullname, code))
        print(query)
        cur.execute(query)
        data = cur.fetchall()
        if(data == ()):
            return render_template('404.html')
        flash('Ha iniciado sesion correctamente!')
        return render_template('index.html', alumnos = data)





if __name__ == "__main__": #verificar que estemos en el entorno main
    app.run(port=4000, debug=True)




