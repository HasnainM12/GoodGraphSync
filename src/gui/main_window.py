from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                            QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem)
from .database import Database 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GoodGraphSync")
        self.setFixedSize(600, 400)
        
        # Initialize database
        self.db = Database()
        
        # Main widget setup
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout(main_widget)
        
        # Login inputs
        self.gr_username = QLineEdit()
        self.gr_username.setPlaceholderText("Goodreads Username")
        self.gr_password = QLineEdit()
        self.gr_password.setPlaceholderText("Goodreads Password")
        self.gr_password.setEchoMode(QLineEdit.Password)
        
        self.sg_username = QLineEdit()
        self.sg_username.setPlaceholderText("StoryGraph Username")
        self.sg_password = QLineEdit()
        self.sg_password.setPlaceholderText("StoryGraph Password")
        self.sg_password.setEchoMode(QLineEdit.Password)
        
        # Login button
        self.login_btn = QPushButton("Login and Sync")
        self.login_btn.clicked.connect(self.handle_login)
        
        # Book table
        self.book_table = QTableWidget()
        self.book_table.setColumnCount(4)
        self.book_table.setHorizontalHeaderLabels(["Title", "Author", "Status", "Platform"])
        self.book_table.hide()  # Hide initially
        
        # Add widgets to layout
        self.layout.addWidget(self.gr_username)
        self.layout.addWidget(self.gr_password)
        self.layout.addWidget(self.sg_username)
        self.layout.addWidget(self.sg_password)
        self.layout.addWidget(self.login_btn)
        self.layout.addWidget(self.book_table)
        
    def handle_login(self):
        # Clear existing books first
        self.db.clear_all_books()
    
        # Add test data (we'll replace this with real scraping later)
        self.db.add_book("The Hobbit", "J.R.R. Tolkien", "Reading", "Goodreads", 5)
        self.db.add_book("1984", "George Orwell", "Want to Read", "StoryGraph", 0)
    
        # Hide login fields
        self.gr_username.hide()
        self.gr_password.hide()
        self.sg_username.hide()
        self.sg_password.hide()
        self.login_btn.hide()
    
        # Show and populate book table
        self.book_table.show()
        self.show_books()
        
    def show_books(self):
        # Get all books from both platforms
        goodreads_books = self.db.get_books("Goodreads")
        storygraph_books = self.db.get_books("StoryGraph")
        all_books = goodreads_books + storygraph_books
        
        # Set table rows
        self.book_table.setRowCount(len(all_books))
        
        # Fill table
        for row, book in enumerate(all_books):
            title, author, status, platform, _ = book  # Unpack book data (ignore rating for now)
            self.book_table.setItem(row, 0, QTableWidgetItem(title))
            self.book_table.setItem(row, 1, QTableWidgetItem(author))
            self.book_table.setItem(row, 2, QTableWidgetItem(status))
            self.book_table.setItem(row, 3, QTableWidgetItem(platform))
            
    def closeEvent(self, event):
        self.db.close()
        event.accept()