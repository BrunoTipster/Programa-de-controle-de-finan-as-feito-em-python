import customtkinter as ctk
from tkinter import messagebox, ttk
from database import Database
from utils import Validation, AddEditButtons, Filters, GraphReports, SearchBar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

class FinanceControl:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle Financeiro")
        self.root.geometry("600x800")

        self.db = Database()
        self.entradas = 0
        self.saidas = 0
        self.total = 0

        self.create_widgets()
        self.load_transactions()

    def create_widgets(self):
        top_frame = ctk.CTkFrame(self.root, corner_radius=10)
        top_frame.pack(pady=10, padx=20, fill="x")

        self.entradas_label = ctk.CTkLabel(top_frame, text=f"Entradas\nR$ {self.entradas:.2f}", width=100, height=50, corner_radius=8)
        self.entradas_label.grid(row=0, column=0, padx=10, pady=10)

        self.saidas_label = ctk.CTkLabel(top_frame, text=f"Saídas\nR$ {self.saidas:.2f}", width=100, height=50, corner_radius=8)
        self.saidas_label.grid(row=0, column=1, padx=10, pady=10)

        self.total_label = ctk.CTkLabel(top_frame, text=f"Total\nR$ {self.total:.2f}", width=100, height=50, corner_radius=8)
        self.total_label.grid(row=0, column=2, padx=10, pady=10)

        input_frame = ctk.CTkFrame(self.root, corner_radius=10)
        input_frame.pack(pady=10, padx=20, fill="x")

        desc_label = ctk.CTkLabel(input_frame, text="Descrição")
        desc_label.grid(row=0, column=0, padx=10, pady=5)
        self.desc_entry = ctk.CTkEntry(input_frame)
        self.desc_entry.grid(row=0, column=1, padx=10, pady=5)

        valor_label = ctk.CTkLabel(input_frame, text="Valor")
        valor_label.grid(row=1, column=0, padx=10, pady=5)
        self.valor_entry = ctk.CTkEntry(input_frame)
        self.valor_entry.grid(row=1, column=1, padx=10, pady=5)

        type_frame = ctk.CTkFrame(input_frame)
        type_frame.grid(row=2, columnspan=2, pady=5)

        self.tipo = ctk.StringVar(value="Entrada")
        entrada_rb = ctk.CTkRadioButton(type_frame, text="Entrada", variable=self.tipo, value="Entrada")
        entrada_rb.pack(side="left", padx=10)
        saida_rb = ctk.CTkRadioButton(type_frame, text="Saída", variable=self.tipo, value="Saída")
        saida_rb.pack(side="left", padx=10)

        add_button = ctk.CTkButton(input_frame, text="Adicionar", command=self.add_transaction)
        add_button.grid(row=3, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.root, columns=("Descrição", "Valor", "Tipo"), show="headings")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.heading("Valor", text="Valor")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.pack(pady=10, padx=20, fill="both", expand=True)

        action_frame = ctk.CTkFrame(self.root, corner_radius=10)
        action_frame.pack(pady=10, padx=20, fill="x")

        # Load additional functionalities
        self.validation = Validation()
        self.add_edit_buttons = AddEditButtons(self, action_frame)
        self.filters = Filters(self)
        self.graph_reports = GraphReports(self)
        self.search_bar = SearchBar(self)

        export_button = ctk.CTkButton(action_frame, text="Exportar CSV", command=self.export_to_csv)
        export_button.pack(side="left", padx=5, pady=5)

    def add_transaction(self):
        descricao = self.desc_entry.get()
        valor = self.valor_entry.get()
        tipo = self.tipo.get()

        if not self.validation.validate(descricao, valor):
            return

        valor = float(valor)
        if tipo == "Entrada":
            self.entradas += valor
        else:
            self.saidas += valor

        self.total = self.entradas - self.saidas

        self.update_labels()

        # Salvar a transação no banco de dados
        self.db.insert_transaction(descricao, valor, tipo)

        self.tree.insert("", "end", values=(descricao, f"R$ {valor:.2f}", tipo))

        self.desc_entry.delete(0, ctk.END)
        self.valor_entry.delete(0, ctk.END)

    def load_transactions(self):
        transactions = self.db.get_all_transactions()
        for transacao in transactions:
            descricao, valor, tipo = transacao
            self.tree.insert("", "end", values=(descricao, f"R$ {valor:.2f}", tipo))
            if tipo == "Entrada":
                self.entradas += valor
            else:
                self.saidas += valor
        self.total = self.entradas - self.saidas
        self.update_labels()

    def update_labels(self):
        self.entradas_label.configure(text=f"Entradas\nR$ {self.entradas:.2f}")
        self.saidas_label.configure(text=f"Saídas\nR$ {self.saidas:.2f}")
        self.total_label.configure(text=f"Total\nR$ {self.total:.2f}")

    def generate_report(self):
        # Collect data for the graph
        transactions = self.db.get_all_transactions()
        entradas = sum([valor for descricao, valor, tipo in transactions if tipo == "Entrada"])
        saidas = sum([valor for descricao, valor, tipo in transactions if tipo == "Saída"])

        # Create the pie chart
        labels = 'Entradas', 'Saídas'
        sizes = [entradas, saidas]
        colors = ['#00FF00', '#FF0000']
        explode = (0.1, 0)  # explode 1st slice

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Display the graph in the Tkinter window
        canvas = FigureCanvasTkAgg(fig1, master=self.root)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)

    def export_to_csv(self):
        transactions = self.db.get_all_transactions()
        with open('transacoes.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Descrição', 'Valor', 'Tipo'])
            for transacao in transactions:
                writer.writerow(transacao)
        messagebox.showinfo("Exportar CSV", "Transações exportadas com sucesso para transacoes.csv")

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x200")

        self.db = Database()

        login_frame = ctk.CTkFrame(self.root, corner_radius=10)
        login_frame.pack(pady=20, padx=20, fill="both", expand=True)

        username_label = ctk.CTkLabel(login_frame, text="Usuário")
        username_label.pack(pady=5)
        self.username_entry = ctk.CTkEntry(login_frame)
        self.username_entry.pack(pady=5)

        password_label = ctk.CTkLabel(login_frame, text="Senha")
        password_label.pack(pady=5)
        self.password_entry = ctk.CTkEntry(login_frame)
        self.password_entry.pack(pady=5)

        login_button = ctk.CTkButton(login_frame, text="Login", command=self.verify_login)
        login_button.pack(pady=10)

    def verify_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.db.verify_user(username, password):
            self.root.destroy()
            root = ctk.CTk()
            app = FinanceControl(root)
            root.mainloop()
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha inválidos")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    login_app = Login(root)
    root.mainloop()
