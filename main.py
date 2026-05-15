from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chave_secreta_ifce'

db = SQLAlchemy(app)

# Modelo do Produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)

# Cria o banco de dados
with app.app_context():
    db.create_all()

# --- ROTAS ---

@app.route('/')
def index():
    return render_template('index.html')

# 1. CREATE (Adicionar)
@app.route('/adicionar', methods=['POST'])
def adicionar_produto():
    codigo = request.form.get('codigo')
    nome = request.form.get('nome')
    preco = request.form.get('preco')

    novo_produto = Produto(codigo=codigo, nome=nome, preco=float(preco))
    db.session.add(novo_produto)
    db.session.commit()
    return redirect(url_for('listar_produtos'))

# 2. READ (Listar com Pesquisa integrada)
@app.route('/produtos')
def listar_produtos():
    query = request.args.get('q')
    if query:
        # Busca por nome ou código
        produtos = Produto.query.filter(
            (Produto.nome.contains(query)) | (Produto.codigo.contains(query))
        ).all()
    else:
        produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)

# 3. DELETE (Remover)
@app.route('/deletar/<int:id>', methods=['POST'])
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('listar_produtos'))

# 4. UPDATE (Apenas rota de exemplo, você pode expandir depois)
@app.route('/editar/<int:id>')
def editar_produto(id):
    # Aqui você renderizaria um form de edição
    return f"Página de edição do produto {id}"

if __name__ == '__main__':
    app.run(debug=True)