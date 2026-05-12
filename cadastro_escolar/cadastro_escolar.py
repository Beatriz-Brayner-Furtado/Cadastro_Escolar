import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector # type: ignore

#CORES

AZUL = "#2786c4"
FUNDO = "#F1F4F7"

#JANELA

janela = tk.Tk()
janela.title("Sistema Escolar")
janela.geometry("1000x700")
janela.configure(bg=FUNDO)

#CONEXÃO MYSQL

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="beatriz",
        password="555555Br@yner",
        database="escola2"
    )

    cursor = conn.cursor()

except mysql.connector.Error as erro:
    print("Erro:", erro)

#FUNÇÕES

def limpa_frame():
    for widget in frame_conteudo.winfo_children():
        widget.destroy()


def cadastrar():
    limpa_frame()

    titulo = tk.Label(
        frame_conteudo,
        text="Cadastrar Aluno",
        font=("Arial", 20, "bold"),
        bg=FUNDO
    )
    titulo.pack(pady=20)

    tk.Label(
        frame_conteudo,
        text="Nome do aluno:",
        font=("Arial", 12),
        bg=FUNDO
    ).pack()

    entry_nome = tk.Entry(
        frame_conteudo,
        width=30,
        font=("Arial", 12)
    )

    entry_nome.pack(pady=10)

    def salvar():

        nome = entry_nome.get()

        if nome == "":
            messagebox.showerror("Erro", "Digite um nome")
            return

        cursor.execute(
            "INSERT INTO alunos(nome) VALUES(%s)",
            (nome,)
        )

        conn.commit()

        messagebox.showinfo("Sucesso", "Aluno cadastrado")

        entry_nome.delete(0, tk.END)

    tk.Button(
        frame_conteudo,
        text="Salvar",
        bg=AZUL,
        fg="white",
        font=("Arial", 12, "bold"),
        width=15,
        bd=0,
        command=salvar
    ).pack(pady=20)


def nota():

    limpa_frame()

    titulo = tk.Label(
        frame_conteudo,
        text="Cadastrar Nota",
        font=("Arial", 20, "bold"),
        bg=FUNDO
    )

    titulo.pack(pady=20)

    tk.Label(
        frame_conteudo,
        text="Nota 1",
        bg=FUNDO
    ).pack()

    entry_nota1 = tk.Entry(frame_conteudo)
    entry_nota1.pack(pady=5)

    tk.Label(
        frame_conteudo,
        text="Nota 2",
        bg=FUNDO
    ).pack()

    entry_nota2 = tk.Entry(frame_conteudo)
    entry_nota2.pack(pady=5)

    tk.Label(
        frame_conteudo,
        text="ID do aluno",
        bg=FUNDO
    ).pack()

    entry_id = tk.Entry(frame_conteudo)
    entry_id.pack(pady=5)

    def salvar():

        try:

            nota1 = float(entry_nota1.get())
            nota2 = float(entry_nota2.get())
            aluno_id = int(entry_id.get())

            cursor.execute(
                """
                INSERT INTO notas(nota1, nota2, nome_id)
                VALUES(%s,%s,%s)
                """,
                (nota1, nota2, aluno_id)
            )

            conn.commit()

            messagebox.showinfo(
                "Sucesso",
                "Notas cadastradas"
            )

        except:
            messagebox.showerror(
                "Erro",
                "Valores inválidos"
            )

    tk.Button(
        frame_conteudo,
        text="Salvar",
        bg=AZUL,
        fg="white",
        font=("Arial", 12, "bold"),
        width=15,
        bd=0,
        command=salvar
    ).pack(pady=20)


def listar_tabela():

    limpa_frame()

    style = ttk.Style()

    style.theme_use("default")

    style.configure(
        "Treeview",
        background="white",
        foreground="black",
        rowheight=30,
        fieldbackground="white",
        font=("Arial", 11)
    )

    style.configure(
        "Treeview.Heading",
        background=AZUL,
        foreground="white",
        font=("Arial", 12, "bold")
    )

    tabela = ttk.Treeview(
        frame_conteudo,
        columns=("id", "nome", "nota1", "nota2"),
        show="headings",
        height=15
    )

    tabela.heading("id", text="ID")
    tabela.heading("nome", text="NOME")
    tabela.heading("nota1", text="NOTA 1")
    tabela.heading("nota2", text="NOTA 2")

    tabela.column("id", width=80, anchor="center")
    tabela.column("nome", width=250, anchor="center")
    tabela.column("nota1", width=150, anchor="center")
    tabela.column("nota2", width=150, anchor="center")

    tabela.pack(
        padx=20,
        pady=20,
        fill="both",
        expand=True
    )

    cursor.execute("""
        SELECT alunos.id,
               alunos.nome,
               notas.nota1,
               notas.nota2
        FROM alunos
        LEFT JOIN notas
        ON alunos.id = notas.nome_id
    """)

    for linha in cursor.fetchall():
        tabela.insert("", tk.END, values=linha)


