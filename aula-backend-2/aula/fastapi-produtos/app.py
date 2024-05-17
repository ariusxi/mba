from fastapi import FastAPI

from models.product import Product

app = FastAPI()

@app.get('/')
def hello_world():
    """
    Primeiro endpoint que diz Hello World!
    """
    return { 'message': 'Hello World' }

@app.get('/{nome}')
def ola(nome: str):
    """
    Escreva o nome e receba a mensagem de olá mais o seu nome
    """
    if not nome:
        pass
    return { 'message': f'Olá {nome}' }

data = [
    Product(id=1, name='Tênis Nike Air', description='Calçado muito legal', price=199.99),
    Product(id=2, name='iPhone', description='Celulares', price=5199.99),
    Product(id=3, name='Samsung', description='Celulares', price=4199.99),
    Product(id=4, name='Notebook', description='Eletrônicos', price=4928.97),
]

@app.get('/api/products')
def get_products():
    """
    Endpoint que disponibiliza recursos com todos os produtos
    """
    return data

@app.get('/api/products/{id}')
def get_product_by_id(id: int):
    """
    Listando um único produto por ID
    """
    for product in data:
        if product.id == id:
            return product
    return { 'message': 'Nenhum produto encontrado com o ID fornecido' }
    