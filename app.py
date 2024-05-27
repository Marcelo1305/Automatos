from flask import Flask, render_template, request, jsonify
import graphviz
import ast

app = Flask(__name__)

def criar_diagrama_de_estados(estados, transicoes, estado_inicial, estados_finais):
    fsm = graphviz.Digraph('FSM', format='png')
    fsm.attr(rankdir='LR', size='8,5')

    for estado in estados:
        if estado in estados_finais:
            fsm.node(estado, shape='doublecircle')
        else:
            fsm.node(estado)

    fsm.node('', shape='none')
    fsm.edge('', estado_inicial)

    for (de, simbolo, para) in transicoes:
        fsm.edge(de, para, label=simbolo)

    return fsm

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        estados = request.form['estados'].split(',')
        transicoes = ast.literal_eval(request.form['transicoes'])
        estado_inicial = request.form['estado_inicial']
        estados_finais = request.form['estados_finais'].split(',')

        diagrama = criar_diagrama_de_estados(estados, transicoes, estado_inicial, estados_finais)
        imagem_path = 'static/fsm_diagram'
        diagrama.render(filename=imagem_path, format='png', cleanup=True)  # Adicione cleanup=True

        # Retornar apenas o caminho da imagem
        return jsonify({'imagem_path': imagem_path + '.png'})

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

#[("q0", "a", "q1"),("q1", "b", "q2"),("q2", "a", "q3"), ("q3", "b", "q0"),("q3", "c", "q1")]