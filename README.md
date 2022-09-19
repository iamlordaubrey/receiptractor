# Receipt Extractor

Description: An API that identifies blocks in a receipt and stores specific 
receipt information to a database

### Limitations
- Versioning wasn't implemented
- Database used is sqlite3

### Tech Stack
Built using Django and Django Rest framework. Libraries are kept as minimal as possible. 

Runtime: Python 3.10.5 (can be found in `.python-version` file)


## Install #
Creates a fresh virtual environment (called .venv) and installs requirements
```commandline
make setup
```

## Run #
Run a single instance of the wsgi server for local development

Install pip requirements
```commandline
make pip_sync
```

Run server
```commandline
make runserver
```

Run tests
```commandline
make runtest
```
