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
