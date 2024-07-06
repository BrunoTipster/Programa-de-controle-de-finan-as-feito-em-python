import customtkinter as ctk
from tkinter import messagebox

class Validation:
    def validate(self, descricao, valor):
        if not descricao:
            messagebox.showerror("Erro de Validação", "A descrição não pode estar vazia.")
            return False
        try:
            valor = float(valor)
            if valor <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro de Validação", "O valor deve ser um número positivo.")
            return False
        return True

class AddEditButtons:
    def __init__(self, app, frame):
        self.app = app
        self.add_buttons(frame)

    def add_buttons(self, frame):
        edit_button = ctk.CTkButton(frame, text="Editar", command=self.edit_transaction)
        edit_button.pack(side="left", padx=5, pady=5)
        delete_button = ctk.CTkButton(frame, text="Excluir", command=self.delete_transaction)
        delete_button.pack(side="left", padx=5, pady=5)

    def edit_transaction(self):
        selected_item = self.app.tree.selection()
        if not selected_item:
            messagebox.showwarning("Nenhuma Seleção", "Selecione uma transação para editar.")
            return
        # Implementar lógica de edição aqui
        # Exemplo: Abrir uma nova janela para editar os detalhes da transação

    def delete_transaction(self):
        selected_item = self.app.tree.selection()
        if not selected_item:
            messagebox.showwarning("Nenhuma Seleção", "Selecione uma transação para excluir.")
            return
        for item in selected_item:
            descricao, valor, tipo = self.app.tree.item(item, 'values')
            self.app.db.cursor.execute(
                "DELETE FROM transacoes WHERE descricao=%s AND valor=%s AND tipo=%s",
                (descricao, float(valor.replace("R$ ", "")), tipo)
            )
            self.app.db.conn.commit()
            self.app.tree.delete(item)

class Filters:
    def __init__(self, app):
        self.app = app
        self.add_filters()

    def add_filters(self):
        filter_frame = ctk.CTkFrame(self.app.root, corner_radius=10)
        filter_frame.pack(pady=10)

        filter_label = ctk.CTkLabel(filter_frame, text="Filtrar por Tipo")
        filter_label.pack(side="left", padx=5)
        self.filter_var = ctk.StringVar(value="Todos")
        filter_all = ctk.CTkRadioButton(filter_frame, text="Todos", variable=self.filter_var, value="Todos", command=self.apply_filter)
        filter_all.pack(side="left", padx=5)
        filter_entrada = ctk.CTkRadioButton(filter_frame, text="Entrada", variable=self.filter_var, value="Entrada", command=self.apply_filter)
        filter_entrada.pack(side="left", padx=5)
        filter_saida = ctk.CTkRadioButton(filter_frame, text="Saída", variable=self.filter_var, value="Saída", command=self.apply_filter)
        filter_saida.pack(side="left", padx=5)

    def apply_filter(self):
        filter_value = self.filter_var.get()
        for item in self.app.tree.get_children():
            descricao, valor, tipo = self.app.tree.item(item, 'values')
            if filter_value == "Todos" or tipo == filter_value:
                self.app.tree.item(item, tags=())
            else:
                self.app.tree.item(item, tags=("hidden",))

        self.app.tree.tag_configure('hidden', foreground='grey')

class GraphReports:
    def __init__(self, app):
        self.app = app
        self.add_graph_button()

    def add_graph_button(self):
        graph_button = ctk.CTkButton(self.app.root, text="Gerar Relatório", command=self.app.generate_report)
        graph_button.pack(pady=5)

class SearchBar:
    def __init__(self, app):
        self.app = app
        self.add_search_bar()

    def add_search_bar(self):
        search_frame = ctk.CTkFrame(self.app.root, corner_radius=10)
        search_frame.pack(pady=10)

        search_label = ctk.CTkLabel(search_frame, text="Pesquisar")
        search_label.pack(side="left", padx=5)
        self.search_entry = ctk.CTkEntry(search_frame)
        self.search_entry.pack(side="left", padx=5)
        search_button = ctk.CTkButton(search_frame, text="Buscar", command=self.search_transaction)
        search_button.pack(side="left", padx=5)

    def search_transaction(self):
        search_term = self.search
