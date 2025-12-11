import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv

#Cargar las variables de entorno
load_dotenv()

#Crear instancia
app = Flask(__name__)

#Configuración de la base de datos PostgreSQL
database_url = os.getenv('DATABASE_URL')
# Fix para SQLAlchemy 1.4+: reemplazar postgres:// con postgresql://
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Desactivar el seguimiento de modificaciones de objetos

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

#Modelo de la base de datos
class Gasto(db.Model):
    __tablename__= 'gastos'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(200))
    metodo_pago = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return{
            'id': self.id,
            'fecha': self.fecha.strftime('%Y-%m-%d'),
            'categoria': self.categoria,
            'monto': self.monto,
            'descripcion': self.descripcion,
            'metodo_pago': self.metodo_pago
        }

#Crear tablas si no existen
with app.app_context():
    db.create_all()

#Ruta raiz
@app.route('/', methods=['GET'])
def index():
    #Trae todos los gastos ordenados por fecha (más reciente primero)
    gastos = Gasto.query.order_by(Gasto.fecha.desc()).all()
    #Calcular total de gastos
    total = sum(gasto.monto for gasto in gastos)
    return render_template('index.html', gastos=gastos, total=total)

#CREAR
@app.route('/new', methods=['GET','POST'])
def create_gasto():
    if request.method == 'POST':
        from datetime import datetime
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d')
        categoria = request.form['categoria']
        monto = float(request.form['monto'])
        descripcion = request.form['descripcion']
        metodo_pago = request.form['metodo_pago']
        db.session.add(Gasto(fecha=fecha, categoria=categoria, monto=monto, descripcion=descripcion, metodo_pago=metodo_pago))
        db.session.commit()
        return redirect(url_for('index'))
    #Aqui sigue si es GET
    return render_template('create_gasto.html')

#ACTUALIZAR
@app.route('/update/<int:id>', methods=['GET','POST'])
def update_gasto(id):
    gasto = Gasto.query.get(id)
    if request.method == 'POST':
        from datetime import datetime
        gasto.fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d')
        gasto.categoria = request.form['categoria']
        gasto.monto = float(request.form['monto'])
        gasto.descripcion = request.form['descripcion']
        gasto.metodo_pago = request.form['metodo_pago']
        db.session.commit()
        return redirect(url_for('index'))
    #Aqui sigue si es GET
    return render_template('update_gasto.html', gasto=gasto)

#ELIMINAR
@app.route('/delete/<int:id>')
def delete_gasto(id):
    gasto = Gasto.query.get(id)
    if gasto:
        db.session.delete(gasto)
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

#source bin/activate
#pip install -r requirements.txt
#flask run --port=5010