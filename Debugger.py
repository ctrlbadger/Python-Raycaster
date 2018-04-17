import tkinter
from tkinter.scrolledtext import ScrolledText
import threading
import time

class Application(tkinter.Frame):
    def __init__(self, GlobalQueue, ExecQueue, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.master=master
        self.GlobalQueue = GlobalQueue
        self.ExecQueue = ExecQueue
        self.GetGlobalsThread = threading.Thread(target=self.GetGlobals)
        self.GetGlobalsThread.start()
        

    def create_widgets(self):
        self.terminal = tkinter.Label(self)
        self.terminal.grid(row=0, column=0)
        #self.terminal.bind()
        #self.terminal.bind("<Key>", lambda e: "break")

        self.input = tkinter.Entry(self)
        self.input.bind('<Return>', self.VariableButtonClick)
        self.input.grid(row=1, column=0)
    
    def VariableButtonClick(self, _):
        self.text_box = tkinter.Label(self, text="Hello World")
        self.text_box.grid(row=1)
   
    # def GetGlobals(self):
    #     print("How many times is this run?")
    #     global_list = [[Name, Var] for Name, Var in self.GlobalQueue.get().items() if Name[0:2] != '__']
    #     StrLastGlobals = "\n".join([str(VarName)+": "+str(Var) for VarName, Var in global_list])

        
    #     self.terminal.insert("0.0", StrLastGlobals)

        
    #     while True:
    #         time.sleep(1)
    #         self.terminal.state = tkinter.DISABLED
    #         for name, var in self.GlobalQueue.get().items():
    #             if name[0:2] != '__':
    #                 zipped_global_list = list(map(list, zip(*global_list)))
    #                 if name in zipped_global_list[0]:
    #                     name_index = zipped_global_list[0].index(name)
    #                     if zipped_global_list[1][name_index] != var:
    #                         global_list[name_index][1] = var
    #                 else:
    #                     global_list.append([name, var])

    #         StrLastGlobals = "\n".join([str(VarName)+": "+str(Var) for VarName, Var in global_list])
            
            
    #         # PrevEnd = tkinter.END
    #         # self.terminal.
    #         self.terminal.delete("0.0", tkinter.END)
    #         self.terminal.insert("0.0", StrLastGlobals)
    #         self.terminal.state = tkinter.NORMAL
    #         # self.terminal.see()
            
    def GetGlobals(self):
        print("How many times is this run?")
        global_list = [[Name, Var] for Name, Var in self.GlobalQueue.get().items() if Name[0:2] != '__']
        StrLastGlobals = "\n".join([str(VarName)+": "+str(Var) for VarName, Var in global_list])

        
        self.terminal.set(StrLastGlobals)

        
        while True:
            time.sleep(1)
            
            for name, var in self.GlobalQueue.get().items():
                if name[0:2] != '__':
                    zipped_global_list = list(map(list, zip(*global_list)))
                    if name in zipped_global_list[0]:
                        name_index = zipped_global_list[0].index(name)
                        if zipped_global_list[1][name_index] != var:
                            global_list[name_index][1] = var
                    else:
                        global_list.append([name, var])

            StrLastGlobals = "\n".join([str(VarName)+": "+str(Var) for VarName, Var in global_list])
            
            
            # PrevEnd = tkinter.END
            # self.terminal.
            
            self.terminal.set(StrLastGlobals)
            
            # self.terminal.see()
class ApplicationThread(threading.Thread):
    def __init__(self, GlobalQueue, ExecQueue):
        threading.Thread.__init__(self)
        self.start()
        self.GlobalQueue = GlobalQueue
        self.ExecQueue   = ExecQueue
    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.app = Application(self.GlobalQueue, self.ExecQueue, master=self.root)
        self.app.mainloop()

"""
root = tkinter.Tk()
app = Application(master=root)
app.mainloop()
"""