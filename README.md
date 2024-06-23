# FastAPI Structure Demo

### Project structure

The project code base is mainly located within the `src` folder. This folder is divided in:

- `apps` - containing all app module like auth, user,...
- `commons` - containing common module for the project like configs, constant, etc.
- `libs` - containing external libs like sendmail, storage,...
- `static` - containing all static files and template html

```
.
├── src
│   ├── apps                                  # Contain modules
│   │   ├── auth                              # Module auth
│   │   │   │
│   │   │   ├── auth_schema.py                # Include all request dto to validate and response data type
│   │   │   ├── auth_controller.py            # Controller
│   │   │   ├── auth_service.py               # Service
│   │   │   
│   │   │
│   │   └── __init__.py                       # List all app's routers
│   │
│   └── commons                               # Contains all shared datas, functions, classes
│   │   │
│   │   ├── configs                           # Configs
│   │   ├── constants                         # Constants
│   │   ├── database                          # Migration files and base repository
│   │   ├── dtos                              # Dtos
│   │   ├── middlewares                       # Middlewares
│   │   ├── utils                             # Utility code base
│   │   ├── models                            # Entity models
│   │   ├── services                          # Declare base service
│   │   └── utils                             # Utilities function
│   │
│   └── main.py                               # Register middlewares, logger, events and bootstrap server


```

## Editor

- Visual studio code
- Extension: https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter

## Local Run

### Prepare env and package

- Create file `.env.dev` simular with file `.env.example`
- Replace environment key with your environment value
- Install packages using `pipenv`

```
# pyenv install 3.12
# pyenv shell 3.12 

# pipenv shell
# pipenv install
```

- Or install packages using requirements

```
# python3 -m venv venv
# source venv/bin/activate
# pip3 install -r requirements.txt
```

### Linting and format

- Run lint
```
# pylint src
```
- Format all code
```
# black .
```


### Setup Database

- Install posgresql
- Run migration if folder `migrations` is already exist

```
# alembic upgrade head 
```

- If you want to create new migration file

```
# alembic revision -m "[Message]"
# alembic upgrade head 
```

- For new project setup, run the following command

```
# alembic init -c alembic.ini
# alembic revision -m "[Message]"
# alembic upgrade head
```

- If you want upgrade/downgrade a migration file

```
# alembic upgrade/downgrade [revisionId]
```

### Run App

- Run FastAPI App

```
# export APP_ENV=dev
# uvicorn src.main:app --host 0.0.0.0 --reload --log-level debug
```

### Swagger UI

```
# http://{{hostname}}/docs
```

## Docker Run
### Prepare env

- Create file `.env.dev` simular with file `.env.example`
- Replace environment key with your environment value

### Build image and run container
- Build image
```
# docker compose --env-file {env-file-name} -f docker-compose.yml build
```

- Run container
```
# docker compose --env-file {env-file-name} -f docker-compose.yml up
```

### To run migration inside docker container
```
# docker ps  -> to get api container name
# docker exec {api-container-name}  python3 -m alembic upgrade head
```

### To run backup database manualy 
- Make sure that you currently run docker container
```
# chmod +x ./scripts/backup_db.sh 
# ./scripts/backup_db.sh [env]
```

### To schedule backup database
- Make sure that you currently run docker container
```
# chmod +x ./scripts/backup_db.sh 
# crontab -e

Then add an entry to schedule run script: 0 15 * * * path/to/the/backup_db.sh [env]
It means the script will run on 15:00 every day

```