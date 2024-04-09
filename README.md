using pipenv for environment maintenance
```
pipenv shell //activate shell
```
```
pipenv install *package_name*
```
```
flask run --debug //for autoreload
flask run // for normal
```

```
//backend
pipenv shell //activate shell
python main.py
celery -A main.celery worker -l info

//frontend
npm run dev
```


```
// to setup celery beat
celery -A main.celery beat --max-interval 1 -l info 

// to run celery
celery -A main.celery worker -l info
```

MailHog service setup and execution
```
sudo apt-get -y install golang-go
go install github.com/mailhog/MailHog@latest
~/go/bin/MailHog
```