from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kaeshark:ellagarto123@localhost/lotto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = SQLAlchemy(app)

# Modelo de ejemplo: Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', username=name)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f"Mostrando el post con ID {post_id}."

# Nueva ruta para probar la conexión
@app.route('/db-check')
def db_check():
    try:
        # Usar text() para la consulta
        db.session.execute(text('SELECT 1'))
        return "¡Conexión a PostgreSQL exitosa!"
    except Exception as e:
        return f"Error al conectar con la base de datos: {e}"
    

@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    if request.method == 'POST':
        # Agregar usuario
        try:
            name = request.form['name']
            email = request.form['email']
            nuevo_usuario = Usuario(nombre=name, correo=email)
            db.session.add(nuevo_usuario)
            db.session.commit()
        except Exception as e:
            return f"Error al agregar usuario: {e}"
    
    # Obtener lista de usuarios
    usuarios = Usuario.query.all()
    return render_template('usuario.html', usuarios=usuarios)

@app.route('/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    try:
        usuario = Usuario.query.get(user_id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return redirect(url_for('usuarios'))
        else:
            return f"Usuario con ID {user_id} no encontrado."
    except Exception as e:
        return f"Error al eliminar usuario: {e}"




if __name__ == '__main__':
    app.run(debug=True)
