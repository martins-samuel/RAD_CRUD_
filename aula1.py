import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
def confirmar():
    messagebox.showinfo("Confirmar", "Login confirmado!")
def cancelar():
    root.destroy()
#Construção de formulário 
#Cria a janela principal 
root = tk.Tk()
root.title("Formulário de Login")#Titulo da janela 
root.geometry("500x500")#tamanho janela
frame = tk.Frame(root)
frame.pack(pady=10)

#cria um rotulo e campo de entrada no login 
login_label = tk.Label(frame, text="Login:")
login_label.grid(row=0, column=0, padx=5, pady=5)#adiciona o rotulo ao frame 
login_entry = tk.Entry(frame)
login_entry.grid(row=0, column=1, padx=5, pady=5)

# cria um rotulo e campo de entrada senha 
senha_label = tk.Label(frame, text ="Senha: ")
senha_label.grid(row=1, column = 0, padx=5, pady=5)
senha_entry = tk.Entry(frame, show="*")
senha_entry.grid(row=1, column = 1, padx=5, pady=5)
# 
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
# Cria um botão para confirmar o login 
confirmar_button = tk.Button(button_frame, text ="Confirmar", command=confirmar)
confirmar_button.grid(row=0,column = 1, padx = 5) 
#
image_path = r"C:\Users\samue\OneDrive\Documentos\Cursos\Aula_rad\images.png"
if os.path.exists(image_path):
    try:
        image = Image.open(image_path)
        image = image.resize((200, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        #cria um rotulo para exibir a imagem
        image_label = tk.Label(root, image=photo)
        image_label.image = photo 
        image_label.pack(pady=10)
    except Exception as e:
        messagebox.showerror("Erro",f"Erro ao abrir a imagem:{e}")
else:
    messagebox.showerror("erro",f"Arquivo não encontrado : {image_path}")
#ultima linha 
root.mainloop()

 