import tkinter as tk
from tkinter import ttk, messagebox #ttk da um estilo pros widgets]

class app(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		#Adiciona menubar na aplicação
		menubar = tk.Menu(self, font=("Verdana", "9"), background="#4682B4",fg='white', activebackground='#011C56', activeforeground='white', tearoff=1)
		menubar.add_command(label="SubscribePage", command=lambda: self.show_frame(SubscribePage))
		menubar.add_command(label="ChatListPage", command=lambda: self.show_frame(ChatListPage))
		menubar.add_command(label="ChatConfigPage", command=lambda: self.show_frame(ChatConfigPage))
		menubar.add_command(label="ChatPage", command=lambda: self.show_frame(ChatPage))
		self.config(menu=menubar)
    
		#Coloca o Título do app
		tk.Tk.wm_title(self, "UDPChat")

    	#Cria o conteiner onde as paginas criadas serão encaixadas
		container = tk.Frame(self)

		container.pack(side="top", fill="both", expand=True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		#Dicionário de páginas
		self.frames = {}
		#Adiciona as paginas no dicionário para serem usadas pelo show_frame e o tamanho de cada
		for F, geometry in zip((ChatPage,ChatConfigPage,ChatListPage,SubscribePage),('300x400','300x200','300x200','270x200')):
#								((ChatConfigPage,ChatListPage,SubscribePage),('720x1080','220x150','220x150'))
			frame = F(container, self)

			self.frames[F] = (frame, geometry)

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(SubscribePage)

	#Traz a pagina que foi adicionada no dicionário ao topo
	def show_frame(self, page_name):
		frame, geometry = self.frames[page_name]
		self.update_idletasks()
		self.geometry(geometry)
		frame.tkraise()


class SubscribePage(tk.Frame):					#Essa parte inicia a pagina como um Frame
	def __init__(self, parent, controller):	#
		tk.Frame.__init__(self, parent)		#

		#Isso adiciona um label na nossa pagina, o processo é o mesmo pra adicionar outras coisas
		label = ttk.Label(self, text="Subscribe Page", font=("Verdana", "12"))
		label.grid(row=0, columnspan=2, pady=10)

		label1 = ttk.Label(self, text="Username:")
		label1.grid(row=1, column=0, sticky="w")
		global ed1
		ed1 = tk.Entry(self)
		ed1.grid(row=1, column=1, sticky="w")

		label2 = tk.Label(self, text="Server Address:")
		label2.grid(row=2, column=0, sticky="w")
		global ed2
		ed2 = tk.Entry(self, show="*")
		ed2.grid(row=2, column=1, sticky="w")

		label3 = tk.Label(self, text="Client Port:")
		label3.grid(row=3, column=0, sticky="w")
		global ed3
		ed3 = tk.Entry(self, show="*")
		ed3.grid(row=3, column=1, sticky="w")

		button1 = tk.Button(self, text="OK", highlightbackground='#3E4149', bg='#B0C4DE', relief='raised', fg='black', activebackground='#4682B4',activeforeground='white', command=lambda: faz_login(ChatListPage, controller))
		button1.grid(row=4, columnspan=2, pady=10)

		labelstatus = ttk.Label(self, text="Conection status\n...", font=("Verdana", "11"))
		labelstatus.grid(row=5, columnspan=2, pady=10)

class ChatListPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		label = tk.Label(self, text="Escolha um chat", font=("Verdana", "10"))
		label.pack(pady=10)

		itemsforlistbox=[x for x in range(100)]

		#var2 = tk.StringVar()
		#var2.set([x for x in range(100)])
		#listaDeChats = tk.Listbox(self, listvariable=var2)
		listaDeChats = tk.Listbox(self)
		def print_selection(event):
			value = str(listaDeChats.get(listaDeChats.curselection()))   
			label.config(text=str(value))
			print(value)
		listaDeChats.bind('<<ListboxSelect>>', print_selection)
		listaDeChats.pack(side = tk.LEFT, fill = tk.BOTH)
		for items in itemsforlistbox:
			listaDeChats.insert(tk.END,items)

		scrollbar = tk.Scrollbar(self)
		scrollbar.pack(side = tk.LEFT, fill = tk.BOTH)

		listaDeChats.config(yscrollcommand = scrollbar.set) 
		scrollbar.config(command = listaDeChats.yview)
		

		button3 = tk.Button(self, text="New Chat +", width='12', highlightbackground='#3E4149', bg='#FD8403', relief='raised', fg='black', activebackground='#CB6A02',activeforeground='white', command=print("botao"))
		button3.pack(pady=10)

class ChatConfigPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		#Isso adiciona um label na nossa pagina, o processo é o mesmo pra adicionar outras coisas
		label = ttk.Label(self, text="Subscribe Page", font=("Verdana", "12"))
		label.grid(row=0, columnspan=2, pady=10)

		label1 = ttk.Label(self, text="Username:")
		label1.grid(row=1, column=0, sticky="w")

		global ed1
		ed1 = tk.Entry(self)
		ed1.grid(row=1, column=1, sticky="w")

		label2 = tk.Label(self, text="Server Address:")
		label2.grid(row=2, column=0, sticky="w")

		global ed2
		ed2 = tk.Entry(self, show="*")
		ed2.grid(row=2, column=1, sticky="w")
		button1 = tk.Button(self, text="OK", highlightbackground='#3E4149', bg='#B0C4DE', relief='raised', fg='black', activebackground='#4682B4',activeforeground='white', command=lambda: faz_login(ChatListPage, controller))
		button1.grid(row=3, columnspan=2, pady=10)

class ChatPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		#Isso adiciona um label na nossa pagina, o processo é o mesmo pra adicionar outras coisas
		label = ttk.Label(self, text="Subscribe Page", font=("Verdana", "12"))
		label.grid(row=0, columnspan=2, pady=10)

		label1 = ttk.Label(self, text="Username:")
		label1.grid(row=1, column=0, sticky="w")

		global ed1
		ed1 = tk.Entry(self)
		ed1.grid(row=1, column=1, sticky="w")

		label2 = tk.Label(self, text="Server Address:")
		label2.grid(row=2, column=0, sticky="w")

		global ed2
		ed2 = tk.Entry(self, show="*")
		ed2.grid(row=2, column=1, sticky="w")
		button1 = tk.Button(self, text="OK", highlightbackground='#3E4149', bg='#B0C4DE', relief='raised', fg='black', activebackground='#4682B4',activeforeground='white', command=lambda: faz_login(ChatListPage, controller))
		button1.grid(row=3, columnspan=2, pady=10)


app = app()

#Centraliza app na tela
app.eval('tk::PlaceWindow %s center' % app.winfo_pathname(app.winfo_id()))

app.mainloop()
