import os
import shutil
import tkinter as tk
from tkinter import messagebox, ttk
import gettext
import time
import threading


gettext.bindtextdomain('cleaner', 'locale')
gettext.textdomain('cleaner')
_ = gettext.gettext


translations = {
    'English': {
        'title': 'PC Cleaner Pro',
        'select': 'Select items to clean:',
        'temp': 'Temporary Files',
        'cache': 'Cache Files',
        'downloads': 'Old Downloads (>30 days)',
        'recycle': 'Empty Recycle Bin',
        'clean': 'Clean',
        'scan': 'Scan',
        'cleaned': 'Cleaned {} items.',
        'done': 'Cleaning completed.',
        'lang': 'Language:',
        'scanning': 'Scanning...',
        'cleaning': 'Cleaning...',
        'space': 'Space to free: {} MB',
        'file': 'File',
        'exit': 'Exit',
        'help': 'Help',
        'about': 'About',
        'about_msg': 'PC Cleaner Pro v1.0\nA professional PC cleaning tool.'
    },
    'Français': {
        'title': 'Nettoyant PC Pro',
        'select': 'Sélectionnez les éléments à nettoyer :',
        'temp': 'Fichiers temporaires',
        'cache': 'Fichiers cache',
        'downloads': 'Téléchargements anciens (>30 jours)',
        'recycle': 'Vider la corbeille',
        'clean': 'Nettoyer',
        'scan': 'Scanner',
        'cleaned': 'Nettoyé {} éléments.',
        'done': 'Nettoyage terminé.',
        'lang': 'Langue :',
        'scanning': 'Scan en cours...',
        'cleaning': 'Nettoyage en cours...',
        'space': 'Espace à libérer : {} Mo',
        'file': 'Fichier',
        'exit': 'Quitter',
        'help': 'Aide',
        'about': 'À propos',
        'about_msg': 'Nettoyant PC Pro v1.0\nUn outil professionnel de nettoyage PC.'
    }
}

