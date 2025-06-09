import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Caminho para o arquivo onde os dados serão armazenados
FILE_PATH = r"C:\Users\usuario\Downloads\RAD_CRUD_-main\registro.txt"
# Caminho para a imagem de fundo (use o caminho da sua imagem real)
BACKGROUND_IMAGE_PATH = r"C:\Users\usuario\Downloads\RAD_CRUD_-main\ACREATIVE.png" # <<< ATENÇÃO: Use o caminho da sua imagem!

# --- Funções de Utilitário e CRUD (permanecem as mesmas) ---

def verificar_arquivo():
    diretorio = os.path.dirname(FILE_PATH)
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
    if not os.path.isfile(FILE_PATH):
        with open(FILE_PATH, 'w') as f:
            pass

def salvar_dados(tipo, dados):
    verificar_arquivo()
    with open(FILE_PATH, 'a') as f:
        f.write(f"{tipo};{';'.join(dados)}\n")
    messagebox.showinfo("Sucesso", f"{tipo} cadastrado com sucesso!")

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
                    if len(dados) >= 9:
                        if campo.lower() == "nome" and valor in dados[1].lower():
                            resultados.append(dados)
                        elif campo.lower() == "cpf" and valor == dados[5].lower():
                            resultados.append(dados)
                        elif campo.lower() == "atividade" and valor in dados[8].lower(): # Índice 8 para atividades
                            resultados.append(dados)
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo de registros não encontrado!")
            return

        for widget in resultados_frame.winfo_children():
            widget.destroy()
        if resultados:
            tree = ttk.Treeview(resultados_frame, columns=("Tipo", "Nome", "Endereço", "Cidade", "Estado", "CPF", "E-mail", "Sexo", "Atividades", "Observação"), show="headings")
            tree.pack(fill="both", expand=True)

            tree.heading("Tipo", text="Tipo")
            tree.heading("Nome", text="Nome")
            tree.heading("Endereço", text="Endereço")
            tree.heading("Cidade", text="Cidade")
            tree.heading("Estado", text="Estado")
            tree.heading("CPF", text="CPF")
            tree.heading("E-mail", text="E-mail")
            tree.heading("Sexo", text="Sexo")
            tree.heading("Atividades", text="Atividades")
            tree.heading("Observação", text="Observação")

            tree.column("Tipo", width=70)
            tree.column("Nome", width=150)
            tree.column("CPF", width=100)
            tree.column("Atividades", width=150)

            for resultado in resultados:
                padded_resultado = resultado + [''] * (10 - len(resultado))
                tree.insert("", "end", values=padded_resultado[:10])

        else:
            tk.Label(resultados_frame, text="Nenhum resultado encontrado.", anchor="w", fg="red").pack(fill="x", padx=5, pady=2)

    ttk.Label(janela, text=f"Valor para Pesquisa ({campo.capitalize()}):").grid(row=0, column=0, pady=5, sticky=tk.W)
    ttk.Entry(janela, textvariable=pesquisa_entry, width=40).grid(row=0, column=1, pady=5)
    ttk.Button(janela, text="Consultar", command=realizar_consulta).grid(row=1, column=0, pady=10)
    ttk.Button(janela, text="Fechar", command=janela.destroy).grid(row=1, column=1, pady=10)

