import sqlite3


class DatabaseManager():

    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE if not exists todo(
                title text,
                description text,
                date text,
                status bool
            )
        """)

        self.conn.commit()

    def get_todo(self, date):
        self.cursor.execute("""
            SELECT * FROM todo
            WHERE date = :date
        """,
        {
            'date': date
        })

        records = self.cursor.fetchall()

        self.conn.commit()

        return records

    def add_todo(self, title, description, date):
        result = None
        self.cursor.execute("""
            SELECT * FROM todo
            WHERE date = :date AND title = :title AND description = :description
        """,
        {
            'date': date,
            'title': title,
            'description': description
        })

        records = self.cursor.fetchall()

        if len(records) == 0:
            self.cursor.execute("""
                INSERT INTO todo
                VALUES (:title, :description, :date, :status)
            """,
            {
                'title': title,
                'description': description,
                'date': date,
                'status': False
            })
            result = True
        else:
            result = False

        self.conn.commit()

        return result

    def update_todo(self, title, description, date, status):
        self.cursor.execute("""
                UPDATE todo
                SET status = :status
                WHERE date = :date AND title = :title AND description = :description
            """,
            {
                'title': title,
                'description': description,
                'date': date,
                'status': status
            })

        self.conn.commit()
