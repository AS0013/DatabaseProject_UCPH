# Project Catalogue Website

This Project was made as part of the 2024 Databases and Information Systems ""DIS" course at the University of Copenhagen.

The Web-App is made using python and flask and uses postgresql for the database.
The Database itself is made using a "scraper" on the futhark site: "https://futhark-lang.org/publications.html#selected-student-projects"
the scraper itself can be found in the scraping.py file.

# Concept 

The purpose of the project is to make it easier and more intuitive to search and find previous student's Bachelor and Master's theses. This is achieved by allowing the user to search using keywords and filters like year of publication, degree level and the specific university. We wanted to leave open the possibility of the catalogue being expanded to cover various danish universities. When the user has found a project that interests them, clicking on the project title will take them to a "Project Overview" page where various info about the project can be found, a link to a PDF file will also be attached.

Additionally we have added an "Add Project" submission page where users would be able to upload their Bachelor and Master's theses to the database. Currently this "upload" means to enter a link to a pdf file, but conceptually this could -if hosted on a service like AWS or Azure- be integrated with a file storage solution, allowing for files to be uploaded to the site and stored internally.

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
2) Create a new database named 'DIS_test'.
3) Update the database configuration in 'database_setup.py' (line 6) and 'app.py' (line 8) with your PostgreSQL information.  

## database_setup.py configs to perform in line 6
```bash
- conn = psycopg2.connect(host="localhost", database="DIS_Test", user="your_username", password="your_password", port=5432)
```
## app.py configs to perform in line 8
```bash
- app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/DIS_Test'
```
## how to Run 
1)  First, set up the database by running 'database_setup.py', you can run it by entering  ```bash  python database_setup.py ```
    - This script will create the necessary tables and fill the database with initial data.
2) Start the flask application by running 'app.py': you can run it by entering ```bash py app.py ```
    - The application should start running and you should be able to see it on http://127.0.0.1:5000/

## How to use the website:
At the front page of the project catalog, you are able to view all
projects in the database as well as use a selection of filters: you can
search for a project by its title and author name; you can filter by level,
that is, whether it is a bachelor's or a master's thesis; you can filter
by year written; you can filter by university.

Upon clicking on a project title, you are taken to its project page, 
where it is possible to view all information about this project (its 
title, author(s), level, and main supervisor) as well as project
attachments, the project pdf specifically.

It is also possible to add another project to the database in the "Add
Project" page: simply enter a title, author(s), supervisor, year, select
a degree and university, and include a link to the pdf. Note that if
multiple authors need to be added, these should be comma-separated.
Upon submission of a project (with legal inputs), it should be visible
in the front page.

Finally, we have included an about page with a description of the project
as well as the contact information of the developers.

## Conclusion