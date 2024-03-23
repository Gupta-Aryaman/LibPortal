from flask import Blueprint, request, make_response
from .extensions import db_session
from .models import *
import jwt
import datetime
from dotenv import load_dotenv
import os
from .helpers import user_token_required, librarian_token_required
from random import shuffle

load_dotenv()

main = Blueprint('main', __name__)
secret_key = os.getenv('SECRET_KEY')


@main.route('/signup', methods = ["POST"])
def signup_user():
    '''
    Signup endpoint for a student (user)
    '''
    if request.method == "POST":
        try:
            username = request.json["username"]
            email = request.json['email']
            password = request.json['password']

            fetch_existing_email = db_session.query(User).filter(User.email == email).all()

            if fetch_existing_email:
                return make_response({"Status": "email already exists"}, 403)

            u = User(username, email, password)
            db_session.add(u)
            db_session.commit()

            return make_response({"Status": "User added succesfully"}, 200)
        
        except Exception as e:
            return make_response({'Error: ': str(e)}, 500)
    
    return make_response({"Status": 'Internal Server Error!'}, 500)


@main.route('/login', methods = ["POST"])
def login_user():
    '''
    Login endpoint for a student (user)
    '''
    if request.method == "POST":
        try:
            email = request.json['email']
            password = request.json['password']

            fetch_user = db_session.query(User).filter(User.email == email and User.check_password(password)).all()

            if not fetch_user:
                return make_response({"Status": "Invalid Credentials"}, 401)

            fetch_user = fetch_user[0]
            token = jwt.encode({'username': fetch_user.username, 'email': fetch_user.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, secret_key)

            return make_response({"Status": "User login successful", "token": token, "user": fetch_user.username}, 200)
        
        except Exception as e:
            return make_response({'Error: ': str(e)}, 500)
        
    return make_response({"Status": 'Internal Server Error!'}, 500)


# search a book by title
# see all books

# borrow a book
# return a book
# see all borrowed books
# see all returned books
# see all books in a section

@main.route('/list_books', methods = ["GET"])
@user_token_required
def list_books(current_user):
    '''
    List all books or search a book by title
    '''
    try:
        if request.args.get("title"):
            title = request.args.get("title")

            if request.args.get("section"):
                section = request.args.get("section")
                books = db_session.query(Books, Sections.section).join(Sections, Books.section == Sections.id).filter(Books.title.like("%" + title + "%"), Sections.section.ilike(section)).all()
            else:
                books = db_session.query(Books, Sections.section).join(Sections, Books.section == Sections.id).filter(Books.title.like("%" + title + "%")).all()

            # return make_response({"Books": [book.serialize() for book in books]}, 200)
        
        elif request.args.get("section"):
            section = request.args.get("section")
            books = db_session.query(Books, Sections.section).join(Sections, Books.section == Sections.id).filter(Sections.section.like("%"+section+"%")).all()
            # return make_response({"Books": [book.serialize() for book in books]}, 200)

        else:
            books = db_session.query(Books, Sections.section).join(Sections, Books.section == Sections.id).all()
        
        borrowed_books = db_session.query(BorrowedBooks).filter(BorrowedBooks.user_id == current_user.id, BorrowedBooks.is_returned == False, BorrowedBooks.is_revoked == False, BorrowedBooks.is_rejected == False).all()
        borrowed_books = [book.book_id for book in borrowed_books]

        res = []
        for book, section in books:
            if book.id in borrowed_books:
                res.append({"id": book.id, "title": book.title, "author": book.author, "section": section, "description": book.description, "available_copies": book.available_copies, "is_borrowed": True})
            else:
                res.append({"id": book.id, "title": book.title, "author": book.author, "section": section, "description": book.description, "available_copies": book.available_copies, "is_borrowed": False})
        # shuffle(res)
        return make_response({"Books": res}, 200)
        
    except Exception as e:
        print(str(e))
        return make_response({"Status": str(e)}, 500)


@main.route('/borrow_book', methods = ["POST"])
@user_token_required
def borrow_book(current_user):
    '''
    Borrow a book
    '''
    try:
        book_id = request.json['book_id']
        book = db_session.query(Books).filter(Books.id == book_id).first()

        if book.available_copies == 0:
            return make_response({"Status": "Book not available"}, 403)

        # book.available_copies -= 1

        b = BorrowedBooks(current_user.id, book.id)
        db_session.add(b)
        db_session.commit()

        return make_response({"Status": "Book borrowed successfully"}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)
    

@main.route('/return_book', methods = ["POST"])
@user_token_required
def return_book(current_user):
    '''
    Return a book
    '''
    try:
        book_id = request.json['book_id']
        borrowed_book = db_session.query(BorrowedBooks).filter(BorrowedBooks.book_id == book_id, BorrowedBooks.user_id == current_user.id, BorrowedBooks.is_returned == False, BorrowedBooks.is_approved == True, BorrowedBooks.is_revoked == False).first()

        if not borrowed_book:
            return make_response({"Status": "Book not borrowed by you"}, 403)

        borrowed_book.is_returned = True
        borrowed_book.actual_return_date = datetime.date.today()

        book = db_session.query(Books).filter(Books.id == book_id).first()
        book.available_copies += 1

        db_session.commit()

        return make_response({"Status": "Book returned successfully"}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)
    

@main.route('/list_borrowed_books', methods = ["GET"])
@user_token_required
def list_borrowed_books(current_user):
    '''
    List all borrowed books
    '''
    try:
        borrowed_books = db_session.query(BorrowedBooks).filter(BorrowedBooks.user_id == current_user.id, BorrowedBooks.is_returned == False, BorrowedBooks.is_approved == True, BorrowedBooks.is_revoked == False).all()
        print(borrowed_books)

        return make_response({"Borrowed Books": [book.serialize() for book in borrowed_books]}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)
    

@main.route('/list_returned_books', methods = ["GET"])
@user_token_required
def list_returned_books(current_user):
    '''
    List all returned books
    '''
    try:
        returned_books = db_session.query(BorrowedBooks).filter(BorrowedBooks.user_id == current_user.id, BorrowedBooks.is_returned == True).all()
        return make_response({"Returned Books": [book.serialize() for book in returned_books]}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)


@main.route('/add_feedback', methods = ["POST"])
@user_token_required
def add_feedback(current_user):
    '''
    Feedback endpoint for a student (user)
    '''
    try:
        feedback = request.json['feedback']
        book_id = request.json['book_id']
        f = Feedback(current_user.id, book_id, feedback)
        db_session.add(f)
        db_session.commit()

        return make_response({"Status": "Feedback added successfully"}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)
    

@main.route('/list_feedback', methods = ["GET"])
@user_token_required
def list_feedback(current_user):
    '''
    List all feedback
    '''
    try:
        book_id = request.args.get['book_id']
        feedback = db_session.query(Feedback).filter(Feedback.book_id == book_id).all()
        return make_response({"Feedback": [fb.serialize() for fb in feedback]}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)
    


#######################
#                     #
# LIBRARIAN ENDPOINTS #
#                     #
#######################

@main.route('/librarian/login', methods = ["POST"])
def login_librarian():
    '''
    Login endpoint for a librarian
    '''
    if request.method == "POST":
        try:
            username = request.json['username']
            password = request.json['password']

            fetch_librarian = db_session.query(Librarian).filter(Librarian.username == username and Librarian.check_password(password)).all()

            if not fetch_librarian:
                return make_response({"Status": "Invalid Credentials"}, 401)

            fetch_librarian = fetch_librarian[0]
            token = jwt.encode({'username': fetch_librarian.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, secret_key)

            return make_response({"Status": "Librarian login successful", "token": token}, 200)
        
        except Exception as e:
            return make_response({'Error: ': str(e)}, 500)
        
    return make_response({"Status": 'Internal Server Error!'}, 500)

       
@main.route('/librarian/add_section', methods = ["POST"])
@librarian_token_required
def add_section(current_user):
    '''
    Add a section
    '''
    try:
        section = request.json['section']
        description = request.json['description']
        s = Sections(section, description)
        db_session.add(s)
        db_session.commit()

        return make_response({"Status": "Section added successfully"}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)
    

@main.route('/librarian/add_book', methods = ["POST"])
@librarian_token_required
def add_book(current_user):
    '''
    Add a book
    '''
    try:
        title = request.json['title']
        author = request.json['author']
        section = request.json['section']
        description = request.json['description']
        available_copies = request.json['available_copies']

        # content = request.json['content']

        section = db_session.query(Sections).filter(Sections.section.ilike(section)).first()
        book = Books(title, author, section.id, description, available_copies)
        db_session.add(book)
        db_session.commit()

        return make_response({"Status": "Book added successfully"}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)
    

@main.route('/librarian/list_sections', methods = ["GET"])
@librarian_token_required
def list_sections(current_user):
    '''
    List all sections
    '''
    try:
        sections = db_session.query(Sections).all()
        return make_response({"Sections": [section.serialize() for section in sections]}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)
    

@main.route('/librarian/list_books_in_section', methods = ["GET"])
@librarian_token_required
def list_books_in_section_librarian(current_user):
    '''
    List all books in a section
    '''
    try:
        section = request.args.get('section')
        section = db_session.query(Sections).filter(Sections.section.ilike(section)).first()
        books = db_session.query(Books).join(Sections, Books.section == Sections.id).filter(Sections.section.ilike(section.section)).all()
        return make_response({"Books in section": [book.serialize() for book in books]}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)

@main.route('/librarian/list_borrowed_books_librarian', methods = ["GET"])
@librarian_token_required
def list_borrowed_books_librarian(current_user):
    '''
    List all borrowed books
    '''
    try:
        borrowed_books = db_session.query(BorrowedBooks).filter(BorrowedBooks.is_returned == False, BorrowedBooks.is_approved == True).all()
        return make_response({"Borrowed Books": [book.serialize() for book in borrowed_books]}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)
    

@main.route('/librarian/list_pending_approval_books', methods = ["GET"])
@librarian_token_required
def list_pending_approval_books(current_user):
    '''
    List all books pending approval
    '''
    try:
        pending_approval_books = db_session.query(BorrowedBooks).filter(BorrowedBooks.is_approved == False).all()
        return make_response({"Pending Approval Books": [book.serialize()
         for book in pending_approval_books]}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)
    

@main.route('/librarian/approve_book_borrow', methods = ["POST"])
@librarian_token_required
def approve_book_borrow(current_user):
    '''
    Approve a book borrow
    '''
    try:
        book_id = request.json['book_id']
        user_id = request.json['user_id']

        book = db_session.query(Books).filter(Books.id == book_id).first()
        
        if book.available_copies == 0:
            return make_response({"Status": "Book not available"}, 403)
        else:
            book.available_copies -= 1

        borrowed_book = db_session.query(BorrowedBooks).filter(BorrowedBooks.book_id == book_id, BorrowedBooks.user_id == user_id, BorrowedBooks.is_approved == False, BorrowedBooks.is_rejected == False).first()

        borrowed_book.is_approved = True
        borrowed_book.borrow_date = datetime.date.today()
        borrowed_book.scheduled_return_date = datetime.date.today() + datetime.timedelta(days=7)

        db_session.commit()

        return make_response({"Status": "Book borrow approved successfully"}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)


@main.route('/librarian/reject_book_borrow', methods = ["POST"])
@librarian_token_required
def reject_book_borrow(current_user):
    '''
    Reject a book borrow
    '''
    try:
        book_id = request.json['book_id']
        user_id = request.json['user_id']

        borrowed_book = db_session.query(BorrowedBooks).filter(BorrowedBooks.book_id == book_id, BorrowedBooks.user_id == user_id, BorrowedBooks.is_approved == False, BorrowedBooks.is_rejected == False).first()

        borrowed_book.is_rejected = True

        db_session.commit()

        return make_response({"Status": "Book borrow rejected successfully"}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)
    

@main.route('/librarian/revoke_borrowed_book', methods = ["POST"])
@librarian_token_required
def revoke_borrowed_book(current_user):
    '''
    Revoke a borrowed book
    '''
    try:
        book_id = request.json['book_id']
        user_id = request.json['user_id']

        borrowed_book = db_session.query(BorrowedBooks).filter(BorrowedBooks.book_id == book_id, BorrowedBooks.user_id == user_id, BorrowedBooks.is_approved == True, BorrowedBooks.is_rejected == False).first()

        borrowed_book.is_approved = False
        borrowed_book.is_revoked = True

        book = db_session.query(Books).filter(Books.id == book_id).first()
        book.available_copies += 1

        db_session.commit()

        return make_response({"Status": "Book borrow revoked successfully"}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)