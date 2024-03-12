from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from .extensions import Base
import hashlib
import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(120), unique=True)
    password = Column(String(128))


    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        if password:
            self.set_password(password)

    def __repr__(self):
        return f"Person(name='{self.username}', email={self.email})"
    
    def set_password(self, password):
        """Hashes the password and sets the password_hash attribute."""
        self.password = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        """Checks if the provided password matches the stored hashed password."""
        return self.password == hashlib.sha256(password.encode()).hexdigest()


class Sections(Base):
    __tablename__ = 'sections'
    id = Column(Integer, primary_key=True)
    section = Column(String(50))
    description = Column(String(200))

    def __init__(self, section=None, description=None):
        self.section = section
        self.description = description

    def __repr__(self):
        return f"Section(section='{self.section}', description={self.description})"
    

class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    author = Column(String(50))
    section = Column(Integer, ForeignKey('sections.id'))
    description = Column(String(200))
    available_copies = Column(Integer)
    image = Column(String(200))
    content = Column(String(200))

    def __init__(self, title=None, author=None, section=None, description=None, available_copies=None):
        self.title = title
        self.author = author
        self.section = section
        self.description = description
        self.available_copies = available_copies

    def __repr__(self):
        return f"Book(title='{self.title}', author={self.author}, section={self.section}, description={self.description}, available_copies={self.available_copies})"
    
    
class BorrowedBooks(Base):
    __tablename__ = 'borrowed_books'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    borrow_date = Column(Date, default = datetime.date.today())
    return_date = Column(Date, default = datetime.date.today() + datetime.timedelta(days=7))
    actual_return_date = Column(Date, nullable=True)
    is_returned = Column(Boolean, default = False)

    def __init__(self, user_id=None, book_id=None):
        self.user_id = user_id
        self.book_id = book_id

    def __repr__(self):
        return f"BorrowedBook(user_id='{self.user_id}', book_id={self.book_id}, borrow_date={self.borrow_date}, return_date={self.return_date}, actual_return_date={self.actual_return_date}, is_returned={self.is_returned})"


class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    feedback = Column(String(200))

    def __init__(self, user_id=None, feedback=None):
        self.user_id = user_id
        self.feedback = feedback

    def __repr__(self):
        return f"Feedback(user_id='{self.user_id}', feedback={self.feedback})"
    

