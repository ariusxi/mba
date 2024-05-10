const botao = document.querySelector('button')
botao.addEventListener('click', somaUm)

function pegarValorAleatorio(maximo) {
    return parseInt(Math.random() * maximo)
}

function somaUm() {
    let elementoH3 = document.querySelector('h3')
    let valor = parseInt(elementoH3.textContent)
    let novoValor = valor + 1
    elementoH3.textContent = novoValor

    const valorMaximo = 256

    let r = pegarValorAleatorio(valorMaximo)
    let g = pegarValorAleatorio(valorMaximo)
    let b = pegarValorAleatorio(valorMaximo)

    elementoH3.style.color = `rgb(${r}, ${g}, ${b})`
}