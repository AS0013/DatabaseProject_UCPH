from flask import Flask,render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Choudhary6583@localhost/DIS_Test'

db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    degree = db.Column(db.String(255), nullable=False)
    pdf = db.Column(db.String(255), nullable=False)
    university = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Projects %r>' % self.title
    
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Author %r>' % self.name


class Supervisor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Supervisor %r>' % self.name
    
class Writes(db.Model):
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)

    __table_args__ = (
        db.UniqueConstraint('author_id', 'project_id', name='unique_author_project'),
    )

    def __repr__(self):
        return '<Writes %r>' % self.author_id   
    
class Supervises(db.Model):
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisor.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)

    __table_args__ = (
        db.UniqueConstraint('supervisor_id', 'project_id', name='unique_supervisor_project'),
    )

    def __repr__(self):
        return '<Supervises %r>' % self.supervisor_id

@app.route('/')
def index():

    # get all the authors that worked on the same project


    projects_with_authors = db.session.query(Project, Author).join(Writes, Project.id == Writes.project_id).join(Author, Writes.author_id == Author.id).all()
    
    project_dict = {}
    for project, author in projects_with_authors:
        if project.id not in project_dict:
            project_dict[project.id] = {
                'title': project.title,
                'degree': project.degree,
                'year': project.year,
                'university': project.university,
                'authors': []
            }
        project_dict[project.id]['authors'].append(author.name)
    
    projects = list(project_dict.values())

    distinct_years = db.session.query(Project.year).distinct().order_by(Project.year).all()
    years = [year[0] for year in distinct_years]

    return render_template('index.html', projects=projects, years=years)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/addProject')
def addProject():
    return render_template('addProject.html')

@app.route('/addProject', methods=['POST'])
def addProjectPost():
    title = request.form.get('title')
    degree = request.form.get('degree')
    year = request.form.get('year')
    university = request.form.get('university')
    authors = [author.strip() for author in request.form.get('author').split(',')]
    supervisor = request.form.get('supervisor')
    pdf = request.form.get('pdf')

    pdf_pattern = r"https?://[^\s]+\.pdf"

    if not re.match(pdf_pattern, pdf):
        # call error message
        return render_template('addProject.html', error="Please enter a valid pdf link")

    # adding the project to the database with the next available id
    project = Project(title=title, degree=degree, year=year, university=university, pdf=pdf)
    db.session.add(project)
    db.session.commit()

    # adding the author to the database with the next available id
    for author in authors:
        author = Author(name=author)
        db.session.add(author)
    db.session.commit()


    # adding the author to the project

    for author in authors:
        writes = Writes(author_id=Author.query.filter_by(name=author).first().id, project_id=project.id)
        db.session.add(writes)
    db.session.commit()

    #adding the supervisor

    supervisor = Supervisor(name=supervisor)
    db.session.add(supervisor)
    db.session.commit()

    #adding the supervises
    supervises = Supervises(supervisor_id=supervisor.id, project_id=project.id)
    db.session.add(supervises)
    db.session.commit()

    return redirect(url_for('index'))

    


@app.route('/project/<string:title>')
def project(title):
    
    project = Project.query.filter_by(title=title).first()

    if project:

        # get the authors of the project aswell

        authors = db.session.query(Author).join(Writes, Author.id == Writes.author_id).filter(Writes.project_id == project.id).all()
        supervisors = db.session.query(Supervisor).join(Supervises, Supervisor.id == Supervises.supervisor_id).filter(Supervises.project_id == project.id).all()
        project = {
            "title": project.title,
            "degree": project.degree,
            "year": project.year,
            "university": project.university,
            "pdf": project.pdf,
            "authors": [author.name for author in authors],
            "supervisor": supervisors[0].name if supervisors else None
        }
        return render_template('projectPage.html', project=project)
    else:
        return render_template('404.html'), 404


@app.route('/search', methods=['POST'])
def search():

    query = request.form['query']
    level = request.form['level']
    year = request.form['year']
    university = request.form['university']

    projects_with_authors = db.session.query(Project, Author).join(Writes, Project.id == Writes.project_id).join(Author, Writes.author_id == Author.id)

    if query:
        projects_with_authors = projects_with_authors.filter(Project.title.ilike(f'%{query}%') | Author.name.ilike(f'%{query}%'))
    
    if level:
        projects_with_authors = projects_with_authors.filter(Project.degree == level)
    
    if year:
        projects_with_authors = projects_with_authors.filter(Project.year == year)
    
    if university:
        projects_with_authors = projects_with_authors.filter(Project.university == university)


    project_ids = [project.id for project, author in projects_with_authors.all()]

    projects_with_authors = db.session.query(Project, Author).join(Writes, Project.id == Writes.project_id).join(Author, Writes.author_id == Author.id).filter(Project.id.in_(project_ids)).all()

    project_dict = {}

    for project, author in projects_with_authors:
        if project.id not in project_dict:
            project_dict[project.id] = {
                'title': project.title,
                'degree': project.degree,
                'year': project.year,
                'university': project.university,
                'authors': []
            }
        project_dict[project.id]['authors'].append(author.name)

    projects = list(project_dict.values())
    
    return render_template('index.html', projects=projects)


if __name__ == '__main__':
    app.run(debug=True)