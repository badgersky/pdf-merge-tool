import os

import customtkinter as ctk
from tkinter import filedialog as fd
from tkinter import messagebox
from PyPDF2 import PdfMerger


class MyTopLevel(ctk.CTkToplevel):

    def __init__(self):
        super().__init__()

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

        # list of selected to merge
        self.files = []

        # insert filenames from self.files to textbox
        self.insert_selected_files()

    def insert_selected_files(self):
        # inserts files into selected files textbox
        self.txt_selected_files.configure(state='normal')
        self.txt_selected_files.delete('0.0', 'end')
        if not self.files:
            self.txt_selected_files.insert('end', 'No selected files')
        else:
            for file in self.files:
                filename = file.split('/')[-1]
                self.txt_selected_files.insert('end', filename + '\n')

        self.txt_selected_files.configure(state='disabled')

    def get_filename(self, directory):
        # gets filename from filename entry, if empty filename is taken from first selected file to merge from self.files
        filename = self.ent_new_filename.get()
        if not filename:
            files = self.txt_selected_files.get('0.0', 'end').split()
            return files[-1]
        else:
            if not filename.endswith('.pdf'):
                filename += '.pdf'
            if filename in os.listdir(directory):
                messagebox.showerror('Filename error', f'Filename {filename} already in merged folder.')
                return
            return filename
        
    def clear_selected_files(self):
        self.files = []
        self.insert_selected_files()


class MergeToolWindow(MyTopLevel):

    def __init__(self):
        super().__init__()
        self.title('PDFmerge')
        self.geometry('600x200')

        # grid configuration
        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure((0, 1, 2, 3), weight=1)

        # buttons
        self.btn_select_files = ctk.CTkButton(self, text='SELECT FILES', width=100, command=self.select_files)
        self.btn_select_files.grid(row=2, column=0, padx=10, pady=10)

        self.btn_clear_selected_files = ctk.CTkButton(self, text='CLEAR', width=100, command=self.clear_selected_files)
        self.btn_clear_selected_files.grid(row=2, column=1, padx=10, pady=10)

        self.btn_cancel = ctk.CTkButton(self, text='BACK', width=100, command=self.destroy)
        self.btn_cancel.grid(row=2, column=2, padx=10, pady=10)
        
        self.btn_merge_files = ctk.CTkButton(self, text='MERGE', width=100, command=self.merge_files)
        self.btn_merge_files.grid(row=2, column=3, padx=10, pady=10)

        # merged files directory
        self.create_merged_dir()
        self.merged_path = 'merged'

    def select_files(self):
        # adds files to list of selected self.files
        files = fd.askopenfiles(filetypes=[('pdf files', '*.pdf')])
        for file in files:
            if file.name not in self.files:
                self.files.append(file.name)

        self.insert_selected_files()

    def merge_files(self):
        # merges files into one
        if not self.files:
            return
        else:
            filename = self.get_filename(directory='merged')
            if filename:
                merger = PdfMerger()
                for file in self.files[::-1]:
                    merger.append(file)

                merger.write(os.path.join(self.merged_path, filename))    
                merger.close()

                self.ent_new_filename.delete('0', 'end')
                messagebox.showinfo('Merge Succes', 'Files were merged successfuly.')
            
    def create_merged_dir(self):
        # creates directory "merged" if does not exist
        curr_dir = os.listdir()
        if 'merged' not in curr_dir:
            os.mkdir('merged')


class SplitToolWindow(MyTopLevel):
        
    def __init__(self):
        super().__init__()
        self.title('PDFsplit')
        self.geometry('600x200')

        # grid configuration
        self.rowconfigure((0, 1, 2, 3), weight=1)
        self.columnconfigure((0, 1, 2, 3), weight=1)

        # buttons
        self.btn_select_files = ctk.CTkButton(self, text='SELECT FILE', width=100, command=self.select_file)
        self.btn_select_files.grid(row=3, column=0, padx=10, pady=10)

        self.btn_clear_selected_files = ctk.CTkButton(self, text='CLEAR', width=100, command=self.clear_selected_files)
        self.btn_clear_selected_files.grid(row=3, column=1, padx=10, pady=10)

        self.btn_cancel = ctk.CTkButton(self, text='BACK', width=100, command=self.destroy)
        self.btn_cancel.grid(row=3, column=2, padx=10, pady=10)
        
        self.btn_merge_files = ctk.CTkButton(self, text='SPLIT', width=100, command=self.split_file)
        self.btn_merge_files.grid(row=3, column=3, padx=10, pady=10)

        # creates split direcotry if it does not exist
        self.create_split_dir()

    def select_file(self):
        # adds file to list of selected self.files
        file = fd.askopenfile(filetypes=[('pdf files', '*.pdf')])
        if file:
            self.clear_selected_files()
            self.files.append(file.name)
            self.insert_selected_files()

    def create_split_dir(self):
        # creates directory "merged" if does not exist
        curr_dir = os.listdir()
        if 'split' not in curr_dir:
            os.mkdir('split')


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
