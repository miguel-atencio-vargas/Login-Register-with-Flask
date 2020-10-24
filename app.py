from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__) # la constante de la aplicacion


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'myhorsenameisjimini'
app.config['MYSQL_DB'] = 'LoyolaDB'
mysql = MySQL(app)

@app.route('/home')
def home():
	return render_template('index.html')


#===== Carreras ========
@app.route('/carreras')
def listarCarreras():
	query= "SELECT * FROM Carrera;"
	cur = mysql.connection.cursor()
	cur.execute(query)
	data = list(cur.fetchall())
	carreras = list()
	for i in data:
		carreras.append(list(i))
	print(carreras)
	if(data):
		return render_template('listarCarreras.html', carreras=carreras)
	return render_template('404.html')


@app.route('/carreras/<id>')
def detallesCarrera(id):
	query="SELECT nombre_carrera, nombre_materia FROM Carrera a, tiene b, Materia c WHERE(a.ID_Carrera = b.fk_ID_Carrera AND b.fk_ID_Materia=c.ID_Materia) AND a.ID_Carrera ='{}';".format(id)
	query2="SELECT nombres, apellido_paterno, apellido_materno, codigo, fecha_de_inscripcion, celular, fecha_nacimiento FROM Alumno a, esta_inscrito b, Carrera c WHERE (a.ID_Alumno = b.fk_ID_Alumno AND b.fk_ID_Carrera = c.ID_Carrera) AND c.ID_Carrera = '{}';".format(id)
	cur = mysql.connection.cursor()
	cur.execute(query)
	data = list(cur.fetchall())
	cur.execute(query2)
	data2 = list(cur.fetchall())
	materias = list()
	alumnos = list()
	for i in data:
		materias.append(list(i))
	for i in data2:
		alumnos.append(list(i))
	if(data):
		print(alumnos)
		return render_template('carrer-detail.html', materias=materias, alumnos=alumnos)
	return render_template('404.html')

#===== Materias ========
@app.route('/materias')
def listarMaterias():
	query= "SELECT * FROM Materia;"
	cur = mysql.connection.cursor()
	cur.execute(query)
	data = list(cur.fetchall())
	materias = list()
	for i in data:
		materias.append(list(i))
	if(data):
		return render_template('listarMaterias.html', materias=materias)
	return render_template('404.html')
#===== Docentes ========
@app.route('/docentes')
def listarDocentes():
	query= "SELECT * FROM Docente;"
	cur = mysql.connection.cursor()
	cur.execute(query)
	data = list(cur.fetchall())
	docentes = list()
	for i in data:
		docentes.append(list(i))
	if(data):
		return render_template('listarDocentes.html', docentes=docentes)
	return render_template('404.html')
#===== Alumnos ========
@app.route('/alumnos')
def listarAlumnos():
	query= "SELECT * FROM Alumno;"
	cur = mysql.connection.cursor()
	cur.execute(query)
	data = list(cur.fetchall())
	alumnos = list()
	for i in data:
		alumnos.append(list(i))
	if(data):
		return render_template('listarAlumnos.html', alumnos=alumnos)
	return render_template('404.html')





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
		print(data)
		if(data == ()):
			return render_template('404.html')
		flash('Ha iniciado sesion correctamente!')
		return render_template('index.html', alumnos = data)


if __name__ == "__main__": #verificar que estemos en el entorno main
	print(__name__)
	app.debug = True
	app.run()
