import os
import base
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


window = Tk()
window.title('Database')
window.geometry('400x300')
window.resizable(0, 0)


class Database:

    def __init__(self, master:Tk) -> None:
        self.master = master

        self.lab1 = ttk.Label(window, text='Name', state='disabled')
        self.lab1.place(x = 15, y = 15)
        self.lab2 = ttk.Label(window, text='Surname', state='disabled')
        self.lab2.place(x = 15, y = 40)
        self.lab3 = ttk.Label(window, text='Age', state='disabled')
        self.lab3.place(x = 15, y = 65)

        self.ent1 = ttk.Entry(window, width=35, state='disabled')
        self.ent1.bind('<Return>', self.add)
        self.ent1.place(anchor=N, x = 200, y = 15)

        self.ent2 = ttk.Entry(window, width=35, state='disabled')
        self.ent2.bind('<Return>', self.add)
        self.ent2.place(anchor=N, x = 200, y = 40)

        self.ent3 = ttk.Entry(window, width=35, state='disabled')
        self.ent3.bind('<Return>', self.add)
        self.ent3.place(anchor=N, x = 200, y = 65)

        self.create_btn = ttk.Button(window, text='Create',command=self.create, cursor='hand2')
        self.create_btn.place(x = 35, y = 260)
        if os.path.exists('database.db'):
            self.create_btn.config(text='Connect')

        self.add_btn = ttk.Button(window, text='Add', command=self.add, state='disabled', cursor='hand2')
        self.add_btn.place(x = 119.5, y = 260)

        self.show_btn = ttk.Button(window, text='Show', command=self.show, state='disabled', cursor='hand2')
        self.show_btn.place(x = 203.5, y = 260)

        self.delete_base_btn = ttk.Button(window, text='Delete DB', command=self.delete_base, state='disabled', cursor='hand2')
        self.delete_base_btn.place(x = 289, y = 260)

    def create(self):
        base.start_base()
        self.lab1.config(state='enabled')
        self.lab2.config(state='enabled')
        self.lab3.config(state='enabled')
        self.ent1.config(state='enabled')
        self.ent2.config(state='enabled')
        self.ent3.config(state='enabled')
        self.create_btn.config(state='disabled')
        self.add_btn.config(state='enabled')
        self.show_btn.config(state='enabled')
        self.delete_base_btn.config(state='enabled')

    def add(self, event=None):
        name = self.ent1.get()
        surname = self.ent2.get()
        age = self.ent3.get()

        if name and surname and age:
            if not name.isnumeric() and not surname.isnumeric() and age.isnumeric():
                base.sql_add(name, surname, age)
                self.ent1.delete(0, END)
                self.ent2.delete(0, END)
                self.ent3.delete(0, END)
                messagebox.showinfo('Person was added', f'{name.capitalize()} {surname.capitalize()}({age} y.o) was added successfully!')
            else:
                messagebox.showwarning('Warnning', 'Wrong type of data')
        else:
            messagebox.showwarning('Warnning', 'Field(s) are empty')

    def delete(self, i):
        new_list = base.sql_delete(i)
        messagebox.showinfo('Person was added', f'{new_list[0].capitalize()} {new_list[1].capitalize()}({new_list[2]} y.o) was deleted!')
        self.new.destroy()

    def show(self):
        res = base.sql_show()

        if len(res) == 0:
            messagebox.showwarning('Warnning', 'Database is empty, nothing to show')
        else:
            self.new = Toplevel()
            self.new.title('Show')
            self.new.geometry('500x500')
            self.new.resizable(0, 0)

            def _on_mouse_wheel(event):
                self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

            self.canvas = Canvas(self.new, bd=0, highlightthickness=0, relief='ridge')
            self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

            self.scroller = ttk.Scrollbar(self.new, orient=VERTICAL, command=self.canvas.yview)
            self.scroller.pack(side=RIGHT, fill=Y)

            self.canvas.configure(yscrollcommand=self.scroller.set)
            self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

            self.frame = Frame(self.canvas)
            self.canvas.create_window((0,0), window=self.frame, anchor=NW)
            if len(res) > 9:
                self.frame.bind_all("<MouseWheel>", _on_mouse_wheel)

            self.heading_frame = Frame(self.frame, height=30)
            self.heading_frame.pack(expand=True, fill=BOTH)

            self.frame1 = Frame(self.frame, height=len(res)*50, width=130)
            self.frame1.pack(padx=10, side=LEFT, fill=Y)

            self.frame2 = Frame(self.frame, height=len(res)*50, width=130)
            self.frame2.pack(side=LEFT, fill=Y)

            self.frame3 = Frame(self.frame, height=len(res)*50, width=130)
            self.frame3.pack(padx=10, side=LEFT, fill=Y)

            self.frame4 = Frame(self.frame, height=len(res)*50, width=50)
            self.frame4.pack(side=LEFT, fill=Y)

            self.lab_1 = ttk.Label(self.heading_frame, text='Name')
            self.lab_1.place(x = 60, y = 10)
            self.lab_2 = ttk.Label(self.heading_frame, text='Surname')
            self.lab_2.place(x = 190, y = 10)
            self.lab_3 = ttk.Label(self.heading_frame, text='Age')
            self.lab_3.place(x = 345, y = 10)

            for i in range(len(res)):
                name_box = ttk.Entry(self.frame1)
                name_box.place(anchor=CENTER, x=65, y=(i+1)*50-25)
                name_box.insert(1, res[i][0])
                name_box.config(state='readonly')

                surname_box = ttk.Entry(self.frame2)
                surname_box.place(anchor=CENTER, x=65, y=(i+1)*50-25)
                surname_box.insert(1, res[i][1])
                surname_box.config(state='readonly')

                age_box = ttk.Entry(self.frame3)
                age_box.place(anchor=CENTER, x=65, y=(i+1)*50-25)
                age_box.insert(1, res[i][2])
                age_box.config(state='readonly')

                delete_member = ttk.Button(self.frame4, text='X', width=3, command=lambda: self.delete(i), cursor='hand2')
                delete_member.place(anchor=CENTER, x=20, y=(i+1)*50-25)

    def delete_base(self):
        if messagebox.askyesno('Warning', 'All data will be permanently deleted!\nAre you sure?'):
            base.delete_base()
            self.lab1.config(state='disabled')
            self.lab2.config(state='disabled')
            self.lab3.config(state='disabled')
            self.ent1.config(state='disabled')
            self.ent2.config(state='disabled')
            self.ent3.config(state='disabled')
            self.create_btn.config(state='enabled', text='Create')
            self.add_btn.config(state='disabled')
            self.show_btn.config(state='disabled')
            self.delete_base_btn.config(state='disabled')


db = Database(window)
window.mainloop()