def janela_cadastro(tipo):
    janela = tk.Toplevel()
    janela.title(f"Cadastro de {tipo}")

    estado_var = tk.StringVar()
    sexo_var = tk.StringVar(value="Masculino")
    atividades_var = {}

    def salvar():
        nome = nome_entry.get().strip()
        endereco = endereco_entry.get().strip()
        cidade = cidade_entry.get().strip()
        estado = estado_var.get().strip()
        cpf = cpf_entry.get().strip()
        email = email_entry.get().strip()
        sexo = sexo_var.get().strip()
        atividades_selecionadas = [atividade for atividade, var in atividades_var.items() if var.get()]
        observacao = observacao_entry.get("1.0", tk.END).strip()

        if not all([nome, endereco, cidade, estado, cpf, email, sexo]) or not atividades_selecionadas:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios e selecione pelo menos uma atividade!")
            return

        salvar_dados(tipo, [nome, endereco, cidade, estado, cpf, email, sexo, ", ".join(atividades_selecionadas), observacao]) # Corrigido aqui
        janela.destroy()

    ttk.Label(janela, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=5)
    nome_entry = ttk.Entry(janela, width=40)
    nome_entry.grid(row=0, column=1, pady=5)

    ttk.Label(janela, text="Endereço:").grid(row=1, column=0, sticky=tk.W, pady=5)
    endereco_entry = ttk.Entry(janela, width=40)
    endereco_entry.grid(row=1, column=1, pady=5)

    ttk.Label(janela, text="Cidade:").grid(row=2, column=0, sticky=tk.W, pady=5)
    cidade_entry = ttk.Entry(janela, width=40)
    cidade_entry.grid(row=2, column=1, pady=5)

    ttk.Label(janela, text="Estado:").grid(row=3, column=0, sticky=tk.W, pady=5)
    estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
    estado_combo = ttk.Combobox(janela, textvariable=estado_var, values=estados, width=37)
    estado_combo.grid(row=3, column=1, pady=5)
    estado_combo.set("SP")

    ttk.Label(janela, text="CPF:").grid(row=4, column=0, sticky=tk.W, pady=5)
    cpf_entry = ttk.Entry(janela, width=40)
    cpf_entry.grid(row=4, column=1, pady=5)

    ttk.Label(janela, text="E-mail:").grid(row=5, column=0, sticky=tk.W, pady=5)
    email_entry = ttk.Entry(janela, width=40)
    email_entry.grid(row=5, column=1, pady=5)

    ttk.Label(janela, text="Sexo:").grid(row=6, column=0, sticky=tk.W, pady=5)
    sexo_frame = tk.Frame(janela)
    sexo_frame.grid(row=6, column=1, pady=5, sticky=tk.W)
    tk.Radiobutton(sexo_frame, text="Masculino", variable=sexo_var, value="Masculino").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(sexo_frame, text="Feminino", variable=sexo_var, value="Feminino").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(sexo_frame, text="Outros", variable=sexo_var, value="Outros").pack(side=tk.LEFT, padx=5)

    ttk.Label(janela, text="Atividades:").grid(row=7, column=0, sticky=tk.W, pady=5)
    atividades_frame = tk.Frame(janela)
    atividades_frame.grid(row=7, column=1, pady=5, sticky=tk.W)
    atividades_opcoes = ["Musculação", "CrossFit", "Natação", "Dança", "Yoga", "Luta"]
    for atividade in atividades_opcoes:
        atividades_var[atividade] = tk.BooleanVar()
        tk.Checkbutton(atividades_frame, text=atividade, variable=atividades_var[atividade]).pack(side=tk.LEFT, padx=2)

    ttk.Label(janela, text="Observação:").grid(row=8, column=0, sticky=tk.W, pady=5)
    observacao_entry = tk.Text(janela, height=4, width=38)
    observacao_entry.grid(row=8, column=1, pady=5)

    ttk.Button(janela, text="Salvar", command=salvar).grid(row=9, column=0, pady=10)
    ttk.Button(janela, text="Cancelar", command=janela.destroy).grid(row=9, column=1, pady=10)

