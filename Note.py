import os
from tkinter import *
from tkinter.messagebox import askyesno

info = 'NoneOpenNever'

def center_window(window, q):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = screen_width // q
    window_height = screen_height // q
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry('{}x{}+{}+{}'.format(window_width, window_height, x, y))
    return window_width, window_height, x, y

def colorbgfg():
    file = open('setting.txt', 'r')
    a = file.readline()
    b = file.readline()
    c = file.readline()
    file.close()
    return a[8:-1], b[8:-1], c[8:]

def Savefile(a):
    file = open(a, 'w', encoding='utf-8')
    file.write(text.get("1.0", "end-1c"))
    file.close()

def Loadfile(a):
    global info
    if info != 'NoneOpenNever':
        Savefile(info)
    info = a
    file = open(a, 'r', encoding='utf-8')
    text.delete("1.0", "end")
    text.insert("1.0", file.read())
    file.close()

def delete_all():
    a = askyesno('Повідомлення', 'Ви впевнені, що хочете все видалити? ')
    if a == 1:
        text.delete("1.0", "end")
    else:
        pass

def delete_allx():
    text.delete("1.0", "end")

root = Tk()
root.title("Нотатки")

x, y, padx, pady = center_window(root, 2)

button_width = x // 10
button_height = y // 10
text_width = x - 3*button_width
text_height = y - button_height

text = Text(root, wrap=WORD, font=("Arial", 12), bg="white", fg="black")
text.place(x=3*button_width, y=button_height, width=text_width, height=text_height)

def get_current_folder():
    return os.path.dirname(os.path.abspath(__file__))

def list_files():
    current_folder = get_current_folder()
    files_list = []
    
    for root_dir, dirs, files in os.walk(current_folder):
        for dir_name in dirs:
            files_list.append(f"folder:{dir_name}")
        for file in files:
            if file.endswith('.txt'):
                files_list.append(file)
    
    print("Всі знайдені папки та файли: ", files_list)
    return files_list

def print_all_notes():
    my_list = list_files()
    for system_file in ['test.py', 'Note.py', 'setting.txt']:
        if system_file in my_list:
            my_list.remove(system_file)
    print("Файли нотаток для відображення: ", my_list)
    return my_list


def tabs(listx):

    def colorbg_choose(a, b, c):
        file = open('setting.txt', 'w')
        file.writelines('ColorBg:{}\n'.format(a))
        file.writelines('ColorFg:{}\n'.format(b))
        file.writelines('ColorFg:{}'.format(c))
        file.close()
        text.config(bg=a, fg=b)

        aaa = print_all_notes()
        tabs(aaa)

    bg, fg, colortabs = colorbgfg()

    for widget in root.winfo_children():
        if isinstance(widget, Button):
            widget.destroy()
    i = 1
    x = button_width
    y = button_height
    for item in listx:
        if item.startswith("folder:"):
            folder_name = item[7:]
            btnx = Button(root, fg='Black', bg='#f0c674', text=folder_name, command=lambda folder=folder_name: open_folder(folder))
        else:
            btnx = Button(root, fg='Black', bg=colortabs, text=item, command=lambda file=item: Loadfile(file))
        btnx.place(x=0, y=i * button_height, width=3*x, height=y)
        i += 1

    root.configure(bg=bg)
    btn_save = Button(root, bg='#e38010', fg='Black', text='Зберегти', command=lambda: Savefile(info))
    btn_save.place(x=5*button_width, y=0, width=button_width, height=button_height)
    btn_delete = Button(root, bg='#e38010', fg='Black', text='Видалити усе', command=delete_all)
    btn_delete.place(x=4*button_width, y=0, width=button_width, height=button_height)
    if bg == 'White':
        btn_theme = Button(root, bg='#e38010', fg='Black', text='Чорна тема', command=lambda: colorbg_choose('Black', 'White', '#090bab'))
        btn_theme.place(x=3*button_width, y=0, width=button_width, height=button_height)
    elif bg == 'Black':
        btn_theme = Button(root, bg='#e38010', fg='Black', text='Біла тема', command=lambda: colorbg_choose('White', 'Black', 'White'))
        btn_theme.place(x=3*button_width, y=0, width=button_width, height=button_height)
    btn_create = Button(root, bg='#e38010', fg='Black', text='Створити', command=lambda: create_file())
    btn_create.place(x=6*button_width, y=0, width=button_width, height=button_height)
    btn_deletex = Button(root, bg='#e38010', fg='Black', text='Видалити', command=lambda: delete_file())
    btn_deletex.place(x=7*button_width, y=0, width=button_width, height=button_height)

def open_folder(folder_name):
    print(f"Открытие папки: {folder_name}")
    pass

def delete_file():
    def entry_get_delete(): 
        filename = entry_delete.get()
        filename = filename + '.txt'
        try:
            os.remove(filename)
            entry_delete.delete(0,END)
            entry_delete.insert(END, 'Файл успішно видалено!')

        except FileNotFoundError:
            entry_delete.delete(0,END)
            entry_delete.insert(END, 'Файл не знайдено!')            

        aaa = print_all_notes()
        tabs(aaa)

    window = Tk()
    center_window(window, 4)
    x, y, a, b = center_window(window, 4)
    xbtn = x / 10
    ybtn = y / 10
    entry_delete = Entry(window, font=32)
    entry_delete.place(x=xbtn, y=3*ybtn, width=8*xbtn, height=ybtn)
    labal_delete = Label(window, text='Видалити файл')
    labal_delete.place(x=xbtn, y=ybtn, width=8*xbtn, height=ybtn)
    btn_delete = Button(window, text='Видалити', command=entry_get_delete)
    btn_delete.place(x=xbtn, y=4*ybtn, width=2*xbtn, height=ybtn)

    window.mainloop()
    tabs()

def create_file():

    def entry_get_create(): 
        filename = entry_create.get()
        if filename:
            filename = filename + '.txt'
            if os.path.isfile(filename):
                Loadfile(filename)
            else:
                open(filename, 'a').close()
                Loadfile(filename)
        
        window1.destroy()
        aaa = print_all_notes()
        tabs(aaa)

    window1 = Tk()
    center_window(window1, 4)
    x, y, a, b = center_window(window1, 4)
    xbtn = x / 10
    ybtn = y / 10
    entry_create = Entry(window1, font=32)
    entry_create.place(x=xbtn, y=3*ybtn, width=8*xbtn, height=ybtn)
    labal_create = Label(window1, text='Створити файл')
    labal_create.place(x=xbtn, y=ybtn, width=8*xbtn, height=ybtn)
    btn_create = Button(window1, text='Створити', command=entry_get_create)
    btn_create.place(x=xbtn, y=4*ybtn, width=2*xbtn, height=ybtn)

    window1.mainloop()

aaa = print_all_notes()
tabs(aaa)

root.mainloop()
