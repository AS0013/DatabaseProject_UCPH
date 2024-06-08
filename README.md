# Project Catalogue Website

This Project was made as part of the 2024 Databases and Information Systems ""DIS" cousre at the University of Copenhagen

## Required Packages 

To run this project, you need the following Pythong Packages:

- Flask
- Flask-SQLAlchemy
- psycopg2

you can install them using pip:

```bash
pip install Flask Flask-SQLAlchemy psycopg2
```
## Database Setup in pgAdmin
1) Open pgAdmin and connect to you PostgreSQL server.
2) Create a new databade named 'DIS_test'.
3) Update the database configuration in 'database_setup.py' (line 6) and 'app.py' (line 8) with your PostgreSQL information.  

# database_setup.py configs to perform in line 6
- conn = psycopg2.connect(host="localhost", database="DIS_Test", user="your_username", password="your_password", port=5432)

# app.py configs to perform in line 8
- app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/DIS_Test'

## how to Run 
1)  First, set up the database by running 'database_setup.py', you can run it by entering    python database_setup.py
    - This script will create the necessary tables and fill the database with initial data.
2) Start the flask application by running 'app.py': you can run it by entering py app.py
    - The application should start running and you should be able to see it on http://127.0.0.1:5000/

## How to use the website:


## Conclusion