
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import filedialog
import threading
import os

from lib.editor import ImgEditor
from lib.viewer import ImgViewer


class App(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title('画像加工')
        self.img = None
        self.num = 0
        self.op = tk.StringVar('')
        self.path = tk.StringVar('')
        self.reverse = tk.BooleanVar()
        self.create_mainframe()
        self.create_selectdirectory()
        self.create_selectbox()
        self.create_textbox()
        self.imcanvas = tk.Canvas(bg='white')

    def create_mainframe(self):
        self.mainframe = ttk.Frame(root, height=1, width=30)
        self.button = ttk.Button(self.mainframe, text='Start',
                                 command=self.main)
        self.button.grid(column=0, row=0)
        ttk.Button(self.mainframe, text='プレビュー',
                   command=lambda: self.put_image(0)).grid(column=1, row=0)
        ttk.Button(self.mainframe, text='戻る',
                   command=lambda: self.put_image(self.num-1)
                   ).grid(column=2, row=0)
        ttk.Button(self.mainframe, text='次へ',
                   command=lambda: self.put_image(self.num+1)
                   ).grid(column=3, row=0)
        self.mainframe.grid(column=0, row=0)

    def create_selectdirectory(self):
        self.select_directory = ttk.Frame(root)
        ttk.Label(self.select_directory, text='フォルダー→').grid(column=0, row=0)
        ttk.Entry(self.select_directory, textvariable=self.path,
                  width=40).grid(column=1, row=0)
        ttk.Button(self.select_directory, text='参照',
                   command=self.ask).grid(column=2, row=0)
        self.select_directory.grid(column=0, row=1)

    def create_selectbox(self):
        self.selectbox = ttk.Frame(root, height=1, width=40)
        ttk.Label(self.selectbox, text='処理を選んでください→').grid(column=0, row=0)
        self.combo = ttk.Combobox(self.selectbox, state='readonly',
                                  textvariable=self.op)
        self.combo['values'] = ('trim', 'rotate', 'crop_half', 'resize_half')
        self.combo.current(0)
        self.combo.grid(column=1, row=0)
        tk.Checkbutton(self.selectbox, variable=self.reverse,
                       text='ファイル名を逆順にする').grid(column=2, row=0)
        self.selectbox.grid(column=0, row=2)

    def create_textbox(self):
        self.textframe = tk.Frame(root, height=10, width=40)
        self.result = tk.Text(self.textframe, font=('MeiryoUI', 9),
                              height=5, width=30)
        self.result.insert('1.0', 'ここに結果が表示されます')
        self.result.configure(state='disabled')
        self.scrollbar = ttk.Scrollbar(self.textframe, orient=tk.VERTICAL,
                                       command=self.result.yview)
        self.result['yscrollcommand'] = self.scrollbar.set
        self.result.grid(column=0, row=0)
        self.scrollbar.grid(column=1, row=0)
        self.textframe.grid(column=3, row=0, rowspan=3)

    def ask(self):
        idir = os.path.abspath(os.path.dirname(__file__))
        self.path.set(filedialog.askdirectory(initialdir=idir))

    def add_text(self, text):
        self.result.configure(state='normal')
        self.result.insert('end', '\n' + text)
        self.result.configure(state='disabled')

    def new_text(self, text):
        self.result.configure(state='normal')
        self.result.delete('1.0', 'end')
        self.result.insert('1.0', text)
        self.result.configure(state='disabled')

    def put_image(self, i):
        path = self.path.get()
        op = self.op.get()
        self.num = i
        self.imcanvas.delete('all')
        self.img, name = ImgViewer(path, op).create(i)
        if self.img is not None:
            self.imcanvas.configure(width=self.img.width(),
                                    height=self.img.height())
            self.imcanvas.create_image((self.img.width()//2),
                                       (self.img.height()//2), image=self.img)
            self.imcanvas.grid(column=0, row=3, rowspan=4, columnspan=4)
            self.new_text(name)
        else:
            self.imcanvas.grid_forget()
            self.new_text(name)

    def main(self):
        self.button.configure(text='処理中', state='disabled')
        th = threading.Thread(target=self.func)
        th.start()

    def func(self):
        path = self.path.get()
        if not os.path.exists(path + r'/tmp/'):
            os.mkdir(path + r'/tmp/')
        reverse = self.reverse.get()
        op = self.op.get()
        # errors, count = ImgEditor(op, path, reverse).main()
        # self.new_text(f'{count}件成功\nエラー:\n{errors}'
        #               if errors else f'{count}件成功\nエラーなし')
        for x in ImgEditor(op, path, reverse).main_yield():
            self.add_text(x)
        self.button.configure(text='Start', state='normal')


if __name__ == '__main__':
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()
