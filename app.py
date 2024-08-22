from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Modelo Cliente
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

# Página Inicial (Lista de Clientes + Pesquisa)
@app.route('/')
def index():
    query = request.args.get('search')
    if query:
        clientes = Cliente.query.filter(Cliente.nome.ilike(f'%{query}%')).all()
    else:
        clientes = Cliente.query.all()
    return render_template('index.html', clientes=clientes)

# Adicionar Cliente
@app.route('/add', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        novo_cliente = Cliente(nome=nome, email=email)
        try:
            db.session.add(novo_cliente)
            db.session.commit()
            flash('Cliente adicionado com sucesso!')
            return redirect('/')
        except:
            flash('Erro ao adicionar cliente')
    return render_template('add_client.html')

# Editar Cliente
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_client(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        cliente.nome = request.form['nome']
        cliente.email = request.form['email']
        try:
            db.session.commit()
            flash('Cliente atualizado com sucesso!')
            return redirect('/')
        except:
            flash('Erro ao atualizar cliente')
    return render_template('edit_client.html', cliente=cliente)

# Excluir Cliente
@app.route('/delete/<int:id>')
def delete_client(id):
    cliente = Cliente.query.get_or_404(id)
    try:
        db.session.delete(cliente)
        db.session.commit()
        flash('Cliente excluído com sucesso!')
    except:
        flash('Erro ao excluir cliente')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
