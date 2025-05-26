import os
import tkinter as tk
from tkinter import ttk, messagebox

# Caminho para o arquivo onde os dados serão armazenados
FILE_PATH = r"C:\Users\samue\OneDrive\Documentos\Cursos\Aula_rad\registro.txt"

# Função para garantir que o diretório e o arquivo existam
def verificar_arquivo():
    diretorio = os.path.dirname(FILE_PATH)
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
    if not os.path.isfile(FILE_PATH):
        with open(FILE_PATH, 'w') as f:
            pass

# Função para salvar os dados no arquivo
def salvar_dados(tipo, dados):
    verificar_arquivo()
    with open(FILE_PATH, 'a') as f:
        f.write(f"{tipo};{';'.join(dados)}\n")
    messagebox.showinfo("Sucesso", f"{tipo} cadastrado com sucesso!")

# Função para realizar consultas
def janela_consulta(campo):
    janela = tk.Toplevel()
    janela.title(f"Consulta por {campo.capitalize()}")

    pesquisa_entry = tk.StringVar()
    resultados_frame = tk.Frame(janela)
    resultados_frame.grid(row=2, column=0, columnspan=2, pady=10)

    def realizar_consulta():
        valor = pesquisa_entry.get().strip().lower()
        resultados = []
        try:
            with open(FILE_PATH, 'r') as f:
                for linha in f:
                    dados = linha.strip().split(";")
                    if campo.lower() == "nome" and valor in dados[1].lower():
                        resultados.append(dados)
                    elif campo.lower() == "cpf" and valor == dados[5].lower():
                        resultados.append(dados)
                    elif campo.lower() == "atividade" and valor in dados[7].lower():
                        resultados.append(dados)
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo de registros não encontrado!")
            return

        for widget in resultados_frame.winfo_children():
            widget.destroy()
        if resultados:
            for resultado in resultados:
                tk.Label(resultados_frame, text=" | ".join(resultado), anchor="w").pack(fill="x", padx=5, pady=2)
        else:
            tk.Label(resultados_frame, text="Nenhum resultado encontrado.", anchor="w", fg="red").pack(fill="x", padx=5, pady=2)

    ttk.Label(janela, text=f"Valor para Pesquisa ({campo.capitalize()}):").grid(row=0, column=0, pady=5, sticky=tk.W)
    ttk.Entry(janela, textvariable=pesquisa_entry, width=40).grid(row=0, column=1, pady=5)
    ttk.Button(janela, text="Consultar", command=realizar_consulta).grid(row=1, column=0, pady=10)
    ttk.Button(janela, text="Fechar", command=janela.destroy).grid(row=1, column=1, pady=10)

