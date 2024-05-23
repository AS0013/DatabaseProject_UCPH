import psycopg2
import sqlalchemy


# remember to change the password to your own password and the database to your own database name
conn = psycopg2.connect(host="localhost", database="DIS_Test", user="postgres", password="Choudhary6583", port=5432)
conn.set_client_encoding('UNICODE')

cur = conn.cursor()

# create Table for Authors from the small_diku_authors.csv



cur.execute('''
            DROP TABLE IF EXISTS writes;
''')

cur.execute('''
            
            DROP TABLE IF EXISTS supervises;
''')


cur.execute('''
            DROP TABLE IF EXISTS author;
''')


cur.execute('''
            DROP TABLE IF EXISTS project;
''')

cur.execute('''
            DROP TABLE IF EXISTS supervisor;
''')

cur.execute('''
            CREATE TABLE IF NOT EXISTS author ( 
                name VARCHAR(255),
                id int,
                PRIMARY KEY (id));
''')

# create Table for Projects from the small_diku_projects.csv

cur.execute('''
CREATE TABLE IF NOT EXISTS project (
            title VARCHAR(255),
            degree VARCHAR(255),
            pdf VARCHAR(255),
            year int,
            university VARCHAR(255),
            id int,
            PRIMARY KEY (id));
''')

# create Table for supervisors from the small_diku_supervisors.csv

cur.execute('''
CREATE TABLE IF NOT EXISTS supervisor (
            name VARCHAR(255),
            id int,
            PRIMARY KEY (id));
''')


# fill in the data author,id from the small_diku_authors.csv

with open('small_diku_authors.csv', 'r') as f:
    next(f)
    cur.copy_from(f, 'author', sep=',')


#  fill in the data projects from the small_diku_projects.csv

with open('small_diku_projects.csv', 'r') as f:
    next(f)
    cur.copy_from(f, 'project', sep=',')

# fill in the data supervisors from the small_diku_supervisors.csv

with open('small_diku_supervisors.csv', 'r') as f:
    next(f)
    cur.copy_from(f, 'supervisor', sep=',')

# create Table for Author-Writes-Projects that connects the authors and projects

cur.execute('''
CREATE TABLE IF NOT EXISTS writes (
            author_id int,
            project_id int,
            PRIMARY KEY (author_id, project_id),
            FOREIGN KEY (author_id) REFERENCES author (id),
            FOREIGN KEY (project_id) REFERENCES project (id)
            );
''') 

# create Table for Supervisor-Supervises-Projects that connects the supervisors and projects

cur.execute('''
CREATE TABLE IF NOT EXISTS supervises (
            supervisor_id int,
            project_id int,
            PRIMARY KEY (supervisor_id, project_id),
            FOREIGN KEY (supervisor_id) REFERENCES supervisor (id),
            FOREIGN KEY (project_id) REFERENCES project (id)
            );
''')


# inserting data into the writes table

cur.execute('''
 INSERT INTO writes (author_id, project_id) VALUES
            (1,1),
            (2,1),
            (3,2),
            (4,2),
            (5,3),
            (6,3),
            (7,4),
            (8,5),
            (9,6),
            (10,7),
            (11,8),
            (12,9),
            (13,9),
            (14,10),
            (15,11),
            (16,12),
            (17,12),
            (14,13),
            (18,14),
            (19,15),
            (20,16),
            (21,16);
            ''')
            






conn.commit()

cur.close()
conn.close()