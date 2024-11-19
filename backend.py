import mysql.connector

class DB:
    def __init__(self, host, port, user, password):
        try:
            self.mysql_connection=mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
            )
            self.cursor=self.mysql_connection.cursor()
            print('Успішне зєднання')
        except mysql.connector.Error as error:
            print(f'Помилка {error}')

    def create_db(self):
        try:
            self.cursor.execute("""create schema if not exists Info
                                default character set cp1251
                                collate cp1251_ukrainian_ci""")
            print('Базу створено')
        except mysql.connector.Error as error:
            print(f'Помилка {error}')

    def create_table(self):
        try:
            self.cursor.execute("""use Info""")
            self.cursor.execute("""create table if not exists users(
            users_id            int auto_increment primary key,
            last_name           varchar(50) not null,
            first_name          varchar(50) not null,
            login               varchar(32) unique,
            password            varchar(100),
            birth_place         varchar(50))
            """)
            print('Таблицю створено')
        except mysql.connector.Error as error:
            print(f'Помилка {error}')

    def add_user(self, l_name, f_name, log, passwd, bh_place):
        try:
            self.cursor.execute('use info')
            self.cursor.execute("""
            insert into users (last_name, first_name, login, password, birth_place) values
            (%s, %s, %s, %s, %s)  """, (l_name, f_name, log, passwd, bh_place))
            self.mysql_connection.commit()
            return 'Користувача додано'

        except mysql.connector.Error as error:
            return f'Помилка {error}'

    def show_users(self):
        try:
            self.cursor.execute("USE Info")
            self.cursor.execute("SELECT users_id, last_name, first_name, login, birth_place FROM users")
            records = self.cursor.fetchall()
            return records
        except mysql.connector.Error as error:
            print(f'Error fetching users: {error}')
            return []

    def delete_user(self, user_id):
            try:
                query = "DELETE FROM users WHERE users_id = %s"
                self.cursor.execute(query, (user_id,))
                self.mysql_connection.commit()
            except mysql.connector.Error as error:
                raise Exception(f"Помилка при видаленні запису: {error}")

    def search_user_by_login(self, login):
        query = "SELECT users_id, last_name, first_name, login, birth_place FROM users WHERE login LIKE %s"
        self.cursor.execute(query, ('%' + login + '%',))
        return self.cursor.fetchall()