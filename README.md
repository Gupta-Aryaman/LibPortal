# LibPortal
A multi-user Library Management Application with a single Librarian and multiple users/students was created using Vue, JavaScript framework in the frontend, and SQLite DB and flask in the backend. The web app shall support all the features of similar Library Management apps like Amazon e-books.

# Demo
Check out the application demo [here](https://youtu.be/olCY4cIEKSM).

# Technologies Used
* Vue – JavaScript based Progressive web framework
* Bootstrap – HTML and CSS styling
* Flask – Python based web framework
* Celery – For automatic job scheduling and execution
* Redis - Works in tandem with celery to store and execute jobs
* Mailhog - To simulate an SMTP server to send emails
* Jinja2 – Template engine for forma ng emails
* SQLite – for data storage
* SQLAlchemy – ORM mapper to manage data in python

# DB Schema
![image](https://github.com/user-attachments/assets/0f76f98b-6ee6-49d8-95ce-08144bce6e06)

# Core Features
### General
1. Application Frontend is implemented in vue3 framework as a Single Page Application
2. Application Backend is implemented using Flask framework
3. Multi Users, such as Librarian and students, are supported
4. General User login is present and uses Role-based access control (RBAC) to login a user
5. Librarian can also login using the same form
6. JWT based Token Authentication is used

### General User
1. User can request, read, return e-books
2. A user can access a book for only 7 days, after that the book is automatically revoked
3. A user can issue a maximum of 5 books at a time
4. A rating by the user can be given to each already read book

### Librarian
1. Only 1 librarian exists in the application
2. Librarian can add new sections/e-books, edit existing sections/e-books, delete sections/e-books issue/revoke access for a book

### Cron Jobs
1. A daily reminder is sent to all the users, via email, who have not logged in our application on each day
2. A monthly activity report is also sent to each user, via email, showing them what all books they read in that month


# Setup Guide
Follow these steps to set up LibPortal on your local machine:

### Installation Steps
```
git clone https://github.com/Gupta-Aryaman/LibPortal.git
cd LibPortal
```

1. Replace DB_PATH and UPLOAD_FOLDER in .env file with your folder path
```
DB_PATH=<your-project-folder-path>/backend/db
UPLOAD_FOLDER=<your-project-folder-path>/frontend/public/images
```
### Running the python backend
2. Open a terminal
```
cd backend
```
```
pipenv install
pipenv shell
```
3. To run the backend server -
```
python main.py --debug
```
### Running node (vuejs) frontend
2. Open a new terminal -
```
cd frontend
```
```
npm install .
npm run dev
```

### Setting up celery beat
2. Open a new terminal -
```
cd backend
```
```
pipenv shell

// to setup celery beat
celery -A main.celery beat --max-interval 1 -l info 
```

3. Running the celery worker <br>
Open a new terminal -
```
cd backend
```
```
pipenv shell

// to run celery
celery -A main.celery worker -l info
```

### MailHog service setup and execution
```
sudo apt-get -y install golang-go
go install github.com/mailhog/MailHog@latest
~/go/bin/MailHog
```
