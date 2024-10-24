import sqlite3

# Conecta ou cria o banco de dados SQLite
conn = sqlite3.connect('todo_list.db')
cursor = conn.cursor()

# Cria a tabela tasks se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL
)
''')

# Confirma a criação da tabela
conn.commit()

# Função para adicionar uma nova tarefa
def add_task(title, description):
    cursor.execute('''
    INSERT INTO tasks (title, description, status)
    VALUES (?, ?, 'pendente')
    ''', (title, description))
    conn.commit()
    print("Tarefa adicionada com sucesso!")

# Função para listar todas as tarefas
def list_tasks():
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    
    if len(tasks) == 0:
        print("Nenhuma tarefa encontrada.")
    else:
        for task in tasks:
            print(f'ID: {task[0]}, Título: {task[1]}, Descrição: {task[2]}, Status: {task[3]}')

# Função para marcar uma tarefa como concluída
def complete_task(task_id):
    cursor.execute('''
    UPDATE tasks
    SET status = 'concluída'
    WHERE id = ?
    ''', (task_id,))
    conn.commit()
    print("Tarefa marcada como concluída!")

# Função para excluir uma tarefa
def delete_task(task_id):
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    print("Tarefa excluída com sucesso!")


# Função para interagir com o usuario
def menu():
    while True:
        print("\nMenu:")
        print("1 - Adicionar tarefa")
        print("2 - Listar tarefas")
        print("3 - Marcar tarefa como concluída")
        print("4 - Excluir tarefa")
        print("0 - Sair")

        choice = input("Selecionar uma opção: ")

        if choice == '1':
            title = input("Digite o título da tarefa: ")
            description = input("Digite a descrição da tarefa (ou pressione ENTER para não adicionar): ")
            add_task(title, description)
        elif choice == '2':
            list_tasks()
        elif choice == '3':
            task_id = int(input("Digite o ID da tarefa que deseja marcar como concluída: "))
            complete_task(task_id)
        elif choice == '4':
            task_id = int(input("Digite o ID da tarefa que deseja excluir: "))
            delete_task(task_id)
        elif choice == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == '__main__':
    menu()
    conn.close()

    