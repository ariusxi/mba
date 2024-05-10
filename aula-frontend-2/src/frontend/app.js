let lista = document.getElementById("produtos__lista")
let endpoint = 'https://raw.githubusercontent.com/guilhermeonrails/api-frontend/main/produtos.json'

function constroiItem(produto) {
    lista.innerHTML += `
        <li class="produtos__item">
            <div class="produtos__content">
                <img src="${produto.img}" alt="${produto.nome}">
                <div class="produtos__informacoes">
                    <h3>${produto.nome}</h3>
                    <p>${produto.descricao}</p>
                    <h4>R$ ${produto.valorComDesconto}<s>R$ ${produto.valorSemDesconto}</s></h4>
                    <p>Frete GRÁTIS</p>
                </div>
            </div>
        </li>
    `
}

async function buscarProdutosApi() {
    let resposta = await fetch(endpoint)
    return resposta.json()
}

async function listaProdutos() {
    const produtos = await buscarProdutosApi()

    produtos.forEach((produto) => constroiItem(produto))
}
listaProdutos()