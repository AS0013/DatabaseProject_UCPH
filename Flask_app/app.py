from flask import Flask,render_template, request, redirect, url_for
import os

app = Flask(__name__)

projects = [
    {"title": "Project A", "level": "Bachelor", "description": "Description of Project A", "author": "Author A", "date": "2021"},
    {"title": "Project B", "level": "Master", "description": "Description of Project B", "author": "Author B", "date": "2020"},
]


@app.route('/')
def index():
    return render_template('index.html', projects=projects)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    filtered_projects = [project for project in projects if query.lower() in project['title'].lower()]
    return render_template('index.html', projects=filtered_projects)

@app.route('/filter', methods=['POST'])
def filter():
    level = request.form['level']
    filtered_projects = [project for project in projects if project['level'] == level]
    return render_template('index.html', projects=filtered_projects)


if __name__ == '__main__':
    app.run(debug=True)