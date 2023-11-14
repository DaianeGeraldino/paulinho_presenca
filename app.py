from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/adicionar_tarefa', methods=['POST'])
def adicionar_tarefa():
    tarefa = request.form.get('tarefa')
    salvar_tarefa(tarefa)
    return redirect(url_for('index'))

@app.route('/editar_tarefa/<tarefa_antiga>', methods=['GET', 'POST'])
def editar_tarefa(tarefa_antiga):
    if request.method == 'POST':
        nova_tarefa = request.form.get('tarefa')
        atualizar_tarefa(tarefa_antiga, nova_tarefa)
        return redirect(url_for('index'))
    else:
        return render_template('editar_tarefa.html', tarefa_antiga=tarefa_antiga)

@app.route('/excluir_tarefa/<tarefa>')
def excluir_tarefa(tarefa):
    tarefas = load_tasks()
    tarefas.remove(tarefa)
    salvar_tarefas(tarefas)
    return redirect(url_for('index'))

def salvar_tarefas(tarefas):
    with open('tarefas.json', 'w') as f:
        json.dump(tarefas, f)

def load_tasks():
    try:
        with open('tarefas.json', 'r') as f:
            tarefas = json.load(f)
    except FileNotFoundError:
        tarefas = []
    return tarefas

def salvar_tarefa(tarefa):
    tarefas = load_tasks()
    tarefas.append(tarefa)
    salvar_tarefas(tarefas)

def atualizar_tarefa(tarefa_antiga, nova_tarefa):
    tarefas = load_tasks()
    if tarefa_antiga in tarefas:
        index = tarefas.index(tarefa_antiga)
        tarefas[index] = nova_tarefa
        salvar_tarefas(tarefas)

if __name__ == '__main__':
    app.run(debug=True)
