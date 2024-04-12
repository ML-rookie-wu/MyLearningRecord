

def my_test():
    print('my_test')
    print("hello world")

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def focus_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def focus_out(self, *args):
        if not self.get():
            self.put_placeholder()
            self['fg'] = self.placeholder_color

class ProgramUI:
    def __init__(self, root):
        self.root = root
        self.root.title("程序执行界面")

        self.create_widgets()

    def create_widgets(self):
        # 创建左侧 Frame
        self.left_frame = ttk.Frame(self.root)
        self.left_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # 创建标签和输入框
        self.labels = ["索引名称:", "Excel路径:", "Excel表格名称:", "URL:"]
        self.entries = []

        for i, label_text in enumerate(self.labels):
            label = tk.Label(self.left_frame, text=label_text)
            label.grid(row=i, column=0, sticky=tk.W)

            entry = EntryWithPlaceholder(self.left_frame, placeholder="请输入" + label_text)
            entry.grid(row=i, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

            self.entries.append(entry)

        # 创建选择文件按钮
        button_select_file = tk.Button(self.left_frame, text="选择文件", command=self.select_excel_file)
        button_select_file.grid(row=1, column=2, padx=5, pady=5)

        # 创建按钮 Frame
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))

        # 创建执行按钮
        button_execute = tk.Button(self.button_frame, text="执行", command=self.execute_program)
        button_execute.pack(side=tk.LEFT, padx=5, pady=(0, 10))

        # 创建清除输入按钮
        button_clear_input = tk.Button(self.button_frame, text="清除输入", command=self.clear_input)
        button_clear_input.pack(side=tk.LEFT, padx=5, pady=(0, 10))

        # 设置左侧 Frame 的列权重
        self.left_frame.grid_columnconfigure(1, weight=1)

        # 设置左侧 Frame 的行权重
        for i in range(len(self.labels)):
            self.left_frame.grid_rowconfigure(i, weight=1)

    def execute_program(self):
        # 这里写执行程序的逻辑
        print("执行程序")

    def select_excel_file(self):
        file_path = filedialog.askopenfilename()
        self.entries[1].delete(0, tk.END)
        self.entries[1].insert(0, file_path)

    def clear_input(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

# 创建主窗口
root = tk.Tk()
app = ProgramUI(root)
root.mainloop()