import customtkinter as ctk
from tkinter import filedialog as fd


class MergeToolWindow(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()
        self.title('PDFmerge')
        self.geometry('600x120')

        # grid configuration
        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1, 2), weight=1)

        # selected files entry
        self.lbl_selected_files = ctk.CTkLabel(self, text='Selected files:')
        self.lbl_selected_files.grid(row=0, column=0, padx=10, pady=10)

        self.txt_selected_files = ctk.CTkTextbox(self, height=50, state='disabled')
        self.txt_selected_files.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')

        # buttons
        self.btn_select_files = ctk.CTkButton(self, text='SELECT FILES', width=80, command=self.select_files)
        self.btn_select_files.grid(row=1, column=0, padx=10, pady=10)

        self.btn_clear_selected_files = ctk.CTkButton(self, text='CLEAR', width=80)
        self.btn_clear_selected_files.grid(row=1, column=1, padx=10, pady=10)
        
        self.btn_merge_files = ctk.CTkButton(self, text='MERGE', width=80)
        self.btn_merge_files.grid(row=1, column=2, padx=10, pady=10)

        # list of files to merge
        self.files = []
        self.insert_selected_files()

    def select_files(self):
        files = fd.askopenfiles()
        for file in files:
            self.files.append(file.name)

        self.insert_selected_files()

    def insert_selected_files(self):
        self.txt_selected_files.configure(state='normal')
        if not self.files:
            self.txt_selected_files.insert('end', 'No selected files')
        else:
            self.txt_selected_files.delete('0.0', 'end')
            for file in self.files:
                filename = file.split('/')[-1]
                self.txt_selected_files.insert('end', filename + '\n')

        self.txt_selected_files.configure(state='disabled')


class SplitToolWindow(ctk.CTkToplevel):
        
    def __init__(self):
        super().__init__()
        self.title('PDFsplit')
        self.geometry('300x200')


class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.geometry('300x150')
        self.title('PDFmerge-split')

        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure(0, weight=1)

        # buttons on main window
        self.btn_merge = ctk.CTkButton(self, width=150, height=30, text='MERGE PDF', command=self.open_merge_tool)
        self.btn_merge.grid(row=0, column=0, padx=10, pady=10)

        self.btn_split = ctk.CTkButton(self, width=150, height=30, text='SPLIT PDF', command=self.open_split_tool)
        self.btn_split.grid(row=1, column=0, padx=10, pady=10)

        self.btn_quit = ctk.CTkButton(self, width=150, height=30, text='QUIT', command=self.quit)
        self.btn_quit.grid(row=2, column=0, padx=10, pady=10)

        # top level windows
        self.merge_tool_window = None
        self.split_tool_window = None

    def open_merge_tool(self):
        if self.merge_tool_window is None or not self.merge_tool_window.winfo_exists():
            self.merge_tool_window = MergeToolWindow()
        else:
            self.merge_tool_window.focus()

    def open_split_tool(self):
        if self.split_tool_window is None or not self.split_tool_window.winfo_exists():
            self.split_tool_window = SplitToolWindow()
        else:
            self.split_tool_window.focus()


if __name__ == '__main__':
    pass
