# Lavanda API

## Instalation

Download and install python (3.5)

Download and install mongo (3.6)

Git clone this project: `github.com/jaconsta/lavanda_api` and 

```
cd lavanda_api
```

Set the virtual environment for the project. And activate (Windows / Unix different)

```
python --env venv

venv/Scripts/Activate # Windows
source venv/bin/activate  # Unix
```

Install dependencies. 

```
pip install -r requirements.txt
```

## Run

Run Mongo on port `32768` (Default first port assignment from Docker container run)

Run the application

```
cd src
python main.py
```

Access the application api-docs: `http://localhost:5000/apidocs`
 