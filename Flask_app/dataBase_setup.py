import psycopg2


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
                id SERIAL,
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
            id SERIAL,
            PRIMARY KEY (id));
''')

# create Table for supervisors from the small_diku_supervisors.csv

cur.execute('''
CREATE TABLE IF NOT EXISTS supervisor (
            name VARCHAR(255),
            id SERIAL,
            PRIMARY KEY (id));
''')



cur.execute(''' INSERT INTO author (name) VALUES
            ('Christian Påbøl'),
            ('Anders Holst'),
            ('Christian Marslev'),
            ('Jonas Grønborg'),
            ('Bjarke Pedersen'),
            ('Oscar Nelin'),
            ('William Henrich Due'),
            ('Rune Nielsen'),
            ('Cornelius Sevald-Krause'),
            ('Kasper Unn Weihe'),
            ('Tjørn Lynghus'),
            ('Jóhann Utne'),
            ('Henriette Naledi Winther Hansen'),
            ('Peter Kanstrup Larsen'),
            ('Emil Vilandt Rasmussen'),
            ('Caroline Amalie Kierkegaard'),
            ('Mikkel Willen'),
            ('Søren Brix'),
            ('Gilli Reynstind Fjallstein'),
            ('Lotte Bruun'),
            ('Ulrik Larsen');
            ''')
            


cur.execute(''' INSERT INTO project (title, degree, pdf, year, university) VALUES
    ('Two optimizations to GPU code generation in the Futhark compiler', 'MSc', 'https://futhark-lang.org/student-projects/christian-anders-scan-reduce-msc-project.pdf', 2024, 'DIKU'),
    ('Efficient Sequentialization of Parallelism', 'MSc', 'https://futhark-lang.org/student-projects/jonas-christian-effseq-msc-thesis.pdf', 2024, 'DIKU'),
    ('General Array Locality Optimization by Permutation (GALOP)', 'MSc', 'https://futhark-lang.org/student-projects/pedersen-nelin-msc-thesis.pdf', 2024, 'DIKU'),
    ('Parallel Parsing using Futhark', 'BSc', 'https://futhark-lang.org/student-projects/william-bsc-thesis.pdf', 2023, 'DIKU'),
    ('Implementation of Graph Algorithms in Futhark', 'BSc', 'https://futhark-lang.org/student-projects/rune-bsc-thesis.pdf', 2023, 'DIKU'),
    ('Flattening Irregular Nested Parallelism in Futhark', 'BSc', 'https://futhark-lang.org/student-projects/cornelius-bsc-thesis.pdf', 2023, 'DIKU'),
    ('Convex Optimization and Parallel Computing for Portfolio Optimization', 'MSc', 'https://futhark-lang.org/student-projects/kasper-msc-thesis.pdf', 2023, 'DIKU'),
    ('Data-parallel Implementation of Randomized Approximate Nearest Neighbours', 'BSc', 'https://futhark-lang.org/student-projects/Tjorn-BSc-Approx-kNN.pdf', 2023, 'DIKU'),
    ('Solving TSP on the GPU based on heuristic algorithms', 'BSc', 'https://futhark-lang.org/student-projects/BSc-Henriette-Johann-TSP.pdf', 2023, 'DIKU'),
    ('Application of Probabilistic Machine Learning Methods for Protein Generation', 'MSc', 'https://futhark-lang.org/student-projects/peter-larsen-msc-var-enc.pdf', 2023, 'DIKU'),
    ('Sparse Approximate Inverse - A Massively Parallel Implementation', 'BSc', 'https://futhark-lang.org/student-projects/Emil-Rasmussen-BSc-SPAI.pdf', 2023, 'DIKU'),
    ('Parallel Implementation of the SPAI algorithm', 'BSc', 'https://futhark-lang.org/student-projects/Caroline-Mikkel-BSc-SPAI.pdf', 2023, 'DIKU'),
    ('Benchmarking Futhark-AD using MINPACK-2', 'No degree found', 'https://futhark-lang.org/student-projects/peter-msc-project.pdf', 2023, 'DIKU'),
    ('Reverse mode automatic differentiation of histograms in Futhark', 'MSc', 'https://futhark-lang.org/student-projects/søren-msc-thesis.pdf', 2022, 'DIKU'),
    ('Extending automatic differentiation for an array language with nested parallelism', 'Msc', 'https://futhark-lang.org/student-projects/gilli-msc-thesis.pdf', 2022, 'DIKU'),
    ('Reverse Automatic Differentiation in Futhark', 'MSc', 'https://futhark-lang.org/student-projects/lotte-ulrik-msc-thesis.pdf', 2022, 'DIKU');
    ''')


cur.execute(''' INSERT INTO supervisor (name) VALUES
    ('Troels Henriksen'),
    ('Cosmin Oancea'),
    ('Martin Elsman');
    ''')

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

# inserting data into the supervises table

cur.execute(''' INSERT INTO supervises (supervisor_id, project_id) VALUES
            
            (1,1),
            (1,2),
            (2,3),
            (2,4),
            (2,5),
            (2,6),
            (3,7),
            (1,8),
            (1,9),
            (1,10),
            (1,12),
            (1,13),
            (1,14),
            (1,15),
            (1,16);
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