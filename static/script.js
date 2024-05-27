document.getElementById('adicionarTransicao').addEventListener('click', function() {
    const tabela = document.getElementById('tabelaTransicoes').getElementsByTagName('tbody')[0];
    const novaLinha = tabela.insertRow();

    const estadoAtual = novaLinha.insertCell(0);
    const simbolo = novaLinha.insertCell(1);
    const proximoEstado = novaLinha.insertCell(2);
    const acao = novaLinha.insertCell(3);

    estadoAtual.innerHTML = '<input type="text" class="form-control estado" placeholder="q0">';
    simbolo.innerHTML = '<input type="text" class="form-control simbolo" placeholder="a">';
    proximoEstado.innerHTML = '<input type="text" class="form-control estado" placeholder="q1">';
    acao.innerHTML = '<button type="button" class="btn btn-danger remover-linha">Remover</button>';
});

document.getElementById('meuFormulario').addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o envio do formulário
    
    const transicoes = [];
    const linhas = document.getElementById('tabelaTransicoes').getElementsByTagName('tbody')[0].getElementsByTagName('tr');

    for (const linha of linhas) {
        const estadoAtual = linha.getElementsByClassName('estado')[0].value;
        const simbolo = linha.getElementsByClassName('simbolo')[0].value;
        const proximoEstado = linha.getElementsByClassName('estado')[1].value;

        transicoes.push(`("${estadoAtual}", "${simbolo}", "${proximoEstado}")`);
    }

    const formData = new FormData(this);
    formData.append('transicoes', `[${transicoes.join(', ')}]`);

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json()) // Converte a resposta para JSON
    .then(data => {
        const imagemContainer = document.getElementById('imagemContainer'); // Insere a imagem na div
        imagemContainer.innerHTML = ''; // Limpa a div
        
        const imgElement = document.createElement('img');
        imgElement.src = data.imagem_path + '?t=' + new Date().getTime(); // Adiciona um parâmetro de consulta único
        imgElement.alt = 'Diagrama de Estados';
        imgElement.classList.add('img-fluid', 'border-image');

        imagemContainer.appendChild(imgElement);
    })
    .catch(error => console.error('Erro:', error)); // Trata erros
});

document.getElementById('tabelaTransicoes').addEventListener('click', function(event) {
    if (event.target.classList.contains('remover-linha')) {
        const linha = event.target.closest('tr');
        linha.remove();
    }
});