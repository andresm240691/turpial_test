# TURPIAL TEST #

### Requirements ###

* Python 3.8.5
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
    ### make a virtual enviroment ###
    virtualenv -p python3 venv
    source venv/bn/activate
    
    ### Install the requirements ###
    pip install -r requirements.txt

### Deploy Application ###
    
    ### Migrate Database ###
    python manage.py makemigrations
    python manage.py migrate

    ### Load Fixtures ###
    python manage.py pokemon
    python manage.py area
    python manage.py region
    
    ### Create User ####
    python manage.py createsuperuser
        - username: admin
        - password: admin

    ## Run the project
    python manage.py runserver 0.0.0.0:8000

### Note ### 
    
    The request_test.json file contains the 
    collection of calls to the api




    
