from flask import Flask, render_template, request, jsonify
import graphviz
import ast

app = Flask(__name__)  # Cria uma instância do aplicativo Flask

def criar_diagrama_de_estados(estados, transicoes, estado_inicial, estados_finais):
    # Função para criar um diagrama de estados usando Graphviz
    fsm = graphviz.Digraph('FSM', format='png')  # Cria um novo grafo dirigido chamado 'FSM' com formato PNG
    fsm.attr(rankdir='LR', size='8,5')  # Define a direção do gráfico da esquerda para a direita e o tamanho

    for estado in estados:
        # Itera sobre todos os estados
        if estado in estados_finais:
            fsm.node(estado, shape='doublecircle')  # Se o estado for final, desenha um círculo duplo
        else:
            fsm.node(estado)  # Caso contrário, desenha um círculo simples

    fsm.node('', shape='none')  # Adiciona um nó invisível para indicar o estado inicial
    fsm.edge('', estado_inicial)  # Cria uma aresta do nó invisível para o estado inicial

    for (de, simbolo, para) in transicoes:
        # Itera sobre todas as transições
        fsm.edge(de, para, label=simbolo)  # Adiciona uma aresta com um rótulo que representa o símbolo de transição

    return fsm  # Retorna o objeto Graphviz

@app.route('/', methods=['GET', 'POST'])
def index():
    # Define a rota principal que aceita métodos GET e POST
    if request.method == 'POST':
        # Se o método da requisição for POST, processa os dados do formulário
        estados = request.form['estados'].split(',')  # Obtém e divide os estados fornecidos pelo usuário
        transicoes = ast.literal_eval(request.form['transicoes'])  # Avalia as transições fornecidas como uma lista de tuplas
        estado_inicial = request.form['estado_inicial']  # Obtém o estado inicial
        estados_finais = request.form['estados_finais'].split(',')  # Obtém e divide os estados finais

        diagrama = criar_diagrama_de_estados(estados, transicoes, estado_inicial, estados_finais)
        # Cria o diagrama de estados
        imagem_path = 'static/fsm_diagram'  # Define o caminho para salvar a imagem do diagrama
        diagrama.render(filename=imagem_path, format='png', cleanup=True)  # Renderiza a imagem e a salva no caminho definido

        # Retorna apenas o caminho da imagem como JSON
        return jsonify({'imagem_path': imagem_path + '.png'})

    return render_template('index.html')  # Se o método for GET, renderiza o template HTML

if __name__ == '__main__':
    app.run(debug=True)  # Inicia o servidor Flask em modo debug

# Exemplo de transições:
# [("q0", "a", "q1"),("q1", "b", "q2"),("q2", "a", "q3"), ("q3", "b", "q0"),("q3", "c", "q1")]