def excluirT():

    resp = messagebox.askyesno(
        "Confirmação",
        "Deseja excluir tudo?"
    )

    if resp:

        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("DELETE FROM notas")
        cursor.execute("DELETE FROM alunos")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        conn.commit()

        messagebox.showinfo(
            "Sucesso",
            "Dados excluídos"
        )


def atualizar_nome():

    limpa_frame()

    titulo = tk.Label(
        frame_conteudo,
        text="Atualizar Nome",
        font=("Arial", 20, "bold"),
        bg=FUNDO
    )

    titulo.pack(pady=20)

    tk.Label(
        frame_conteudo,
        text="ID do aluno",
        bg=FUNDO
    ).pack()

    entry_id = tk.Entry(frame_conteudo)
    entry_id.pack(pady=5)

    tk.Label(
        frame_conteudo,
        text="Novo nome",
        bg=FUNDO
    ).pack()

    entry_nome = tk.Entry(frame_conteudo)
    entry_nome.pack(pady=5)

    def atualizar():

        try:

            aluno_id = int(entry_id.get())

        except:

            messagebox.showerror(
                "Erro",
                "ID inválido"
            )

            return

        novo_nome = entry_nome.get()

        cursor.execute(
            "UPDATE alunos SET nome=%s WHERE id=%s",
            (novo_nome, aluno_id)
        )

        conn.commit()

        messagebox.showinfo(
            "Sucesso",
            "Nome atualizado"
        )

    tk.Button(
        frame_conteudo,
        text="Atualizar",
        bg=AZUL,
        fg="white",
        font=("Arial", 12, "bold"),
        width=15,
        bd=0,
        command=atualizar
    ).pack(pady=20)

#TOPO

frame_topo = tk.Frame(
    janela,
    bg=AZUL,
    height=90
)

frame_topo.pack(fill="x")
frame_topo.pack_propagate(False)

#LOGO

img = Image.open(
    r"C:\Users\beatr\OneDrive\Documentos\codigo\cadastro_escolar\escola.png"
)

img = img.resize((60, 60))

logo = ImageTk.PhotoImage(img)

label_logo = tk.Label(
    frame_topo,
    image=logo,
    bg=AZUL
)

label_logo.pack(
    side="left",
    padx=20,
    pady=10
)

titulo = tk.Label(
    frame_topo,
    text="Sistema Escolar",
    font=("Arial", 24, "bold"),
    bg=AZUL,
    fg="white"
)

titulo.pack(
    side="left",
    padx=10
)

#MENU LATERAL

frame_menu = tk.Frame(
    janela,
    bg=AZUL,
    width=180
)

frame_menu.pack(
    side="left",
    fill="y"
)

frame_menu.pack_propagate(False)

#CONTEÚDO

frame_conteudo = tk.Frame(
    janela,
    bg=FUNDO
)

frame_conteudo.pack(
    side="right",
    fill="both",
    expand=True
)

#BOTÕES

fonte_btn = ("Arial", 12, "bold")

def criar_botao(texto, comando):

    frame_borda = tk.Frame(
        frame_menu,
        bg="white",
        padx=1,
        pady=1
    )

    frame_borda.pack(
        fill="x",
        pady=7,
        padx=5
    )

    botao = tk.Button(
        frame_borda,
        text=texto,
        font=fonte_btn,
        bg=AZUL,
        fg="white",

        activebackground="#1f7aad",
        activeforeground="white",

        bd=0,
        relief="flat",

        height=3,
        cursor="hand2",
        command=comando
    )

    botao.pack(fill="x")
# ---------------- MENU ----------------

criar_botao("Cadastrar\nAluno", cadastrar)

criar_botao("Cadastrar\nNota", nota)

criar_botao("Listar\nTudo", listar_tabela)

criar_botao("Atualizar\nAluno", atualizar_nome)

criar_botao("Excluir\nTudo", excluirT)

# ---------------- INICIAR ----------------

listar_tabela()

janela.mainloop()