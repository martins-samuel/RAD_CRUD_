from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# (o resto do seu código continua igual...)

# Menu principal com imagem de fundo
def menu_principal():
    janela = Tk()
    janela.title("Sistema de Cadastro de Alunos e Professores")

    # Carrega a imagem de fundo
    imagem_fundo = Image.open("fundo.png")  # Substitua pelo nome da sua imagem
    imagem_fundo = imagem_fundo.resize((800, 600))  # Redimensiona para a janela
    bg = ImageTk.PhotoImage(imagem_fundo)

    canvas = Canvas(janela, width=800, height=600)
    canvas.pack(fill="both", expand=True)

    canvas.create_image(0, 0, image=bg, anchor="nw")  # Define a imagem de fundo

    # Widgets sobre a imagem de fundo
    canvas.create_text(400, 40, text="Sistema de Cadastro", font=("Arial", 20, "bold"), fill="white")

    # Botões como widgets nativos sobrepostos
    botao_cadastrar_aluno = ttk.Button(janela, text="Cadastrar Aluno", command=lambda: janela_cadastro("Aluno"))
    botao_cadastrar_professor = ttk.Button(janela, text="Cadastrar Professor", command=lambda: janela_cadastro("Professor"))
    botao_consulta_nome = ttk.Button(janela, text="Consultar por Nome", command=lambda: janela_consulta("nome"))
    botao_consulta_cpf = ttk.Button(janela, text="Consultar por CPF", command=lambda: janela_consulta("cpf"))
    botao_consulta_atividade = ttk.Button(janela, text="Consultar por Atividade", command=lambda: janela_consulta("atividade"))
    botao_alterar = ttk.Button(janela, text="Alterar Cadastro", command=alterar_registro)
    botao_excluir = ttk.Button(janela, text="Excluir Cadastro", command=excluir_cadastro)
    botao_relatorios = ttk.Button(janela, text="Gerar Relatórios", command=gerar_relatorios)
    botao_sair = ttk.Button(janela, text="Sair", command=janela.destroy)

    # Posicionando os botões sobre o canvas
    canvas.create_window(200, 100, window=botao_cadastrar_aluno)
    canvas.create_window(600, 100, window=botao_cadastrar_professor)
    canvas.create_window(200, 160, window=botao_consulta_nome)
    canvas.create_window(600, 160, window=botao_consulta_cpf)
    canvas.create_window(400, 220, window=botao_consulta_atividade)
    canvas.create_window(200, 280, window=botao_alterar)
    canvas.create_window(600, 280, window=botao_excluir)
    canvas.create_window(400, 340, window=botao_relatorios)
    canvas.create_window(400, 420, window=botao_sair)

    # Manter a imagem viva
    janela.bg = bg

    janela.mainloop()

# Iniciar o programa
if __name__ == "__main__":
    menu_principal()
