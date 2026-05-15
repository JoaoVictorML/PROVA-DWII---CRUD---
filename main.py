from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chave_secreta_ifce'

db = SQLAlchemy(app)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)

class ProdutoDAO:
    @staticmethod
    def inserir(produto):
        db.session.add(produto)
        db.session.commit()

    @staticmethod
    def listar():
        return Produto.query.all()

    @staticmethod
    def procurar_por_id(id_produto):
        return Produto.query.get_or_404(id_produto)

    @staticmethod
    def pesquisar(query):
        return Produto.query.filter(
            (Produto.nome.contains(query)) | (Produto.codigo.contains(query))
        ).all()

    @staticmethod
    def alterar():
        db.session.commit()

    @staticmethod
    def apagar(produto):
        db.session.delete(produto)
        db.session.commit()

with app.app_context():
    db.create_all()


# --- ROTAS ---

@app.route('/')
def index():
    return render_template('index.html', produto=None)

@app.route('/adicionar', methods=['POST'])
def adicionar_produto():
    codigo = request.form.get('codigo')
    nome = request.form.get('nome')
    preco = request.form.get('preco')

    novo_produto = Produto(codigo=codigo, nome=nome, preco=float(preco))
    ProdutoDAO.inserir(novo_produto)
    return redirect(url_for('listar_produtos'))

@app.route('/produtos')
def listar_produtos():
    query = request.args.get('q')
    if query:
        produtos = ProdutoDAO.pesquisar(query)
    else:
        produtos = ProdutoDAO.listar()
    return render_template('produtos.html', produtos=produtos)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    produto = ProdutoDAO.procurar_por_id(id)
    
    if request.method == 'POST':
        produto.codigo = request.form.get('codigo')
        produto.nome = request.form.get('nome')
        produto.preco = float(request.form.get('preco'))
        
        ProdutoDAO.alterar()
        return redirect(url_for('listar_produtos'))
        
    return render_template('index.html', produto=produto)

@app.route('/deletar/<int:id>', methods=['POST'])
def deletar_produto(id):
    produto = ProdutoDAO.procurar_por_id(id)
    ProdutoDAO.apagar(produto)
    return redirect(url_for('listar_produtos'))

if __name__ == '__main__':
    app.run(debug=True)