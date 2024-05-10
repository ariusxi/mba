let botao = document.querySelector('button')
botao.addEventListener('click', somarUm)

function somarUm() {
    let elementoH3 = document.querySelector('h3')
    let valorAtual = parseInt(elementoH3.textContent)
    let novoValor = valorAtual + 1
    elementoH3.textContent = novoValor

    let r = Math.floor(Math.random() * 256);
    let g = Math.floor(Math.random() * 256);
    let b = Math.floor(Math.random() * 256);

    if (novoValor > valorAtual) {
        elementoH3.style.color = `rgb(${r}, ${g}, ${b})`;
    }
}