def alterar_registro():
    def buscar():
        cpf_pesquisa = cpf_entry.get().strip()
        if not cpf_pesquisa:
            messagebox.showerror("Erro", "Digite um CPF para buscar.")
            return

        with open(FILE_PATH, 'r') as f:
            linhas = f.readlines()

        encontrado = False
        for linha in linhas:
            dados = linha.strip().split(';')
            if len(dados) >= 10 and dados[5] == cpf_pesquisa:
                preencher_campos(dados)
                encontrado = True
                break

        if not encontrado:
            messagebox.showinfo("Não encontrado", "Cadastro não localizado.")

    def salvar():
        _tipo = tipo_var.get().strip()
        _nome = nome.get().strip()
        _endereco = endereco.get().strip()
        _cidade = cidade.get().strip()
        _estado = estado.get().strip()
        _cpf = cpf.get().strip()
        _email = email.get().strip()
        _sexo = sexo.get().strip()
        _atividades = atividades.get().strip()
        _observacao = observacao.get("1.0", tk.END).strip()

        if not all([_tipo, _nome, _endereco, _cidade, _estado, _cpf, _email, _sexo, _atividades]):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos para alteração.")
            return

        novo_dado = [_tipo, _nome, _endereco, _cidade, _estado, _cpf, _email, _sexo, _atividades, _observacao]

        with open(FILE_PATH, 'r') as f:
            linhas = f.readlines()

        with open(FILE_PATH, 'w') as f:
            alterado = False
            for linha in linhas:
                dados = linha.strip().split(';')
                if len(dados) >= 6 and dados[5] == _cpf:
                    f.write(";".join(novo_dado) + "\n")
                    alterado = True
                else:
                    f.write(linha)
        
        if alterado:
            messagebox.showinfo("Alterado", "Cadastro alterado com sucesso.")
            janela.destroy()
        else:
            messagebox.showerror("Erro", "Cadastro não encontrado para alteração.")

    def preencher_campos(dados):
        if len(dados) >= 10:
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
        else:
            messagebox.showerror("Erro", "Dados do registro estão incompletos no arquivo.")

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

    ttk.Label(janela, text="CPF para Buscar:").grid(row=0, column=0, sticky=tk.W, pady=5)
    cpf_entry = ttk.Entry(janela, textvariable=cpf, width=40)
    cpf_entry.grid(row=0, column=1, pady=5)
    ttk.Button(janela, text="Buscar", command=buscar).grid(row=0, column=2, pady=5, padx=5)

    campos = [("Tipo", tipo_var), ("Nome", nome), ("Endereço", endereco), ("Cidade", cidade),
              ("Estado", estado), ("E-mail", email), ("Sexo", sexo), ("Atividades", atividades)]
    
    for i, (label, var) in enumerate(campos, start=1):
        ttk.Label(janela, text=f"{label}:").grid(row=i, column=0, sticky=tk.W, pady=2)
        ttk.Entry(janela, textvariable=var, width=40).grid(row=i, column=1, columnspan=2, pady=2)

    ttk.Label(janela, text="Observação:").grid(row=9, column=0, sticky=tk.W, pady=2)
    observacao = tk.Text(janela, height=4, width=38)
    observacao.grid(row=9, column=1, columnspan=2, pady=2)

    ttk.Button(janela, text="Salvar Alterações", command=salvar).grid(row=10, column=1, pady=10)
    ttk.Button(janela, text="Cancelar", command=janela.destroy).grid(row=10, column=2, pady=10)

def excluir_cadastro():
    def excluir():
        cpf_excluir = cpf_entry.get().strip()
        if not cpf_excluir:
            messagebox.showerror("Erro", "Digite um CPF para excluir.")
            return

        try:
            with open(FILE_PATH, 'r') as f:
                linhas = f.readlines()

            with open(FILE_PATH, 'w') as f:
                excluido = False
                for linha in linhas:
                    dados = linha.strip().split(';')
                    if len(dados) >= 6 and dados[5] != cpf_excluir:
                        f.write(linha)
                    elif len(dados) >= 6 and dados[5] == cpf_excluir:
                        excluido = True
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo de registros não encontrado.")
            return

        if excluido:
            messagebox.showinfo("Sucesso", "Cadastro excluído com sucesso.")
        else:
            messagebox.showinfo("Não encontrado", "Cadastro não localizado.")
        janela.destroy()

    janela = tk.Toplevel()
    janela.title("Excluir Cadastro")

    ttk.Label(janela, text="Digite o CPF para excluir:").grid(row=0, column=0, sticky=tk.W, pady=5)
    cpf_entry = ttk.Entry(janela, width=40)
    cpf_entry.grid(row=0, column=1, pady=5)
    ttk.Button(janela, text="Excluir", command=excluir).grid(row=1, column=0, pady=10)
    ttk.Button(janela, text="Cancelar", command=janela.destroy).grid(row=1, column=1, pady=10)

def gerar_relatorios():
    tipos = {}
    atividades = {}

    try:
        with open(FILE_PATH, 'r') as f:
            for linha in f:
                dados = linha.strip().split(';')
                if len(dados) >= 9:
                    tipo = dados[0]
                    tipos[tipo] = tipos.get(tipo, 0) + 1

                    for atv in dados[8].split(', '):
                        if atv:
                            atividades[atv] = atividades.get(atv, 0) + 1
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo de registros não encontrado!")
        return

    texto = "Relatório de Cadastros:\n\n"
    for tipo, qt in tipos.items():
        texto += f"- {tipo}: {qt} registros\n"

    texto += "\nRelatório por Atividades:\n"
    for atv, qt in atividades.items():
        texto += f"- {atv}: {qt} ocorrências\n"

    messagebox.showinfo("Relatórios", texto)

