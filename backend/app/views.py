from flask import Blueprint, request, make_response
from .extensions import db_session
from .models import *
import jwt
import datetime
from dotenv import load_dotenv
import os
from .helpers import user_token_required, librarian_token_required
from werkzeug.utils import secure_filename
from sqlalchemy import or_, func
import uuid
from .tasks import send_monthly_report 
from .cache import cache

load_dotenv()

main = Blueprint('main', __name__)
secret_key = os.getenv('SECRET_KEY')
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')

def clear_cached_route(route):
    cache.delete_memoized(route)

@main.route('/check')
def check():
    send_monthly_report.delay()
    return 'OK', 200

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

            fetch_user = db_session.query(User).filter(User.email == email).all()

            if fetch_user is not None:
                # Verify the password
                if fetch_user[0].check_password(password):
                    # Password is correct, user is authenticated
                    fetch_user = fetch_user
                else:
                    # Password is incorrect
                    return make_response({"Status": "Invalid Credentials"}, 401)
            else:
                # User with given email not found
                return make_response({"Status": "Invalid Credentials"}, 401)


            # if not fetch_user:
            #     return make_response({"Status": "Invalid Credentials"}, 401)

            login_log = db_session.query(LoginLogs).filter(LoginLogs.user_id == fetch_user[0].id, LoginLogs.login_date == datetime.date.today()).first()

            if not login_log:
                l = LoginLogs(fetch_user[0].id)
                db_session.add(l)
                db_session.commit()

            fetch_user = fetch_user[0]
            token = jwt.encode({'username': fetch_user.username, 'email': fetch_user.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, secret_key)

            return make_response({"Status": "User login successful", "token": token, "user": fetch_user.username}, 200)
        
        except Exception as e:
            return make_response({'Error: ': str(e)}, 500)
        
    return make_response({"Status": 'Internal Server Error!'}, 500)


@main.route('/list_books', methods = ["GET"])
@user_token_required
@cache.memoize(timeout=30)
def list_books(current_user):
    '''
    List all books or search a book by title
    '''
    try:
        if request.args.get("title"):
            title = request.args.get("title")

            if request.args.get("section"):
                section = request.args.get("section")
                books = db_session.query(Books, Sections.section).join(Sections, Books.section == Sections.id).filter(Books.title.like("%" + title + "%"), Sections.section.ilike(section), Books.is_deleted == False).all()
            else:
                books = db_session.query(Books, Sections.section).join(Sections, Books.section == Sections.id).filter(Books.title.like("%" + title + "%")).all()

            # return make_response({"Books": [book.serialize() for book in books]}, 200)
        
        elif request.args.get("section"):
            section = request.args.get("section")
            books = db_session.query(Books, Sections.section).join(Sections, Books.section == Sections.id).filter(Sections.section.like("%"+section+"%"), Books.is_deleted == False).all()
            # return make_response({"Books": [book.serialize() for book in books]}, 200)

        else:
            books = db_session.query(Books, Sections.section).join(Sections, Books.section == Sections.id).filter(Books.is_deleted == False).all()
        
        borrowed_books = db_session.query(BorrowedBooks).filter(BorrowedBooks.user_id == current_user.id, BorrowedBooks.is_returned == False, BorrowedBooks.is_revoked == False, BorrowedBooks.is_rejected == False).all()
        borrowed_books = [book.book_id for book in borrowed_books]

        res = []
        for book, section in books:
            if book.id in borrowed_books:
                feedback = db_session.query(func.avg(Feedback.feedback_rating).label('average')).filter(Feedback.book_id == book.id).all()
                res.append({"id": book.id, "title": book.title, "author": book.author, "section": section, "description": book.description, "available_copies": book.available_copies, "is_borrowed": True, "image": book.image, "feedback": int(feedback[0][0]) if feedback[0][0] else 0})
            else:
                feedback = db_session.query(func.avg(Feedback.feedback_rating).label('average')).filter(Feedback.book_id == book.id).all()
                res.append({"id": book.id, "title": book.title, "author": book.author, "section": section, "description": book.description, "available_copies": book.available_copies, "is_borrowed": False, "image": book.image, "feedback": int(feedback[0][0]) if feedback[0][0] else 0})
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

        clear_cached_route(list_books)

        return make_response({"Status": "Book borrowed successfully"}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)


@main.route('/cancel_borrow_request', methods = ["DELETE"])
@user_token_required
def cancel_borrow_request(current_user):
    '''
    Cancel a borrow request
    '''
    try:
        req_id = request.json['req_id']
        borrowed_book = db_session.query(BorrowedBooks).filter(BorrowedBooks.id == req_id, BorrowedBooks.user_id == current_user.id, BorrowedBooks.is_approved == False, BorrowedBooks.is_rejected == False).first()

        if not borrowed_book:
            return make_response({"Status": "Book not borrowed by you"}, 403)

        db_session.delete(borrowed_book)
        db_session.commit()

        clear_cached_route(list_approval_pending_books)

        return make_response({"Status": "Borrow request cancelled successfully"}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)


@main.route('/return_book', methods = ["POST"])
@user_token_required
def return_book(current_user):
    '''
    Return a book
    '''
    try:
        req_id = request.json['req_id']
        borrowed_book = db_session.query(BorrowedBooks).filter(BorrowedBooks.id == req_id, BorrowedBooks.user_id == current_user.id, BorrowedBooks.is_returned == False, BorrowedBooks.is_approved == True, BorrowedBooks.is_revoked == False).first()

        if not borrowed_book:
            return make_response({"Status": "Book not borrowed by you"}, 403)

        borrowed_book.is_returned = True
        borrowed_book.actual_return_date = datetime.date.today()

        book = db_session.query(Books).filter(Books.id == borrowed_book.book_id).first()
        book.available_copies += 1

        db_session.commit()
        clear_cached_route(list_borrowed_books)
        clear_cached_route(list_returned_books)

        return make_response({"Status": "Book returned successfully"}, 200)
    except Exception as e:
        print(str(e))
        return make_response({"Status": str(e)}, 500)


@main.route('/list_approval_pending_books', methods = ["GET"])
@user_token_required
@cache.memoize(timeout=30)
def list_approval_pending_books(current_user):
    '''
    List all books pending approval
    '''
    try:
        pending_approval_books = db_session.query(BorrowedBooks, Books, Sections).\
            join(Books, BorrowedBooks.book_id == Books.id).\
            join(Sections, Books.section == Sections.id).\
            filter(
                BorrowedBooks.user_id == current_user.id,
                BorrowedBooks.is_approved == False,
                BorrowedBooks.is_rejected == False
            ).all()

        res = []
        for book, book_details, section in pending_approval_books:
            res.append({"req_id": book.id, "title": book_details.title, "author": book_details.author, "section": section.section})
        return make_response({"Books": res}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)


@main.route('/list_borrowed_books', methods = ["GET"])
@user_token_required
@cache.memoize(timeout=10)
def list_borrowed_books(current_user):
    '''
    List all borrowed books
    '''
    try:      
        borrowed_books = db_session.query(BorrowedBooks, Books, Sections).\
            join(Books, BorrowedBooks.book_id == Books.id).\
            join(Sections, Books.section == Sections.id).\
            filter(
                BorrowedBooks.user_id == current_user.id,
                BorrowedBooks.is_approved == True,
                BorrowedBooks.is_revoked == False,
                BorrowedBooks.is_returned == False
            ).all()
        res = []
        for book, book_details, section in borrowed_books:
            res.append({"req_id": book.id, "title": book_details.title, "author": book_details.author, "section": section.section, "scheduled_return_date": book.scheduled_return_date, "book_id": book_details.id})

        return make_response({"Books": res}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)
    

@main.route('/list_returned_books', methods = ["GET"])
@user_token_required
@cache.memoize(timeout=30)
def list_returned_books(current_user):
    '''
    List all returned books
    '''
    try:
        returned_books = db_session.query(BorrowedBooks, Books, Sections).\
            join(Books, BorrowedBooks.book_id == Books.id).\
            join(Sections, Books.section == Sections.id).\
            filter(
                BorrowedBooks.user_id == current_user.id,
                or_(BorrowedBooks.is_returned == True, BorrowedBooks.is_revoked == True),
                Books.is_deleted == False
            ).all()
        res = []
        for book, book_details, section in returned_books:

            feedback = db_session.query(Feedback).filter(Feedback.user_id == current_user.id, Feedback.book_id == book_details.id).first()

            res.append({"book_id":book_details.id, "req_id": book.id, "title": book_details.title, "author": book_details.author, "section": section.section, "actual_return_date": book.actual_return_date, "feedback": feedback.feedback_rating if feedback else 0})
        return make_response({"Books": res}, 200)
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

        exising_feedback = db_session.query(Feedback).filter(Feedback.user_id == current_user.id, Feedback.book_id == book_id).first()

        if exising_feedback:
            exising_feedback.feedback_rating = feedback
        else:
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
    

@main.route('/fetch_stats', methods = ["GET"])
@user_token_required
@cache.memoize(timeout=60)
def fetch_stats(current_user):
    '''
    Fetch stats for a student (user)
    '''
    try:
        monthly_counts = db_session.query(
            func.strftime('%Y-%m', BorrowedBooks.borrow_date).label('month'),
            func.count().label('book_count')
        ).filter(BorrowedBooks.user_id == current_user.id, BorrowedBooks.is_approved==True)\
        .group_by(func.strftime('%Y-%m', BorrowedBooks.borrow_date)).all()

        borrowed_books_count_by_section = db_session.query(Sections.section, func.count(BorrowedBooks.id)).\
                                    join(Books, Sections.id == Books.section).\
                                    join(BorrowedBooks, Books.id == BorrowedBooks.book_id).\
                                    filter(BorrowedBooks.is_approved == True, BorrowedBooks.user_id == current_user.id).\
                                    group_by(Sections.section).all()

        bar_months = [month for month, count in monthly_counts]
        bar_counts = [count for month, count in monthly_counts]
        
        pie_sections = [section for section, count in borrowed_books_count_by_section]
        pie_counts = [count for section, count in borrowed_books_count_by_section]

        return make_response({"bar_months": bar_months, "bar_counts": bar_counts, "pie_sections": pie_sections, "pie_counts": pie_counts}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)


@main.route('/fetch_book/<int:book_id>', methods = ["GET"])
@user_token_required
@cache.memoize(timeout=60)
def view_book(current_user, book_id):
    '''
    Fetch a book's data
    '''
    try:
        is_borrowed = db_session.query(BorrowedBooks).filter(BorrowedBooks.user_id == current_user.id, BorrowedBooks.book_id == book_id, BorrowedBooks.is_approved == True, BorrowedBooks.is_returned == False, BorrowedBooks.is_revoked == False).first()

        if not is_borrowed:
            return make_response({"Status": "Unauthiorized access to book"}, 403)

        book = db_session.query(Books).filter(Books.id == book_id).first()

        return make_response({"Book": book.serialize()}, 200)
        
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

            fetch_librarian = db_session.query(Librarian).filter(Librarian.username == username).all()

            if fetch_librarian is not None:
                # Verify the password
                if len(fetch_librarian) and fetch_librarian[0].check_password(password):
                    # Password is correct, user is authenticated
                    fetch_librarian = fetch_librarian
                else:
                    # Password is incorrect
                    return make_response({"Status": "Invalid Credentials"}, 401)
            else:
                # User with given email not found
                return make_response({"Status": "Invalid Credentials"}, 401)

            # if not fetch_librarian:
            #     return make_response({"Status": "Invalid Credentials"}, 401)

            fetch_librarian = fetch_librarian[0]
            token = jwt.encode({'username': fetch_librarian.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, secret_key)

            return make_response({"Status": "Librarian login successful", "token": token, "username": fetch_librarian.username}, 200)
        
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
        clear_cached_route(list_sections)

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
        title = request.form['title']
        author = request.form['author']
        section = request.form['section']
        description = request.form['description']
        available_copies = request.form['available_copies']
        content = request.form['content']

        # Get the uploaded file
        uploaded_file = request.files['picture']

        section = db_session.query(Sections).filter(Sections.section.ilike(section)).first()
        if not section:
            return make_response({"Status": "Section not found"}, 404)

        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            unique_filename = str(uuid.uuid4()) + '_' + filename
            upload_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            
            # Save the file to the designated folder
            uploaded_file.save(upload_path)

            book = Books(title, author, section.id, description, available_copies, image=unique_filename, content=content)

        else:
            book = Books(title, author, section.id, description, available_copies, content=content)

        db_session.add(book)
        db_session.commit()

        clear_cached_route(list_books_in_section_librarian)

        return make_response({"Status": "Book added successfully"}, 200)
    except Exception as e:
        print(str(e))
        return make_response({"Status": str(e)}, 500)
    

@main.route('/librarian/delete_book', methods = ["DELETE"])
@librarian_token_required
def delete_book(current_user):
    '''
    Delete a book
    '''
    try:
        book_id = request.json['book_id']

        book = db_session.query(Books).filter(Books.id == book_id).first()

        if not book:
            return make_response({"Status": "Book not found"}, 404)

        book.is_deleted = True

        borrow_books = db_session.query(BorrowedBooks).filter(BorrowedBooks.book_id == book_id, or_(BorrowedBooks.is_approved == True, (BorrowedBooks.is_approved == False and BorrowedBooks.is_rejected == False)), BorrowedBooks.is_returned == False, BorrowedBooks.is_revoked == False).all()

        for b in borrow_books:
            if b.is_approved == False:
                b.is_rejected = True
                continue
            else:
                b.is_revoked = True
                b.is_returned = True
                b.actual_return_date = datetime.date.today()

        db_session.commit()
        clear_cached_route(list_books_in_section_librarian)

        return make_response({"Status": "Book deleted successfully"}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)


@main.route('/librarian/restore_book', methods = ["POST"])
@librarian_token_required
def restore_book(current_user):
    '''
    Restore a book
    '''
    try:
        book_id = request.json['book_id']

        book = db_session.query(Books).filter(Books.id == book_id).first()

        if not book:
            return make_response({"Status": "Book not found"}, 404)

        book.is_deleted = False

        db_session.commit()
        clear_cached_route(list_books_in_section_librarian)

        return make_response({"Status": "Book restored successfully"}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)


@main.route('/librarian/get_edit_book', methods = ["GET"])
@librarian_token_required
def get_edit_book(current_user):
    '''
    Get a book to edit
    '''
    try:
        book_id = request.args.get('book_id')
        book = db_session.query(Books).filter(Books.id == book_id).first()
        section_name = db_session.query(Sections).filter(Sections.id == book.section).first()
        if not book:
            return make_response({"Status": "Book not found"}, 404)

        return make_response({"book": book.serialize(), "section": section_name.section}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)


@main.route('/librarian/edit_book', methods = ["PUT"])
@librarian_token_required
def edit_book(current_user):
    '''
    Edit a book
    '''
    try:
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        available_copies = request.form['available_copies']
        book_id = request.form['book_id']
        content = request.form['content']

        book = db_session.query(Books).filter(Books.id == book_id).first()

        if not book:
            return make_response({"Status": "Book not found"}, 404)

        try:
            # Get the uploaded file
            uploaded_file = request.files['picture']

            
            if uploaded_file:
                filename = secure_filename(uploaded_file.filename)
                unique_filename = str(uuid.uuid4()) + '_' + filename
                upload_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                
                # Save the file to the designated folder
                uploaded_file.save(upload_path)

                book.image = unique_filename
        except:
            pass

        book.title = title
        book.author = author
        book.description = description
        book.available_copies = available_copies
        book.content = content

        db_session.commit()
        clear_cached_route(list_books_in_section_librarian)

        return make_response({"Status": "Book edited successfully"}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)


@main.route('/librarian/list_sections', methods = ["GET"])
@librarian_token_required
@cache.memoize(timeout=30)
def list_sections(current_user):
    '''
    List all sections
    '''
    try:
        sections = db_session.query(Sections).all()
        return make_response({"Sections": [section.serialize() for section in sections]}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)


@main.route('/librarian/edit_section', methods = ["POST"])
@librarian_token_required
def edit_section(current_user):
    '''
    Edit a section
    '''
    try:
        section_id = request.json['section_id']
        section = request.json['section']
        description = request.json['description']

        s = db_session.query(Sections).filter(Sections.id == section_id).first()

        if not s:
            return make_response({"Status": "Section not found"}, 404)

        s.section = section
        s.description = description

        db_session.commit()
        clear_cached_route(list_sections)

        return make_response({"Status": "Section edited successfully"}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)
    

@main.route('/librarian/delete_section', methods = ["DELETE"])
@librarian_token_required
def delete_section(current_user):
    '''
    Delete a section
    '''
    try:
        section_id = request.json['section_id']

        s = db_session.query(Sections).filter(Sections.id == section_id).first()

        if not s:
            return make_response({"Status": "Section not found"}, 404)

        books = db_session.query(Books).filter(Books.section == section_id).all()

        for book in books:
            book.is_deleted = True
            borrow_books = db_session.query(BorrowedBooks).filter(BorrowedBooks.book_id == book.id, or_(BorrowedBooks.is_approved == True, (BorrowedBooks.is_approved == False and BorrowedBooks.is_rejected == False)), BorrowedBooks.is_returned == False, BorrowedBooks.is_revoked == False).all()

            for b in borrow_books:
                if b.is_approved == False:
                    b.is_rejected = True
                    continue
                else:
                    b.is_revoked = True
                    b.is_returned = True
                    b.actual_return_date = datetime.date.today()

        s.is_deleted = True
        db_session.commit()
        clear_cached_route(list_sections)

        return make_response({"Status": "Section deleted successfully"}, 200)
    except Exception as e:
        print(str(e))
        return make_response({"Status": str(e)}, 500)


@main.route('/librarian/restore_section', methods = ["POST"])
@librarian_token_required
def restore_section(current_user):
    '''
    Restore a section
    '''
    try:
        section_id = request.json['section_id']

        s = db_session.query(Sections).filter(Sections.id == section_id).first()

        if not s:
            return make_response({"Status": "Section not found"}, 404)

        s.is_deleted = False

        books = db_session.query(Books).filter(Books.section == section_id).all()
        for book in books:
            book.is_deleted = False

        db_session.commit()
        clear_cached_route(list_sections)

        return make_response({"Status": "Section restored successfully"}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)


@main.route('/librarian/list_books_in_section', methods = ["GET"])
@librarian_token_required
# @cache.memoize(timeout=30)
def list_books_in_section_librarian(current_user):
    '''
    List all books in a section
    '''
    try:
        section = request.args.get('section')
        books = db_session.query(Books).join(Sections, Books.section == Sections.id).filter(Sections.section == section).all()
        
        res = []
        for book in books:
            borrowed_by = db_session.query(BorrowedBooks, User).join(User, BorrowedBooks.user_id == User.id).filter(BorrowedBooks.book_id == book.id, BorrowedBooks.is_approved == True, BorrowedBooks.is_returned == False, BorrowedBooks.is_revoked == False).all()
            borrowed_by = [user.email for book, user in borrowed_by]
            res.append({"title": book.title, "author": book.author, "available_copies": book.available_copies, "borrowed_by": borrowed_by, "is_deleted": book.is_deleted, "book_id": book.id})

        return make_response({"books": res}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)

@main.route('/librarian/list_borrowed_books_librarian', methods = ["GET"])
@librarian_token_required
@cache.memoize(timeout=30)
def list_borrowed_books_librarian(current_user):
    '''
    List all borrowed books
    '''
    try:
        borrowed_books = db_session.query(User.email, Books.title, BorrowedBooks.id, BorrowedBooks.scheduled_return_date, Books.id, User.id)\
            .join(BorrowedBooks, BorrowedBooks.user_id == User.id)\
            .join(Books, BorrowedBooks.book_id == Books.id)\
            .filter(BorrowedBooks.is_approved == True, BorrowedBooks.is_returned == False, BorrowedBooks.is_revoked == False).all()

        res = []
        for user, book, req_id, return_date, book_id, user_id in borrowed_books:
            res.append({"email": user, "title": book, "req_id": req_id, "scheduled_return_date": return_date, "book_id": book_id, "user_id": user_id})
        
        return make_response({"Books": res}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)
    

@main.route('/librarian/list_pending_approval_books', methods = ["GET"])
@librarian_token_required
@cache.memoize(timeout=30)
def list_pending_approval_books(current_user):
    '''
    List all books pending approval
    '''
    try:
        pending_approval_books = db_session.query(User.email, Books.title, BorrowedBooks.id, Books.id, User.id)\
            .join(BorrowedBooks, BorrowedBooks.user_id == User.id)\
            .join(Books, BorrowedBooks.book_id == Books.id)\
            .filter(BorrowedBooks.is_approved == False, BorrowedBooks.is_rejected == False).all()
        res = []
        for user, book, req_id, book_id, user_id in pending_approval_books:
            res.append({"email": user, "title": book, "req_id": req_id, "book_id": book_id, "user_id": user_id})
        return make_response({"Books": res}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)
    

@main.route('/librarian/approve_book_borrow', methods = ["POST"])
@librarian_token_required
def approve_book_borrow(current_user):
    '''
    Approve a book borrow
    '''
    try:
        req_id = request.json['req_id']
        user_id = request.json['user_id']
        book_id = request.json['book_id']

        user_already_borrowed_book = db_session.query(BorrowedBooks).filter(BorrowedBooks.user_id == user_id, BorrowedBooks.is_approved == True, BorrowedBooks.is_returned == False, BorrowedBooks.is_revoked == False).count()

        if user_already_borrowed_book >= 5:
            return make_response({"Status": "User has already borrowed 5 books"}, 403)

        book = db_session.query(Books).filter(Books.id == book_id).first()
        
        if book.available_copies == 0:
            return make_response({"Status": "Book not available"}, 404)
        else:
            book.available_copies -= 1

        borrowed_book = db_session.query(BorrowedBooks).filter(BorrowedBooks.id == req_id).first()

        borrowed_book.is_approved = True
        borrowed_book.borrow_date = datetime.date.today()
        borrowed_book.scheduled_return_date = datetime.date.today() + datetime.timedelta(days=7)

        db_session.commit()
        clear_cached_route(list_pending_approval_books)
        clear_cached_route(list_borrowed_books_librarian)

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
        req_id = request.json['req_id']

        # borrowed_book = db_session.query(BorrowedBooks).filter(BorrowedBooks.req_id == req_id, BorrowedBooks.is_approved == False, BorrowedBooks.is_rejected == False).first()
        borrowed_book = db_session.query(BorrowedBooks).filter(BorrowedBooks.id == req_id).first()

        borrowed_book.is_rejected = True

        db_session.commit()
        clear_cached_route(list_pending_approval_books)

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
        req_id = request.json['req_id']

        borrowed_book = db_session.query(BorrowedBooks).filter(BorrowedBooks.id == req_id).first()

        borrowed_book.is_revoked = True
        borrowed_book.is_returned = True
        borrowed_book.actual_return_date = datetime.date.today()

        book = db_session.query(Books).filter(Books.id == book_id).first()
        book.available_copies += 1

        db_session.commit()
        clear_cached_route(list_borrowed_books_librarian)

        return make_response({"Status": "Borrowed Book revoked successfully"}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)


@main.route('/librarian/fetch_stats', methods = ["GET"])
@librarian_token_required
@cache.memoize(timeout=60)
def librarian_fetch_stats(current_user):
    '''
    Fetch stats for a of all users
    '''
    try:
        monthly_counts = db_session.query(
            func.strftime('%Y-%m', BorrowedBooks.borrow_date).label('month'),
            func.count().label('book_count')
        ).filter(BorrowedBooks.is_approved==True)\
        .group_by(func.strftime('%Y-%m', BorrowedBooks.borrow_date)).all()

        borrowed_books_count_by_section = db_session.query(Sections.section, func.count(BorrowedBooks.id)).\
                                    join(Books, Sections.id == Books.section).\
                                    join(BorrowedBooks, Books.id == BorrowedBooks.book_id).\
                                    filter(BorrowedBooks.is_approved == True).\
                                    group_by(Sections.section).all()
        
        print(borrowed_books_count_by_section)

        bar_months = [month for month, count in monthly_counts]
        bar_counts = [count for month, count in monthly_counts]
        
        pie_sections = [section for section, count in borrowed_books_count_by_section]
        pie_counts = [count for section, count in borrowed_books_count_by_section]

        return make_response({"bar_months": bar_months, "bar_counts": bar_counts, "pie_sections": pie_sections, "pie_counts": pie_counts}, 200)
    except Exception as e:
        return make_response({"Status": str(e)}, 500)