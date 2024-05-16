# Run the project

1. Replace DB_PATH and UPLOAD_FOLDER in .env file with your folder path
```
DB_PATH=<your-project-folder-path>/backend/db
UPLOAD_FOLDER=<your-project-folder-path>/frontend/public/images
```
2. Running the python backend -
Open a terminal
```
cd backend
```
```
pipenv install
pipenv shell
```
To run the backend server -
```
python main.py --debug
```
3. Running node (vuejs) frontend -
Open a new terminal -
```
cd frontend
```
```
npm install .
npm run dev
```

4. Setting up celery beat - 
Open a new terminal -
```
cd backend
```
```
pipenv shell

// to setup celery beat
celery -A main.celery beat --max-interval 1 -l info 
```

5. Running the celery worker - 
Open a new terminal -
```
cd backend
```
```
pipenv shell

// to run celery
celery -A main.celery worker -l info
```

6. MailHog service setup and execution
```
sudo apt-get -y install golang-go
go install github.com/mailhog/MailHog@latest
~/go/bin/MailHog
```
