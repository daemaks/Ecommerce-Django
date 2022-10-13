![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django)

## Quick start
1. Install [PyPi](https://pypi.org/) packages:

```python
pip install -r requirements.txt
```
2. In base direcory create __.env__ file and put you Django secret key in this

3. Make migrate:
```python
#Step 1
python manage.py makemigrations
#Step 2
python manage.py migrate
```

4. Start the server:
```python
py manage.py runserver
```
