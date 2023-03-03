import os
import base
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


def create():
    base.start_base()
    lab1.config(state='enabled')
    lab2.config(state='enabled')
    lab3.config(state='enabled')
    ent1.config(state='enabled')
    ent2.config(state='enabled')
    ent3.config(state='enabled')
    create_btn.config(state='disabled')
    add_btn.config(state='enabled')
    show_btn.config(state='enabled')
    delete_base_btn.config(state='enabled')


def add():
    name = ent1.get()
    surname = ent2.get()
    age = ent3.get()

    if name and surname and age:
        base.sql_add(name, surname, age)
        ent1.delete(0, END)
        ent2.delete(0, END)
        ent3.delete(0, END)
        messagebox.showinfo('Person was added', f'{name.capitalize()} {surname.capitalize()}({age} y.o) was added successfully!')
    else:
        messagebox.showwarning('Warnning', 'Field(s) are empty')


def delete(i):
    new_list = base.sql_delete(i)
    messagebox.showinfo('Person was added', f'{new_list[0].capitalize()} {new_list[1].capitalize()}({new_list[2]} y.o) was deleted!')
    new.destroy()


def show():
    res = base.sql_show()

    if len(res) == 0:
        messagebox.showwarning('Warnning', 'Database is empty, nothing to show')
    else:
        global new
        new = Toplevel()
        new.title('Show')
        new.geometry('500x500')
        new.resizable(0, 0)

        def _on_mouse_wheel(event):
            canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

        canvas = Canvas(new, bd=0, highlightthickness=0, relief='ridge')
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

        scroller = ttk.Scrollbar(new, orient=VERTICAL, command=canvas.yview)
        scroller.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scroller.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        frame = Frame(canvas)
        canvas.create_window((0,0), window=frame, anchor=NW)
        if len(res) > 9:
            frame.bind_all("<MouseWheel>", _on_mouse_wheel)

        heading_frame = Frame(frame, height=30)
        heading_frame.pack(expand=True, fill=BOTH)

        frame1 = Frame(frame, height=len(res)*50, width=130)
        frame1.pack(padx=10, side=LEFT, fill=Y)

        frame2 = Frame(frame, height=len(res)*50, width=130)
        frame2.pack(side=LEFT, fill=Y)

        frame3 = Frame(frame, height=len(res)*50, width=130)
        frame3.pack(padx=10, side=LEFT, fill=Y)

        frame4 = Frame(frame, height=len(res)*50, width=50)
        frame4.pack(side=LEFT, fill=Y)

        lab_1 = ttk.Label(heading_frame, text='Name')
        lab_1.place(x = 60, y = 10)
        lab_2 = ttk.Label(heading_frame, text='Surname')
        lab_2.place(x = 190, y = 10)
        lab_3 = ttk.Label(heading_frame, text='Age')
        lab_3.place(x = 345, y = 10)

        for i in range(len(res)):
            name_box = ttk.Entry(frame1)
            name_box.place(anchor=CENTER, x=65, y=(i+1)*50-25)
            name_box.insert(1, res[i][0])
            name_box.config(state='readonly')

            surname_box = ttk.Entry(frame2)
            surname_box.place(anchor=CENTER, x=65, y=(i+1)*50-25)
            surname_box.insert(1, res[i][1])
            surname_box.config(state='readonly')

            age_box = ttk.Entry(frame3)
            age_box.place(anchor=CENTER, x=65, y=(i+1)*50-25)
            age_box.insert(1, res[i][2])
            age_box.config(state='readonly')

            delete_member = ttk.Button(frame4, text='X', width=3, command=lambda: delete(i), cursor='hand2')
            delete_member.place(anchor=CENTER, x=20, y=(i+1)*50-25)


def delete_base():
    if messagebox.askyesno('Warning', 'All data will be permanently deleted!\nAre you sure?'):
        base.delete_base()
        lab1.config(state='disabled')
        lab2.config(state='disabled')
        lab3.config(state='disabled')
        ent1.config(state='disabled')
        ent2.config(state='disabled')
        ent3.config(state='disabled')
        create_btn.config(state='enabled', text='Create')
        add_btn.config(state='disabled')
        show_btn.config(state='disabled')
        delete_base_btn.config(state='disabled')


window = Tk()
window.title('Database')
window.geometry('400x300')
window.resizable(0, 0)

lab1 = ttk.Label(window, text='Name', state='disabled')
lab1.place(x = 15, y = 15)
lab2 = ttk.Label(window, text='Surname', state='disabled')
lab2.place(x = 15, y = 40)
lab3 = ttk.Label(window, text='Age', state='disabled')
lab3.place(x = 15, y = 65)

ent1 = ttk.Entry(window, width=35, state='disabled')
ent1.place(anchor=N, x = 200, y = 15)

ent2 = ttk.Entry(window, width=35, state='disabled')
ent2.place(anchor=N, x = 200, y = 40)

ent3 = ttk.Entry(window, width=35, state='disabled')
ent3.place(anchor=N, x = 200, y = 65)

create_btn = ttk.Button(window, text='Create',command=create, cursor='hand2')
create_btn.place(x = 35, y = 260)
if os.path.exists('database.db'):
    create_btn.config(text='Connect')

add_btn = ttk.Button(window, text='Add', command=add, state='disabled', cursor='hand2')
add_btn.place(x = 119.5, y = 260)

show_btn = ttk.Button(window, text='Show', command=show, state='disabled', cursor='hand2')
show_btn.place(x = 203.5, y = 260)

delete_base_btn = ttk.Button(window, text='Delete DB', command=delete_base, state='disabled', cursor='hand2')
delete_base_btn.place(x = 289, y = 260)

window.mainloop()