# Função para cadastro de dados
def janela_cadastro(tipo):
    janela = tk.Toplevel()
    janela.title(f"Cadastro de {tipo}")

    estado_var = tk.StringVar()
    sexo_var = tk.StringVar(value="Masculino")
    atividades_var = {}

    def salvar():
        nome = nome_entry.get()
        endereco = endereco_entry.get()
        cidade = cidade_entry.get()
        estado = estado_var.get()
        cpf = cpf_entry.get()
        email = email_entry.get()
        sexo = sexo_var.get()
        atividades = [atividade for atividade, var in atividades_var.items() if var.get()]
        observacao = observacao_entry.get("1.0", tk.END).strip()

        if not all([nome, endereco, cidade, estado, cpf, email, sexo, atividades]):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return

        salvar_dados(tipo, [nome, endereco, cidade, estado, cpf, email, sexo, ", ".join(atividades), observacao])
        janela.destroy()

    ttk.Label(janela, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=5)
    nome_entry = ttk.Entry(janela)
    nome_entry.grid(row=0, column=1, pady=5)

    ttk.Label(janela, text="Endereço:").grid(row=1, column=0, sticky=tk.W, pady=5)
    endereco_entry = ttk.Entry(janela)
    endereco_entry.grid(row=1, column=1, pady=5)

    ttk.Label(janela, text="Cidade:").grid(row=2, column=0, sticky=tk.W, pady=5)
    cidade_entry = ttk.Entry(janela)
    cidade_entry.grid(row=2, column=1, pady=5)

    ttk.Label(janela, text="Estado:").grid(row=3, column=0, sticky=tk.W, pady=5)
    estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
    estado_combo = ttk.Combobox(janela, textvariable=estado_var, values=estados)
    estado_combo.grid(row=3, column=1, pady=5)

    ttk.Label(janela, text="CPF:").grid(row=4, column=0, sticky=tk.W, pady=5)
    cpf_entry = ttk.Entry(janela)
    cpf_entry.grid(row=4, column=1, pady=5)

    ttk.Label(janela, text="E-mail:").grid(row=5, column=0, sticky=tk.W, pady=5)
    email_entry = ttk.Entry(janela)
    email_entry.grid(row=5, column=1, pady=5)

    ttk.Label(janela, text="Sexo:").grid(row=6, column=0, sticky=tk.W, pady=5)
    sexo_frame = tk.Frame(janela)
    sexo_frame.grid(row=6, column=1, pady=5)
    tk.Radiobutton(sexo_frame, text="Masculino", variable=sexo_var, value="Masculino").pack(side=tk.LEFT)
    tk.Radiobutton(sexo_frame, text="Feminino", variable=sexo_var, value="Feminino").pack(side=tk.LEFT)
    tk.Radiobutton(sexo_frame, text="Outros", variable=sexo_var, value="Outros").pack(side=tk.LEFT)

    ttk.Label(janela, text="Atividades:").grid(row=7, column=0, sticky=tk.W, pady=5)
    atividades_frame = tk.Frame(janela)
    atividades_frame.grid(row=7, column=1, pady=5)
    atividades = ["Musculação", "CrossFit", "Natação", "Dança", "Todos"]
    for atividade in atividades:
        atividades_var[atividade] = tk.BooleanVar()
        tk.Checkbutton(atividades_frame, text=atividade, variable=atividades_var[atividade]).pack(side=tk.LEFT)

    ttk.Label(janela, text="Observação:").grid(row=8, column=0, sticky=tk.W, pady=5)
    observacao_entry = tk.Text(janela, height=4, width=40)
    observacao_entry.grid(row=8, column=1, pady=5)

    ttk.Button(janela, text="Salvar", command=salvar).grid(row=9, column=0, pady=10)
    ttk.Button(janela, text="Cancelar", command=janela.destroy).grid(row=9, column=1, pady=10)

# Funções administrativas

def alterar_registro():
    def buscar():
        cpf = cpf_entry.get().strip()
        if not cpf:
            messagebox.showerror("Erro", "Digite um CPF para buscar.")
            return

        with open(FILE_PATH, 'r') as f:
            linhas = f.readlines()

        for linha in linhas:
            dados = linha.strip().split(';')
            if dados[5] == cpf:
                preencher_campos(dados)
                return

        messagebox.showinfo("Não encontrado", "Cadastro não localizado.")

    def salvar():
        novo_dado = [tipo_var.get(), nome.get(), endereco.get(), cidade.get(), estado.get(), cpf.get(), email.get(), sexo.get(), atividades.get(), observacao.get("1.0", tk.END).strip()]
        with open(FILE_PATH, 'r') as f:
            linhas = f.readlines()

        with open(FILE_PATH, 'w') as f:
            for linha in linhas:
                dados = linha.strip().split(';')
                if dados[5] == cpf.get():
                    f.write(";".join(novo_dado) + "\n")
                else:
                    f.write(linha)

        messagebox.showinfo("Alterado", "Cadastro alterado com sucesso.")
        janela.destroy()

    def preencher_campos(dados):
        tipo_var.set(dados[0])
        nome.set(dados[1])
        endereco.set(dados[2])
        cidade.set(dados[3])
        estado.set(dados[4])
        cpf.set(dados[5])
        email.set(dados[6])
        sexo.set(dados[7])
        atividades.set(dados[8])
        observacao.delete("1.0", tk.END)
        observacao.insert(tk.END, dados[9])

    janela = tk.Toplevel()
    janela.title("Alterar Cadastro")

    tipo_var = tk.StringVar()
    nome = tk.StringVar()
    endereco = tk.StringVar()
    cidade = tk.StringVar()
    estado = tk.StringVar()
    cpf = tk.StringVar()
    email = tk.StringVar()
    sexo = tk.StringVar()
    atividades = tk.StringVar()

    ttk.Label(janela, text="CPF:").grid(row=0, column=0)
    cpf_entry = ttk.Entry(janela, textvariable=cpf)
    cpf_entry.grid(row=0, column=1)
    ttk.Button(janela, text="Buscar", command=buscar).grid(row=0, column=2)

    campos = [("Tipo", tipo_var), ("Nome", nome), ("Endereço", endereco), ("Cidade", cidade), ("Estado", estado), ("E-mail", email), ("Sexo", sexo), ("Atividades", atividades)]
    for i, (label, var) in enumerate(campos, start=1):
        ttk.Label(janela, text=f"{label}:").grid(row=i, column=0)
        ttk.Entry(janela, textvariable=var).grid(row=i, column=1, columnspan=2)

    ttk.Label(janela, text="Observação:").grid(row=9, column=0)
    observacao = tk.Text(janela, height=4, width=40)
    observacao.grid(row=9, column=1, columnspan=2)

    ttk.Button(janela, text="Salvar Alterações", command=salvar).grid(row=10, column=1, pady=10)
    ttk.Button(janela, text="Cancelar", command=janela.destroy).grid(row=10, column=2, pady=10)

