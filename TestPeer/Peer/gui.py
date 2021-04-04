import tkinter as tk
from tkinter import ttk, messagebox #ttk da um estilo pros widgets]
import threading, time, json

import ChatConnector
import ChatManager
import UDPPeer
import Chat

objChatConnector = ChatConnector.ChatConnector()
objChatManager = ChatManager.ChatManager(objChatConnector)

class app(tk.Tk):
	def __init__(self, *args, **kwargs):
		global objChatConnector

		tk.Tk.__init__(self, *args, **kwargs)

		#Adiciona menubar na aplicação
		menubar = tk.Menu(self, font=("Verdana", "9"), background="#4682B4",fg='white', activebackground='#011C56', activeforeground='white', tearoff=1)
		menubar.add_command(label="ChatListPage", command=lambda: self.show_frame(ChatListPage, objChatManager=objChatManager))
		menubar.add_command(label="ChatPage", command=lambda: self.show_frame(ChatPage))
		self.config(menu=menubar)
    
		#Coloca o Título do app
		tk.Tk.wm_title(self, "ZappZapp")

    	#Cria o conteiner onde as paginas criadas serão encaixadas
		container = tk.Frame(self)

		container.pack(side="top", fill="both", expand=True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		#Dicionário de páginas
		self.frames = {}
		#Adiciona as paginas no dicionário para serem usadas pelo show_frame e o tamanho de cada
		for F, geometry in zip((SubscribePage,ChatListPage, ChatConfigPage, ChatPage),('270x200', '300x200', '300x200', '300x400')):
			frame = F(container, self)

			self.frames[F] = (frame, geometry)

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(SubscribePage)

	#Traz a pagina que foi adicionada no dicionário ao topo
	def show_frame(self, page_name, objChat=None, objChatManager=None, objChatConnector=None):
		frame, geometry = self.frames[page_name]
		self.update_idletasks()
		self.geometry(geometry)
		if objChat:
			print("Updating chat page with: "+objChat.chatName)
			frame.setChat(objChat=objChat)
		if objChatManager:
			print("Setting objChatManager")
			frame.setChatManager(objChatManager=objChatManager)
		if objChatConnector:
			frame.setChatConnector(objChatConnector=objChatConnector)
			print("Setting objChatConnector")
			frame.refreshUsers()
		frame.tkraise()

class SubscribePage(tk.Frame):					#Essa parte inicia a pagina como um Frame
	def __init__(self, parent, controller):	#
		global objChatConnector
		tk.Frame.__init__(self, parent)		#

		with open('config.json', 'r', encoding='utf-8') as config:
			config = json.loads(config.read())["ChatConnectorConfig"]

		#Isso adiciona um label na nossa pagina, o processo é o mesmo pra adicionar outras coisas
		label = ttk.Label(self, text="Subscribe Page", font=("Verdana", "12"))
		label.grid(row=0, columnspan=2, pady=10)

		label1 = ttk.Label(self, text="Username:")
		label1.grid(row=1, column=0, sticky="w")
		self.ed1 = tk.Entry(self)
		self.ed1.insert(0, config["username"])
		self.ed1.grid(row=1, column=1, sticky="w")

		label2 = tk.Label(self, text="Server IP:")
		label2.grid(row=2, column=0, sticky="w")
		self.ed2 = tk.Entry(self)
		self.ed2.insert(0, config["serverIP"])
		self.ed2.grid(row=2, column=1, sticky="w")

		label3 = tk.Label(self, text="Peer Port:")
		label3.grid(row=3, column=0, sticky="w")
		self.ed3 = tk.Entry(self)
		self.ed3.insert(0, config["peerPort"])
		self.ed3.grid(row=3, column=1, sticky="w")

		self.labelstatus = ttk.Label(self, text="Conection status\n...", font=("Verdana", "11"))
		self.labelstatus.grid(row=5, columnspan=2, pady=10)

		button1 = tk.Button(self, text="OK", highlightbackground='#3E4149', bg='#B0C4DE', relief='raised', fg='black', activebackground='#4682B4',activeforeground='white', command=lambda: self.subscribeUser(controller))
		button1.grid(row=4, columnspan=2, pady=10)

	def subscribeUser(self, controller):
		global objChatConnector
		_username = self.ed1.get()
		_serverIP = self.ed2.get()
		_peerPort = self.ed3.get()
		print("entries: ",_username, _serverIP, _peerPort)
		objChatConnector.setConfig(peerPort=_peerPort, username=_username, serverIP=_serverIP)
		subscribed = objChatConnector.subscribeToServer()
		self.labelstatus.config(text = str(subscribed))
		controller.show_frame(SubscribePage)
		if subscribed != 'Timeout':
			time.sleep(1)
			controller.show_frame(ChatListPage)

class ChatListPage(tk.Frame):
	def __init__(self, parent, controller):
		global objChatConnector
		global objChatManager
		global objUDPPeer

		tk.Frame.__init__(self, parent)

		label = tk.Label(self, text="Escolha um chat:", font=("Verdana", "10"))
		label.pack(pady=12)

		self.objChatManager = objChatManager#ChatManager.ChatManager(objChatConnector)
		self.itemsforlistbox=[(chat.chatName,chat.chatID, chat) for chat in self.objChatManager.chatList]
		objUDPPeer = UDPPeer.UDPPeer(self.objChatManager, objChatConnector)

		self.listaDeChats = tk.Listbox(self)
		def goChat():
			value = str(self.listaDeChats.get(self.listaDeChats.curselection()))   
			label.config(text=value)
			print(value + " selected!")
			for item in self.itemsforlistbox:
				if item[1] == value.split(' / ')[1]:
					objChat=item[2]
			controller.show_frame(ChatPage, objChat=objChat)

		def chatConfig():
			controller.show_frame(ChatConfigPage, objChatManager=self.objChatManager, objChatConnector=objChatConnector)
		#listaDeChats.bind('<<ListboxSelect>>', goChat)
		self.listaDeChats.pack(side = tk.LEFT, fill = tk.BOTH)
		for items in self.itemsforlistbox:
			self.listaDeChats.insert(tk.END,items[0]+' / '+items[1])

		scrollbar = tk.Scrollbar(self)
		scrollbar.pack(side = tk.LEFT, fill = tk.BOTH)

		self.listaDeChats.config(yscrollcommand = scrollbar.set) 
		scrollbar.config(command = self.listaDeChats.yview)
		

		button3 = tk.Button(self, text="New Chat +", width='10', highlightbackground='#3E4149', bg='#FD8403', relief='raised', fg='black', activebackground='#CB6A02',activeforeground='white', command=chatConfig)
		button3.pack(pady=10)

		button4 = tk.Button(self, text="Go chat!", width='10', highlightbackground='#3E4149', bg='#FD8403', relief='raised', fg='black', activebackground='#CB6A02',activeforeground='white', command=goChat)
		button4.pack(pady=10)

	def setChatManager(self, objChatManager=None):
		self.objChatManager = objChatManager
		if objChatManager:
			self.refreshChatList()
			

	def refreshChatList(self):
		print(self.objChatManager.chatList)
		self.listaDeChats.delete(0,tk.END)
		self.itemsforlistbox=[(chat.chatName,chat.chatID, chat) for chat in self.objChatManager.chatList]
		for items in self.itemsforlistbox:
			self.listaDeChats.insert(tk.END,items[0]+' / '+items[1])
		self.objChatManager.saveChatList()

class ChatConfigPage(tk.Frame):
	def __init__(self, parent, controller, chatID=None):
		tk.Frame.__init__(self, parent)
		class Checkbar(tk.Frame):
			def __init__(self, parent=None, picks=[], side=tk.LEFT, anchor=tk.W):
				tk.Frame.__init__(self, parent)
				self.setUsers(picks)

			def state(self):
				#return map((lambda var: var.get()), self.vars)
				selecionados = [pick for var,pick in zip(self.vars, self.picks) if var.get()==1]
				return selecionados

			def setUsers(self, userList):
				self.picks = userList			
				self.vars = []
				for pick in self.picks:
					var = tk.IntVar()
					chk = tk.Checkbutton(self, text=pick, variable=var)
					chk.pack(anchor=tk.W, expand=tk.YES)
					self.vars.append(var)


		#Create Main Frame
		main_frame = tk.Frame(self)
		main_frame.pack(fill=tk.BOTH, expand=1)

		#Create a canvas
		my_canvas = tk.Canvas(main_frame)
		my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

		#Add a scrollbar to the Canvas
		my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
		my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		#Configure another frame inside the canvas
		my_canvas.configure(yscrollcommand=my_scrollbar.set)
		my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

		#Create another frame inside the canvas
		self.checkbar = Checkbar(my_canvas)
		#Isso adiciona um label na nossa pagina, o processo é o mesmo pra adicionar outras coisas
		label = ttk.Label(self.checkbar, text="Chat Config Page", font=("Verdana", "12"))
		label.pack(pady=10)

		self.labelChatName = tk.Label(self.checkbar, text="Chat Name: ")
		self.labelChatName.pack()
		self.ed1 = tk.Entry(self.checkbar)
		self.ed1.pack()

		self.labelSelectUsers = tk.Label(self.checkbar, text="Select users to chat:")
		self.labelSelectUsers.pack()
		
		#add that new fdrame to a new windo
		my_canvas.create_window((0,0), window=self.checkbar, anchor="nw")

		self.checkbar.setUsers(["user_"+str(option) for option in range(10)])

		def createChat():
			print("Chat Name:", self.ed1.get())
			_chatName = self.ed1.get()
			print("Users: ", self.checkbar.state())
			_destUsers = self.checkbar.state()
			if self.objChatConnector.username not in _destUsers:
				_destUsers.append(self.objChatConnector.username)
			if _chatName in [chat.chatName for chat in self.objChatManager.chatList]:
				self.ed1.insert(0, "INVALID CHATNAME!")
			else:
				self.objChatManager.newChat( _chatName, _destUsers)
				for chat in self.objChatManager.chatList:
					if chat.chatName==_chatName:
						objChat=chat
						break
				controller.show_frame(ChatPage, objChat=objChat)


		self.button = tk.Button(self.checkbar, text='Go Chat!', command=createChat).pack()

	def setChatManager(self, objChatManager=None):
		self.objChatManager=objChatManager

	def setChatConnector(self, objChatConnector=None):
		self.objChatConnector=objChatConnector

	def refreshUsers(self):
		for widget in self.checkbar.winfo_children():
			if widget.winfo_class()=="Checkbutton":
				widget.destroy()
		users = self.objChatConnector.getContactDict()
		userList = [user for user in users]
		self.checkbar.setUsers(userList)


class ChatPage(tk.Frame):
	def __init__(self, parent, controller):
		global objChatConnector
		global objUDPPeer

		tk.Frame.__init__(self, parent)
		objUDPPeer.setCurrentChatPage(self)
		objUDPPeer.handleReceive()

		self.configure(width = 470, height = 550, bg = "#17202A")

		self.labelHead = tk.Label(self,bg = "#17202A", fg = "#EAECEE", text = "Chat not initialized" , font=("Verdana", "11"), pady = 5)
          
		self.labelHead.place(relwidth = 1)
		self.line = tk.Label(self, width = 450, bg = "#ABB2B9")
          
		self.line.place(relwidth = 1, rely = 0.07, relheight = 0.012)
          
		self.textCons = tk.Text(self,width = 20,height = 2, bg = "#17202A",fg = "#EAECEE",font=("Verdana", "12"), padx = 5, pady = 5)
          
		self.textCons.place(relheight = 0.745,
                            relwidth = 1, 
                            rely = 0.08)
          
		self.labelBottom = tk.Label(self,
                                 bg = "#ABB2B9",
                                 height = 80)
          
		self.labelBottom.place(relwidth = 1,
                               rely = 0.825)
          
		self.entryMsg = tk.Entry(self.labelBottom,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = ("Verdana", "12"))
          
		# place the given widget
		# into the gui window
		self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
          
		self.entryMsg.focus()

		# create a Send Button
		self.buttonMsg = tk.Button(self.labelBottom,
                                text = "Send",
                                font=("Verdana", "12"), 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))
          
		self.buttonMsg.place(relx = 0.77,
                             rely = 0.008,
                             relheight = 0.06, 
                             relwidth = 0.22)
          
		self.textCons.config(cursor = "arrow")
          
		# create a scroll bar
		scrollbar = tk.Scrollbar(self.textCons)
          
		# place the scroll bar 
		# into the gui window
		scrollbar.place(relheight = 1,
                        relx = 0.974)
          
		scrollbar.config(command = self.textCons.yview)
          
		self.textCons.config(state = tk.DISABLED)


	def setChat(self, objChat=None):
		global objChatConnector
		global objUDPPeer
		if objChat:
			self.objChat = objChat
		objUDPPeer.setCurrentChatPage(self)
		#Isso adiciona um label na nossa pagina, o processo é o mesmo pra adicionar outras coisas
		self.labelHead.configure(text=self.objChat.chatName)
		self.textCons.config(state = tk.NORMAL)
		self.textCons.delete(1.0, tk.END)
		self.textCons.config(state = tk.DISABLED)

		for msg in self.objChat.messageList:
			# insert messages to text box
			self.textCons.config(state = tk.NORMAL)
			self.textCons.insert(tk.END,
									msg["oriusername"]+": "+msg["content"] +"\n\n")
				
			self.textCons.config(state = tk.DISABLED)
			self.textCons.see(tk.END)

	def sendButton(self, msg):
		global objChatConnector
		global objUDPPeer
		self.textCons.config(state = tk.DISABLED)
		self.msg=msg
		self.entryMsg.delete(0, tk.END)
		msg = self.objChat.createMsg('text', msg)
		print("Sending message: "+str(msg))
		objUDPPeer.sendMessage(msg)


app = app()
#Centraliza app na tela
app.eval('tk::PlaceWindow %s center' % app.winfo_pathname(app.winfo_id()))
app.mainloop()
