import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('goodgraphsync.db')
        self.cursor = self.conn.cursor()
        self.setup_database()

    def setup_database(self):
        # Drop existing table and create new one with unique constraint
        self.cursor.execute('DROP TABLE IF EXISTS books')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                title TEXT,
                author TEXT,
                status TEXT,
                platform TEXT,
                rating INTEGER,
                UNIQUE(title, author, platform)
            )
        ''')
        self.conn.commit()

    def add_book(self, title, author, status, platform, rating=0):
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO books (title, author, status, platform, rating)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, author, status, platform, rating))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass  # Ignore duplicate entries

    def get_books(self, platform):
        self.cursor.execute('SELECT * FROM books WHERE platform = ?', (platform,))
        return self.cursor.fetchall()

    def clear_all_books(self):
        self.cursor.execute('DELETE FROM books')
        self.conn.commit()

    def close(self):
        self.conn.close()