# --- NOVA FUNÇÃO para o botão "ENTRAR" ---
def janela_entrar():
    janela_login = tk.Toplevel()
    janela_login.title("Área de Acesso")

    # Frame para centralizar o conteúdo
    content_frame = ttk.Frame(janela_login, padding="20 20 20 20")
    content_frame.pack(expand=True, fill="both")

    ttk.Label(content_frame, text="Acesso Restrito", font=("Arial", 14, "bold")).pack(pady=15)

    # Botões para as opções de Consulta e Administrativo
    ttk.Button(content_frame, text="Consultar por Nome", command=lambda: janela_consulta("nome")).pack(pady=5, ipadx=10, ipady=5)
    ttk.Button(content_frame, text="Consultar por CPF", command=lambda: janela_consulta("cpf")).pack(pady=5, ipadx=10, ipady=5)
    ttk.Button(content_frame, text="Consultar por Atividade", command=lambda: janela_consulta("atividade")).pack(pady=5, ipadx=10, ipady=5)
    
    ttk.Separator(content_frame, orient="horizontal").pack(fill="x", pady=10)

    ttk.Button(content_frame, text="Alterar Registro", command=alterar_registro).pack(pady=5, ipadx=10, ipady=5)
    ttk.Button(content_frame, text="Excluir Cadastro", command=excluir_cadastro).pack(pady=5, ipadx=10, ipady=5)
    ttk.Button(content_frame, text="Gerar Relatórios", command=gerar_relatorios).pack(pady=5, ipadx=10, ipady=5) # Corrigido o nome da função aqui

    ttk.Button(content_frame, text="Fechar", command=janela_login.destroy).pack(pady=20)


# --- Menu principal (agora com os botões personalizados) ---
def menu_principal():
    janela = tk.Tk()
    janela.title("ACREATIVE GYM ACADEMIA")

    # Configurar estilo dos botões personalizados
    style = ttk.Style()

# Botão 1 (INSCREVA-SE HOJE) - Amarelo dourado
    style.configure('YellowButton.TButton', 
                background='#FFD700', 
                foreground='black', 
                font=('Arial', 14, 'bold'),
                padding=10,
                relief='raised',
                borderwidth=3)
    style.map('YellowButton.TButton', 
          background=[('active', '#FFEB3B')])

# Botão 2 (ENTRAR) - Amarelo personalizado
    style.configure('DarkButton.TButton', 
                background='#FFD700',  # Mesmo amarelo do primeiro botão
                foreground='black', 
                font=('Arial', 12, 'bold'),
                padding=8,
                relief='raised',
                borderwidth=2)
    style.map('DarkButton.TButton', 
          background=[('active', '#FFEB3B')])


    # Tenta carregar a imagem de fundo
    try:
        img = Image.open(BACKGROUND_IMAGE_PATH)
        janela_width = 800
        janela_height = 600
        img = img.resize((janela_width, janela_height), Image.LANCZOS)
        
        bg_image = ImageTk.PhotoImage(img)

        background_label = tk.Label(janela, image=bg_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = bg_image # Mantém uma referência
        
        janela.geometry(f"{janela_width}x{janela_height}")
        janela.resizable(False, False) # Impede redimensionamento para manter imagem

    except FileNotFoundError:
        messagebox.showwarning("Aviso", f"Imagem de fundo não encontrada em: {BACKGROUND_IMAGE_PATH}. O sistema continuará sem ela.")
        janela.geometry("800x600")
    except Exception as e:
        messagebox.showerror("Erro ao carregar imagem", f"Ocorreu um erro ao carregar a imagem de fundo: {e}")
        janela.geometry("800x600")

    # Frame para os elementos principais da tela de boas-vindas
    # SEM bg='transparent' aqui. O Tkinter pode não desenhar o frame, permitindo a imagem de fundo.
    main_content_frame = tk.Frame(
    janela,
    bg='white',          # Fundo branco
    bd=3,                # Largura da borda (em pixels)
    relief='solid',      # Estilo da borda (sólida)
    highlightthickness=0  # Remove contorno extra (opcional)
    )
    
    main_content_frame.pack(side=tk.BOTTOM, pady=80)

    # Logo/Título "ACREATIVE GYM ACADEMIA" - Definir bg para a cor que você quer (ex: a cor da imagem) ou 'transparent'
    # 'transparent' aqui (no Label) pode funcionar sobre outro Label (o background_label)
    

    # Botões personalizados
    ttk.Button(main_content_frame, text="INSCREVA-SE HOJE", 
               command=lambda: janela_cadastro("Aluno"), 
               style='YellowButton.TButton',
               width=25).pack(pady=10)

    ttk.Button(main_content_frame, text="ENTRAR", 
               command=janela_entrar,
               style='DarkButton.TButton',
               width=20).pack(pady=5)
    
    janela.mainloop()

# Executar o sistema
if __name__ == "__main__":
    verificar_arquivo()
    menu_principal()