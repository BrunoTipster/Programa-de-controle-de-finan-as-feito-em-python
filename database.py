import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="controle_financeiro"
        )
        self.cursor = self.conn.cursor()

    def insert_transaction(self, descricao, valor, tipo):
        self.cursor.execute(
            "INSERT INTO transacoes (descricao, valor, tipo) VALUES (%s, %s, %s)",
            (descricao, valor, tipo)
        )
        self.conn.commit()

    def get_all_transactions(self):
        self.cursor.execute("SELECT descricao, valor, tipo FROM transacoes")
        return self.cursor.fetchall()

    def verify_user(self, username, password):
        self.cursor.execute("SELECT * FROM usuarios WHERE username=%s AND password=%s", (username, password))
        return self.cursor.fetchone() is not None

    def __del__(self):
        self.cursor.close()
        self.conn.close()
