# TURPIAL TEST #

### Requirements ###

* Python 3.8.10
* Postgres 12


### Enviroments ###

    # Database Postgres SQL 
    export DB_NAME=turpial_dev_db2
    export DB_USER=admin
    export DB_PASSWORD=admin
    export DB_HOST=localhost
    export DB_PORT=5433

    # Configuration
    export ALLOWED_HOSTS=*
    export FIXTURE_ROUTE='<str_path>/turpial_test/turpial_test/fixtures' 
    # Example /home/andres/Projects/turpial_test/turpial_test/fixtures'

### Installation ###
    
    pip install -r requirements.txt

### Deploy Application ###

    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

### Load Fixtures ###

    python manage.py pokemons
    python manage.py area
    
