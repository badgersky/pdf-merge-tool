import os

import customtkinter as ctk
from tkinter import filedialog as fd
from PyPDF2 import PdfMerger


class MergeToolWindow(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()
        self.title('PDFmerge')
        self.geometry('600x200')

        # grid configuration
        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure((0, 1, 2, 3), weight=1)

        # selected files textbox
        self.lbl_selected_files = ctk.CTkLabel(self, text='Selected files:')
        self.lbl_selected_files.grid(row=0, column=0, padx=10, pady=10)

        self.txt_selected_files = ctk.CTkTextbox(self, height=50, state='disabled')
        self.txt_selected_files.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky='nsew')

        # new file name entry
        self.lbl_new_filename = ctk.CTkLabel(self, text='New filename:')
        self.lbl_new_filename.grid(row=1, column=0, padx=10, pady=10)

        self.ent_new_filename = ctk.CTkEntry(self, placeholder_text='New filename')
        self.ent_new_filename.grid(row=1, column=1, columnspan=3, padx=10, pady=10, sticky='nsew')

        # buttons
        self.btn_select_files = ctk.CTkButton(self, text='SELECT FILES', width=100, command=self.select_files)
        self.btn_select_files.grid(row=2, column=0, padx=10, pady=10)

        self.btn_clear_selected_files = ctk.CTkButton(self, text='CLEAR', width=100, command=self.clear_selected_files)
        self.btn_clear_selected_files.grid(row=2, column=1, padx=10, pady=10)

        self.btn_cancel = ctk.CTkButton(self, text='BACK', width=100, command=self.destroy)
        self.btn_cancel.grid(row=2, column=2, padx=10, pady=10)
        
        self.btn_merge_files = ctk.CTkButton(self, text='MERGE', width=100, command=self.merge_files)
        self.btn_merge_files.grid(row=2, column=3, padx=10, pady=10)

        # list of files to merge
        self.files = []

        # insert filenames from self.files to textbox
        self.insert_selected_files()

        # merged files directory
        self.create_merged_dir()
        self.merged_path = 'merged'

    def select_files(self):
        files = fd.askopenfiles()
        for file in files:
            self.files.append(file.name)

        self.insert_selected_files()

    def insert_selected_files(self):
        self.txt_selected_files.configure(state='normal')
        self.txt_selected_files.delete('0.0', 'end')
        if not self.files:
            self.txt_selected_files.insert('end', 'No selected files')
        else:
            for file in self.files:
                filename = file.split('/')[-1]
                self.txt_selected_files.insert('end', filename + '\n')

        self.txt_selected_files.configure(state='disabled')

    def clear_selected_files(self):
        self.files = []
        self.insert_selected_files()

    def merge_files(self):
        if not self.files:
            return
        else:
            filename = self.get_filename()

            merger = PdfMerger()
            for file in self.files[::-1]:
                merger.append(file)

            merger.write(os.path.join(self.merged_path, filename))    
            merger.close()

    def get_filename(self):
        filename = self.ent_new_filename.get()
        if not filename:
            files = self.txt_selected_files.get('0.0', 'end').split()
            return files[-1]
        else:
            if filename.endswith('.pdf'):
                return filename
            else:
                return filename + '.pdf'
            
    def create_merged_dir(self):
        curr_dir = os.listdir()
        if 'merged' not in curr_dir:
            os.mkdir('merged')


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
