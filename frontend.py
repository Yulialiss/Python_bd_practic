import os
import mysql.connector
from dotenv import load_dotenv
from backend import DB
import tkinter as tk
from tkinter import ttk, messagebox


class Application(tk.Tk):
    def __init__(self, db):
        super().__init__()

        self.db = db
        self.title('Студенти Боско')
        self.geometry('800x800')
        self.db.create_db()
        self.db.create_table()
        self.create_inteface()
        self.create_treeview()
        self.load_records()

        self.label_style = ttk.Style(self)
        self.button_style = ttk.Style(self)
        self.entry_style = ttk.Style(self)

        self.label_style.configure("My.TLabel",
                                   font="helvetica 14",
                                   foreground="white",
                                   background="black",
                                   padding=10)

        self.button_style.configure("My.TButton",
                                    font="helvetica 10",
                                    background="white",
                                    padding=5,
                                    relief="flat",
                                    borderwidth=1,
                                    width=20,
                                    height=4,
                                    anchor="center")

        self.entry_style.configure("My.TEntry",
                                   font="helvetica 12",
                                   padding=5,
                                   relief="solid",
                                   background="gray",
                                   width=30,
                                   height=4,
                                   foreground="black")

    def create_inteface(self):
        self.config(bg="black")

        ttk.Label(self, text='Список', style="My.TLabel").place(x=370, y=400)

        ttk.Label(self, text='Прізвище', style="My.TLabel").place(x=20, y=20)
        self.last_name = ttk.Entry(self, style="My.TEntry")
        self.last_name.place(x=220, y=25)

        ttk.Label(self, text='Імя', style="My.TLabel").place(x=20, y=65)
        self.first_name = ttk.Entry(self, style="My.TEntry")
        self.first_name.place(x=220, y=65)
        ttk.Label(self, text='Логін', style="My.TLabel").place(x=20, y=100)
        self.login = ttk.Entry(self, style="My.TEntry")
        self.login.place(x=220, y=105)

        ttk.Label(self, text='Пароль', style="My.TLabel").place(x=20, y=140)
        self.password = ttk.Entry(self, show='*', style="My.TEntry")
        self.password.place(x=220, y=145)

        ttk.Label(self, text='Місце проживання', style="My.TLabel").place(x=20, y=175)
        self.place_birth = ttk.Entry(self, style="My.TEntry")
        self.place_birth.place(x=220, y=185)

        self.add_record = ttk.Button(self, text='Додати запис', style="My.TButton", command=self.add_record)
        self.add_record.place(x=380, y=260)
        self.delete_record = ttk.Button(self, text='Видалити запис', command=self.delete_record, style="My.TButton")
        self.delete_record.place(x=550, y=260)
        self.search_button = ttk.Button(self, text="Шукати", command=self.search_user, style="My.TButton")
        self.search_button.place(x=350, y=330)
        self.exit_button = ttk.Button(self, text='Вийти', command=self.destroy, style="My.TButton")
        self.exit_button.place(x=650, y=700)

        ttk.Label(self, text='Пошук за логіном:', style="My.TLabel").place(x=20, y=330)
        self.search_login = ttk.Entry(self, style="My.TEntry")
        self.search_login.place(x=200, y=335)

    def create_treeview(self):
        columns = [
            ('id', 'id', 30),
            ('last_name', 'Прізвище', 120),
            ('first_name', 'Імя', 120),
            ('login', 'Логін', 100),
            ('birth_place', 'Місце народження', 180),
        ]

        self.tree = ttk.Treeview(self, columns=[col[0] for col in columns], show='headings')

        for col_id, col_text, col_width in columns:
            self.tree.heading(col_id, text=col_text)
            self.tree.column(col_id, width=col_width)

        self.tree.place(x=150, y=450, width=550, height=200)

    def add_record(self):
        last_name = self.last_name.get()
        first_name = self.first_name.get()
        login = self.login.get()
        password = self.password.get()
        place_birth = self.place_birth.get()

        if last_name and first_name and login and password and place_birth:
            try:
                self.db.add_user(last_name, first_name, login, password, place_birth)
                messagebox.showinfo("Успіх", "Запис додано успішно")
                self.load_records()
            except mysql.connector.Error as error:
                messagebox.showerror("Помилка", f"Не вдалося додати запис: {error}")
        else:
            messagebox.showwarning("Попередження", "Всі поля мають бути заповнені")

    def delete_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            user_id = self.tree.item(selected_item, 'values')[0]
            try:
                self.db.delete_user(user_id)
                messagebox.showinfo("Успіх", "Запис видалено успішно")
                self.load_records()
            except mysql.connector.Error as error:
                messagebox.showerror("Помилка", f"Не вдалося видалити запис: {error}")
        else:
            messagebox.showwarning("Попередження", "Не обрано запис для видалення")

    def search_user(self):
        login_to_search = self.search_login.get()
        if login_to_search:
            users = self.db.search_user_by_login(login_to_search)
            if users:
                for item in self.tree.get_children():
                    self.tree.delete(item)

                for user in users:
                    self.tree.insert("", tk.END, values=user)
            else:
                messagebox.showwarning("Не знайдено", "Користувача з таким логіном не знайдено.")
        else:
            messagebox.showwarning("Попередження", "Будь ласка, введіть логін для пошуку.")

    def load_records(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            records = self.db.show_users()
            for record in records:
                self.tree.insert("", tk.END, values=record)
        except mysql.connector.Error as error:
            messagebox.showerror("Помилка", f"Не вдалося завантажити записи: {error}")


if __name__ == '__main__':
    load_dotenv()
    db = DB(
        host=os.getenv('HOST'),
        port=os.getenv('PORT'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD')
    )
    app = Application(db)
    app.mainloop()
