import tkinter as tk
from tkinter import ttk
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

root = tk.Tk()
root.title('Blabla')
root.geometry("500x400")

#Create Main Frame
main_frame = tk.Frame(root)
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
checkbar = Checkbar(my_canvas)

#add that new fdrame to a new windo
my_canvas.create_window((0,0), window=checkbar, anchor="nw")

checkbar.setUsers(["option_"+str(option) for option in range(100)])

root.mainloop()