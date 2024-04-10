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
        print(self.password == hashlib.sha256(password.encode()).hexdigest())
        return self.password == hashlib.sha256(password.encode()).hexdigest()


class Librarian(Base):
    __tablename__ = 'librarians'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(128))

    def __init__(self, username=None, password=None):
        self.username = username
        if password:
            self.set_password(password)

    def __repr__(self):
        return f"Librarian(name='{self.username}')"
    
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
    date_created = Column(Date, default = datetime.date.today())
    is_deleted = Column(Boolean, default = False)

    def __init__(self, section=None, description=None):
        self.section = section
        self.description = description

    def __repr__(self):
        return f"Section(section='{self.section}', description={self.description})"
    
    def serialize(self):
        return {
            'id': self.id,
            'section': self.section,
            'description': self.description,
            'date_created': self.date_created,
            'is_deleted': self.is_deleted
        }
    

class Books(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    author = Column(String(50))
    section = Column(Integer, ForeignKey('sections.id'))
    description = Column(String(200))
    available_copies = Column(Integer)
    image = Column(String(200), nullable=True)
    is_deleted = Column(Boolean, default = False)
    # content = Column(String(200))

    def __init__(self, title=None, author=None, section=None, description=None, available_copies=None, image=None):
        self.title = title
        self.author = author
        self.section = section
        self.description = description
        self.available_copies = available_copies
        self.image = image

    def __repr__(self):
        return f"Book(title='{self.title}', author={self.author}, section={self.section}, description={self.description}, available_copies={self.available_copies}, image={self.image})"
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'section': self.section,
            'description': self.description,
            'available_copies': self.available_copies,
            'image': self.image,
            'is_deleted': self.is_deleted
            # 'content': self.content
        }
    
    
class BorrowedBooks(Base):
    __tablename__ = 'borrowed_books'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    borrow_date = Column(Date, default = datetime.date.today())
    scheduled_return_date = Column(Date, default = datetime.date.today() + datetime.timedelta(days=7))
    actual_return_date = Column(Date, nullable=True)
    is_returned = Column(Boolean, default = False)
    is_approved = Column(Boolean, default = False)
    is_rejected = Column(Boolean, default = False)
    is_revoked = Column(Boolean, default = False)

    def __init__(self, user_id=None, book_id=None):
        self.user_id = user_id
        self.book_id = book_id

    def __repr__(self):
        return f"BorrowedBook(user_id='{self.user_id}', book_id={self.book_id}, borrow_date={self.borrow_date}, scheduled_return_date={self.scheduled_return_date}, actual_return_date={self.actual_return_date}, is_returned={self.is_returned}, is_approved={self.is_approved}, is_rejected={self.is_rejected}, is_revoked={self.is_revoked})"
    
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'borrow_date': self.borrow_date,
            'scheduled_return_date': self.scheduled_return_date,
            'actual_return_date': self.actual_return_date,
            'is_returned': self.is_returned,
            'is_approved': self.is_approved,
            'is_rejected': self.is_rejected,
            'is_revoked': self.is_revoked
        }


class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    feedback_rating = Column(Integer)

    def __init__(self, user_id=None, book_id=None, feedback_rating=None):
        self.user_id = user_id
        self.book_id = book_id
        self.feedback_rating = feedback_rating

    def __repr__(self):
        return f"Feedback(user_id='{self.user_id}', feedback={self.feedback_rating})"
    

class LoginLogs(Base):
    __tablename__ = 'login_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    login_date = Column(Date, default = datetime.date.today())

    def __init__(self, user_id=None):
        self.user_id = user_id

    def __repr__(self):
        return f"LoginHistory(user_id='{self.user_id}', login_date={self.login_date}, logout_date={self.logout_date})"
    
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'login_date': self.login_date,
            'logout_date': self.logout_date
        }