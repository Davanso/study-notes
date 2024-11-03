import sqlite3
from datetime import datetime

# Conecta ao BD
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

########################################################
# Cria tabela de livros
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    publication_year INTEGER NOT NULL,
    is_available INTEGER NOT NULL
);
""")

########################################################
# Cria tabela de membros
cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);
""")

########################################################
# Cria tabela de empréstimos
cursor.execute("""
CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    loan_date TEXT NOT NULL,
    return_date TEXT,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (member_id) REFERENCES members(id)
);
""")

conn.commit()

########################################################
# Função para adicionar um livro
def add_book(title, author, publication_year, is_available=True):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO books (title, author, publication_year, is_available)
    VALUES (?, ?, ?, ?)
    """, (title, author, publication_year, is_available))
    conn.commit()
    conn.close()
    print("Livro adicionado com sucesso")

########################################################
# Função para listar todos os livros
def list_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    if len(books) == 0:
        print("Nenhum livro encontrado.")
    else:
        for book in books:
            status = "Disponível" if book[4] == 1 else "Indisponível"
            print(f'ID: {book[0]}, Título: {book[1]}, Autor: {book[2]}, Ano: {book[3]}, Status: {status}')

########################################################
# Função para adicionar um novo membro
def add_member(name, address, email):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO members (name, address, email)
    VALUES (?, ?, ?)
    """, (name, address, email))
    conn.commit()
    conn.close()
    print("Membro adicionado com sucesso")

########################################################
# Função para listar os membros
def list_members():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM members')
    members = cursor.fetchall()
    conn.close()
    if len(members) == 0:
        print("Nenhum membro encontrado.")
    else:
        for member in members:
            print(f'ID: {member[0]}, Nome: {member[1]}, Endereço: {member[2]}, Email: {member[3]}')

########################################################
# Função para registrar um empréstimo
def loan_book(book_id, member_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT is_available FROM books WHERE id=?', (book_id,))
    book_is_available = cursor.fetchone()[0]

    if book_is_available == 1:  # Verifica se o livro está disponível
        loan_date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("""
        INSERT INTO loans (book_id, member_id, loan_date)
        VALUES (?, ?, ?)
        """, (book_id, member_id, loan_date))

        cursor.execute('UPDATE books SET is_available=? WHERE id=?', (0, book_id))
        conn.commit()
        print("Livro emprestado com sucesso")
    else:
        print("Livro indisponível")
    conn.close()

########################################################
# Função para registrar a devolução de um livro
def return_book(loan_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    return_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
    UPDATE loans
    SET return_date = ?
    WHERE id = ? AND return_date IS NULL
    ''', (return_date, loan_id))

    cursor.execute('SELECT book_id FROM loans WHERE id = ?', (loan_id,))
    book_id = cursor.fetchone()[0]

    cursor.execute('UPDATE books SET is_available = 1 WHERE id = ?', (book_id,))

    conn.commit()
    conn.close()
    print("Devolução registrada com sucesso!")

########################################################
# Função para interagir com o user
def menu():
    while True:
        print("\nMenu:")
        print("1 - Adicionar livro")
        print("2 - Listar livros")
        print("3 - Adicionar membro")
        print("4 - Listar membros")
        print("5 - Registrar empréstimo")
        print("6 - Registrar devolução")
        print("0 - Sair")

        choice = input("Selecione uma opção: ")

        if choice == '1':
            title = input("Digite o título do livro: ")
            author = input("Digite o autor do livro: ")
            year = int(input("Digite o ano de publicação: "))
            add_book(title, author, year)
        elif choice == '2':
            list_books()
        elif choice == '3':
            name = input("Digite o nome do membro: ")
            address = input("Digite o endereço do membro: ")
            email = input("Digite o email do membro: ")
            add_member(name, address, email)
        elif choice == '4':
            list_members()
        elif choice == '5':
            book_id = int(input("Digite o ID do livro: "))
            member_id = int(input("Digite o ID do membro: "))
            loan_book(book_id, member_id)
        elif choice == '6':
            loan_id = int(input("Digite o ID do empréstimo: "))
            return_book(loan_id)
        elif choice == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == '__main__':
    menu()


# Falta tratar os erros