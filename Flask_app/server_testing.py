import psycopg2
import sqlalchemy

conn = psycopg2.connect(host="localhost", database="DIS_Test", user="postgres", password="Choudhary6583", port=5432)

cur = conn.cursor()

# create Table for Authors from the small_diku_authors.csv



cur.execute('''
            DROP TABLE IF EXISTS writes;
''')

cur.execute('''
            
            DROP TABLE IF EXISTS supervises;
''')


cur.execute('''
            DROP TABLE IF EXISTS authors;
''')


cur.execute('''
            DROP TABLE IF EXISTS projects;
''')

cur.execute('''
            DROP TABLE IF EXISTS supervisors;
''')

cur.execute('''
            CREATE TABLE IF NOT EXISTS authors ( 
                author_name VARCHAR(255),
                author_id int,
                PRIMARY KEY (author_id));
''')

# create Table for Projects from the small_diku_projects.csv

cur.execute('''
CREATE TABLE IF NOT EXISTS projects (
            project_title VARCHAR(255),
            project_degree VARCHAR(255),
            project_pdf VARCHAR(255),
            project_year int,
            project_university VARCHAR(255),
            project_id int,
            PRIMARY KEY (project_id));
''')

# create Table for supervisors from the small_diku_supervisors.csv

cur.execute('''
CREATE TABLE IF NOT EXISTS supervisors (
            supervisor_name VARCHAR(255),
            supervisor_id int,
            PRIMARY KEY (supervisor_id));
''')


# fill in the data author,id from the small_diku_authors.csv

with open('small_diku_authors.csv', 'r') as f:
    next(f)
    cur.copy_from(f, 'authors', sep=',')


#  fill in the data projects from the small_diku_projects.csv

with open('small_diku_projects.csv', 'r') as f:
    next(f)
    cur.copy_from(f, 'projects', sep=',')

# fill in the data supervisors from the small_diku_supervisors.csv

with open('small_diku_supervisors.csv', 'r') as f:
    next(f)
    cur.copy_from(f, 'supervisors', sep=',')

# create Table for Author-Writes-Projects that connects the authors and projects

cur.execute('''
CREATE TABLE IF NOT EXISTS writes (
            author_id int,
            project_id int,
            PRIMARY KEY (author_id, project_id),
            FOREIGN KEY (author_id) REFERENCES authors (author_id),
            FOREIGN KEY (project_id) REFERENCES projects (project_id)
            );
''') 

# create Table for Supervisor-Supervises-Projects that connects the supervisors and projects

cur.execute('''
CREATE TABLE IF NOT EXISTS supervises (
            supervisor_id int,
            project_id int,
            PRIMARY KEY (supervisor_id, project_id),
            FOREIGN KEY (supervisor_id) REFERENCES supervisors (supervisor_id),
            FOREIGN KEY (project_id) REFERENCES projects (project_id)
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