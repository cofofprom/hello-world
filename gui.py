from tkinter import *
from tkinter import filedialog
import subprocess
import threading
import io
import time

class MainFrame(Frame):
    """Обеспечивает создание главного экрана"""
    def __init__(self, master):
        super().__init__(master)
        self.grid(column = 0, row = 0, sticky = 'nsew')
        self.__loadWidgets()

    def __loadMenu(self):
        menubar = Menu(self.master)
        self.master['menu'] = menubar
        script = Menu(menubar)
        menubar.add_cascade(menu = script, label = 'File')
        script.add_command(label = 'Load', command = self.__loadScript)
        script.add_command(label = 'Exit', command = self.master.destroy)

    def __message(self, text):
        self.status['text'] = text
        self.status.after(2000, lambda: self.status.config(text = ''))
        
    def __loadWidgets(self):
        self.__loadMenu()
        self.text = Text(self)
        self.output = Text(self, bg = 'black', fg = 'green')
        self.save = Button(self, text = 'Save', command = self.__saveScript)
        self.run = Button(self, text = 'Run', command = self.__executeScript)
        self.stop = Button(self, text = 'Stop', command = self.__stopScript)
        self.clear = Button(self, text = 'Clear console', command = lambda: self.output.delete('0.0', END))
        self.status = Label(self)
        self.text.grid(column = 0, row = 0, columnspan = 2, rowspan = 4, sticky = 'nsew')
        self.output.grid(column = 3, row = 0, columnspan = 2, rowspan = 4, sticky = 'nsew')
        self.save.grid(column = 2, row = 0, sticky = 'ew')
        self.run.grid(column = 2, row = 1, sticky = 'ew')
        self.stop.grid(column = 2, row = 2, sticky = 'ew')
        self.clear.grid(column = 2, row = 3, sticky = 'ew')
        self.status.grid(column = 3, row = 4, columnspan = 2, sticky = 'ew')
    
    def __stopScript(self):
        self.script.kill()
        self.__message('Процесс убит')
    
    def __saveScript(self):
        try:
            with open(self.filename, 'wb') as f:
                f.write(self.text.get('0.0', END).encode('utf-8'))
            self.__message('Сохранено')
        except AttributeError:
            self.__message('Необходимо выбрать файл')

    def __executeScript(self):
        self.output.delete('0.0', END)
        starttime = time.time()
        self.script = subprocess.Popen('python ' + self.filename, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines = True)
        for x in self.script.stdout:
            self.output.insert(END, x)
            root.update()
        endtime = time.time()
        self.__message('Выполнение завершено. Затрачено {}'.format(endtime - starttime))
    
    def __loadScript(self):
        self.filename = filedialog.askopenfilename()
        with open(self.filename, 'rb') as f:
            self.text.insert('0.0', f.read().decode('utf-8'))

root = Tk()
root.option_add('*tearOff', FALSE)
main = MainFrame(root)
root.rowconfigure(0, weight = 1)
root.columnconfigure(0, weight = 1)
root.mainloop()