def excluir_cadastro():
    def excluir():
        cpf = cpf_entry.get().strip()
        if not cpf:
            messagebox.showerror("Erro", "Digite um CPF para excluir.")
            return

        with open(FILE_PATH, 'r') as f:
            linhas = f.readlines()

        with open(FILE_PATH, 'w') as f:
            excluido = False
            for linha in linhas:
                dados = linha.strip().split(';')
                if dados[5] != cpf:
                    f.write(linha)
                else:
                    excluido = True

        if excluido:
            messagebox.showinfo("Sucesso", "Cadastro excluído com sucesso.")
        else:
            messagebox.showinfo("Não encontrado", "Cadastro não localizado.")
        janela.destroy()

    janela = tk.Toplevel()
    janela.title("Excluir Cadastro")

    ttk.Label(janela, text="Digite o CPF para excluir:").grid(row=0, column=0)
    cpf_entry = ttk.Entry(janela)
    cpf_entry.grid(row=0, column=1)
    ttk.Button(janela, text="Excluir", command=excluir).grid(row=1, column=0, pady=10)
    ttk.Button(janela, text="Cancelar", command=janela.destroy).grid(row=1, column=1, pady=10)

def gerar_relatorios():
    tipos = {}
    atividades = {}

    try:
        with open(FILE_PATH, 'r') as f:
            for linha in f:
                dados = linha.strip().split(';')
                tipo = dados[0]
                tipos[tipo] = tipos.get(tipo, 0) + 1

                for atv in dados[8].split(', '):
                    atividades[atv] = atividades.get(atv, 0) + 1
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo de registros não encontrado!")
        return

    texto = "Relatório de Cadastros:\n\n"
    for tipo, qt in tipos.items():
        texto += f"{tipo}: {qt}\n"

    texto += "\nRelatório por Atividades:\n"
    for atv, qt in atividades.items():
        texto += f"{atv}: {qt}\n"

    messagebox.showinfo("Relatórios", texto)

# Menu principal
def menu_principal():
    janela = tk.Tk()
    janela.title("Sistema de Cadastro")

    menu = tk.Menu(janela)
    janela.config(menu=menu)

    cadastro_menu = tk.Menu(menu, tearoff=0)
    consulta_menu = tk.Menu(menu, tearoff=0)
    administrativo_menu = tk.Menu(menu, tearoff=0)

    menu.add_cascade(label="Cadastro", menu=cadastro_menu)
    menu.add_cascade(label="Consulta", menu=consulta_menu)
    menu.add_cascade(label="Administrativo", menu=administrativo_menu)

    cadastro_menu.add_command(label="Aluno", command=lambda: janela_cadastro("Aluno"))
    cadastro_menu.add_command(label="Funcionário", command=lambda: janela_cadastro("Funcionário"))
    cadastro_menu.add_command(label="Professor", command=lambda: janela_cadastro("Professor"))

    consulta_menu.add_command(label="Por Nome", command=lambda: janela_consulta("nome"))
    consulta_menu.add_command(label="Por CPF", command=lambda: janela_consulta("cpf"))
    consulta_menu.add_command(label="Por Atividade", command=lambda: janela_consulta("atividade"))

    administrativo_menu.add_command(label="Alterar Registro", command=alterar_registro)
    administrativo_menu.add_command(label="Excluir Cadastro", command=excluir_cadastro)
    administrativo_menu.add_command(label="Gerar Relatórios", command=gerar_relatorios)

    ttk.Label(janela, text="Bem-vindo ao Sistema de Cadastro").pack(pady=20)
    ttk.Button(janela, text="Sair", command=janela.destroy).pack(pady=10)

    janela.mainloop()

# Executar o sistema
if __name__ == "__main__":
    menu_principal()
