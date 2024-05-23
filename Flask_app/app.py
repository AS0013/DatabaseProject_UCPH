from flask import Flask,render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Choudhary6583@localhost/DIS_Test'
# app.config['SECRET_KEY']  # some sort of secret key can added for security? gonna look into this later. 
# https://stackoverflow.com/questions/34902378/where-do-i-get-secret-key-for-flask

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

    

    return render_template('index.html', projects=projects)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/project/<string:title>')
def project(title):
    
    project = Project.query.filter_by(title=title).first()

    if project:

        # get the authors of the project aswell

        authors = db.session.query(Author).join(Writes, Author.id == Writes.author_id).filter(Writes.project_id == project.id).all()
        project = {
            "title": project.title,
            "degree": project.degree,
            "year": project.year,
            "university": project.university,
            "pdf": project.pdf,
            "authors": [author.name for author in authors]
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
        projects_with_authors = projects_with_authors.filter(Project.title.ilike(f'%{query}%'))
    
    if level:
        projects_with_authors = projects_with_authors.filter(Project.degree == level)
    
    if year:
        projects_with_authors = projects_with_authors.filter(Project.year == year)
    
    if university:
        projects_with_authors = projects_with_authors.filter(Project.university == university)

    projects_with_authors = projects_with_authors.all()

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