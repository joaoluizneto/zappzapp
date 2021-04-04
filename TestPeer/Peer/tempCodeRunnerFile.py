		class Checkbar(tk.Frame):
			def __init__(self, parent=None, picks=[], side=tk.LEFT, anchor=tk.W):
				tk.Frame.__init__(self, parent)
				self.setUsers(picks)

			def state(self):
				return map((lambda var: var.get()), self.vars)
			def setUsers(self, userList):
				picks = userList			
				self.vars = []
				for pick in picks:
					var = tk.IntVar()
					chk = tk.Checkbutton(self, text=pick, variable=var)
					chk.pack(anchor=tk.W, expand=tk.YES)
					self.vars.append(var)