class PCCleaner:
    def __init__(self, root):
        self.root = root
        self.current_lang = 'English'

       
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 10, 'bold'), padding=6)
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TCheckbutton', font=('Arial', 10))
        style.configure('TCombobox', font=('Arial', 10))
        style.configure('TProgressbar', thickness=20)

        self.root.geometry("600x500")
        self.root.minsize(500, 400)
        self.root.title(translations[self.current_lang]['title'])

        
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=translations[self.current_lang]['file'], menu=file_menu)
        file_menu.add_command(label=translations[self.current_lang]['exit'], command=self.root.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=translations[self.current_lang]['help'], menu=help_menu)
        help_menu.add_command(label=translations[self.current_lang]['about'], command=self.show_about)

       
        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill='both', expand=True)

        
        lang_frame = ttk.LabelFrame(main_frame, text=translations[self.current_lang]['lang'], padding=10)
        lang_frame.pack(fill='x', pady=5)
        self.lang_combo = ttk.Combobox(lang_frame, values=list(translations.keys()), state='readonly', font=('Arial', 10))
        self.lang_combo.set(self.current_lang)
        self.lang_combo.pack(side='left')
        self.lang_combo.bind('<<ComboboxSelected>>', self.change_lang)

       
        options_frame = ttk.LabelFrame(main_frame, text=translations[self.current_lang]['select'], padding=10)
        options_frame.pack(fill='x', pady=5)

        self.temp_var = tk.BooleanVar()
        self.cache_var = tk.BooleanVar()
        self.downloads_var = tk.BooleanVar()
        self.recycle_var = tk.BooleanVar()

        self.temp_check = ttk.Checkbutton(options_frame, text=translations[self.current_lang]['temp'], variable=self.temp_var)
        self.temp_check.pack(anchor='w', pady=2)

        self.cache_check = ttk.Checkbutton(options_frame, text=translations[self.current_lang]['cache'], variable=self.cache_var)
        self.cache_check.pack(anchor='w', pady=2)

        self.downloads_check = ttk.Checkbutton(options_frame, text=translations[self.current_lang]['downloads'], variable=self.downloads_var)
        self.downloads_check.pack(anchor='w', pady=2)

        self.recycle_check = ttk.Checkbutton(options_frame, text=translations[self.current_lang]['recycle'], variable=self.recycle_var)
        self.recycle_check.pack(anchor='w', pady=2)

        
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=10)

        self.scan_button = ttk.Button(buttons_frame, text=translations[self.current_lang]['scan'], command=self.scan)
        self.scan_button.pack(side='left', padx=10)

        self.clean_button = ttk.Button(buttons_frame, text=translations[self.current_lang]['clean'], command=self.start_clean, state='disabled')
        self.clean_button.pack(side='left', padx=10)

        
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill='x', pady=5)

        self.progress = ttk.Progressbar(progress_frame, orient='horizontal', mode='determinate')
        self.progress.pack(fill='x')

        
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill='x', pady=5)

        self.status_label = ttk.Label(status_frame, text="", font=('Arial', 9))
        self.status_label.pack(side='left')

        self.space_label = ttk.Label(status_frame, text="", font=('Arial', 9))
        self.space_label.pack(side='right')

    def change_lang(self, event):
        self.current_lang = self.lang_combo.get()
        self.update_texts()

    def update_texts(self):
        self.root.title(translations[self.current_lang]['title'])

        self.root.config(menu=self.create_menu())

        for child in self.root.winfo_children():
            if isinstance(child, ttk.LabelFrame):
                if 'lang' in child.cget('text').lower() or 'language' in child.cget('text').lower():
                    child.config(text=translations[self.current_lang]['lang'])
                elif 'select' in child.cget('text').lower():
                    child.config(text=translations[self.current_lang]['select'])
        
        self.temp_check.config(text=translations[self.current_lang]['temp'])
        self.cache_check.config(text=translations[self.current_lang]['cache'])
        self.downloads_check.config(text=translations[self.current_lang]['downloads'])
        self.recycle_check.config(text=translations[self.current_lang]['recycle'])
        self.scan_button.config(text=translations[self.current_lang]['scan'])
        self.clean_button.config(text=translations[self.current_lang]['clean'])

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=translations[self.current_lang]['file'], menu=file_menu)
        file_menu.add_command(label=translations[self.current_lang]['exit'], command=self.root.quit)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=translations[self.current_lang]['help'], menu=help_menu)
        help_menu.add_command(label=translations[self.current_lang]['about'], command=self.show_about)
        return menubar

    def show_about(self):
        messagebox.showinfo(translations[self.current_lang]['about'], translations[self.current_lang]['about_msg'])

    def scan(self):
        self.status_label.config(text=translations[self.current_lang]['scanning'])
        self.progress['value'] = 0
        self.root.update()
        total_space = 0
        if self.temp_var.get():
            temp_dir = os.path.join(os.environ.get('TEMP', '/tmp'))
            for file in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file)
                if os.path.isfile(file_path):
                    total_space += os.path.getsize(file_path)
        if self.cache_var.get():
            
            pass
        if self.downloads_var.get():
            downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            if os.path.exists(downloads_dir):
                for file in os.listdir(downloads_dir):
                    file_path = os.path.join(downloads_dir, file)
                    if os.path.isfile(file_path) and time.time() - os.path.getmtime(file_path) > 30*24*3600:
                        total_space += os.path.getsize(file_path)
        if self.recycle_var.get():

            pass
        total_mb = total_space / (1024*1024)
        self.space_label.config(text=translations[self.current_lang]['space'].format(round(total_mb, 2)))
        self.clean_button.config(state='normal')
        self.status_label.config(text="")

    def start_clean(self):
        threading.Thread(target=self.clean).start()

    def clean(self):
        self.status_label.config(text=translations[self.current_lang]['cleaning'])
        self.progress['value'] = 0
        cleaned = 0
        steps = sum([self.temp_var.get(), self.cache_var.get(), self.downloads_var.get(), self.recycle_var.get()])
        step = 100 / steps if steps > 0 else 100
        current = 0

        if self.temp_var.get():
            temp_dir = os.path.join(os.environ.get('TEMP', '/tmp'))
            cleaned_dir = os.path.join(temp_dir, 'Cleaned')
            os.makedirs(cleaned_dir, exist_ok=True)
            for file in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file)
                try:
                    if os.path.isfile(file_path) and not file.startswith('Cleaned'):
                        shutil.move(file_path, os.path.join(cleaned_dir, file))
                        cleaned += 1
                except:
                    pass
            current += step
            self.progress['value'] = current
            self.root.update()

        if self.cache_var.get():
            
            current += step
            self.progress['value'] = current
            self.root.update()

        if self.downloads_var.get():
            downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
            cleaned_dir = os.path.join(downloads_dir, 'Cleaned')
            os.makedirs(cleaned_dir, exist_ok=True)
            if os.path.exists(downloads_dir):
                for file in os.listdir(downloads_dir):
                    file_path = os.path.join(downloads_dir, file)
                    try:
                        if os.path.isfile(file_path) and time.time() - os.path.getmtime(file_path) > 30*24*3600:
                            shutil.move(file_path, os.path.join(cleaned_dir, file))
                            cleaned += 1
                    except:
                        pass
            current += step
            self.progress['value'] = current
            self.root.update()

        if self.recycle_var.get():
            
            current += step
            self.progress['value'] = current
            self.root.update()

        self.status_label.config(text=translations[self.current_lang]['cleaned'].format(cleaned))
        messagebox.showinfo(translations[self.current_lang]['done'], translations[self.current_lang]['cleaned'].format(cleaned))
        self.clean_button.config(state='disabled')
        self.space_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = PCCleaner(root)
    root.mainloop()
