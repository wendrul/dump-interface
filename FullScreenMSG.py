import tkinter as tk
from tkinter import font



class FullScreenMSG:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.config(cursor="none")
        self.label = tk.Label(self.root, width=20, height=9, font=("Comic", 30), wraplength=450, justify="center", fg="white")
        self.label.pack()
        self.label.configure(bg="pink")
        self.root.configure(bg="pink")
    def PrintMsg(self, msg):
        msg = msg.replace('\\n', '\n')
        self.label.config(text=msg)
    def ChangeBackgroundColor(self, bg_color="pink"):
        self.label.configure(bg=bg_color)
        self.root.configure(bg=bg_color)



# root=tk.Tk()
# root.attributes('-fullscreen', True, )
# root.config(cursor="none")
# label = tk.Label(root, width=20, height=9, font=("Comic", 30), wraplength=450, justify="center", fg="white")
# label.pack()
# label.configure(bg="pink")
# root.configure(bg="pink")
# #print(font.families())
# while (True):
#     try:
#         s = input("> ")
#         if (s == "exit"):
#             break
#         if (s == "color=green"):
#             label.configure(bg="green")
#             root.configure(bg="green")
#         elif (s == "color=red"):
#             label.configure(bg="red")
#             root.configure(bg="red")
#         else:
#             s = s.replace('\\n', '\n')
#             label.config(text=s)
#     except EOFError:
#         print("exit")
#         break
#     time.sleep(0.5)
    