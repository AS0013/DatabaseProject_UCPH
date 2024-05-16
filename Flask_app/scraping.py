# for scraping
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re


url = "https://futhark-lang.org/publications.html#selected-student-projects"

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

# print(soup.prettify())

# Extracting just one project to see how to extract the information
# in the ul tag after the h2 tag with id selected-student-projects

project = soup.find('h2', id='selected-student-projects').find_next('ul')

# in each <p> to </p> tag, there is a project. the format is: 
# <p>
#      name(s) of the author(s):
#    <strong>
#     title of the project
#    </strong>
#    ,degree level , University, Month year (
#    <a href="link to the pdf">
#     pdf
#    </a>
#    )
# </p>

# Extracting the information from the first project
# project1 = project.find('p')

# # Extracting the name of the author(s), removing :
# author = project1.contents[0].strip().replace(':', '')
# # author = project1.contents[0].strip()

# print(author)

# # Extracting the title of the project
# title = project1.find('strong').text.strip()

# print(title)

# # Extracting the degree level
# degree_level = project1.find('strong').text.strip()

# print(degree_level)

# # Extracting the university
# university = project1.find('strong').find_next('strong').find_next('strong').text.strip()

# # Extracting the month and year
# month_year = project1.find('strong').find_next('strong').find_next('strong').strip()

# # Extracting the link to the pdf
# pdf = project1.find('a')['href']

# link_pdf = 'https://futhark-lang.org/' + pdf

# print(link_pdf)

# # Creating a dictionary with the information extracted
# project1_dict = {
#     'author': author,
#     'title': title,
#     'degree_level': degree_level,
#     'university': university,
#     'month_year': month_year,
#     'pdf': pdf
# }

# print(project1_dict)


# Extrating all the information in in each p tag in the ul tag after the h2 tag with id selected-student-projects and storing each p tag in a list
projects = project.find_all('p')

# make a list where each element is the string of the p tag including the html tags
projects_list = [str(project) for project in projects]


# print(projects_list[-1])
# print(projects_list[0])

# regular expression to get the author(s) name(s)
# author_pattern = (r'<p>(.*?)\s*:')
author_pattern = r'<p>(.*?)\s*:'


list_of_authors = []
list_of_DIKU_authors = []

DIKU_project_list = []
DIKU_key_words = ['DIKU']
# getting only the projects that contain 'DIKU', 'Department of Computer Science', 'University of Copenhagen'

for project in projects_list:
    if any(word in project for word in DIKU_key_words):
        DIKU_project_list.append(project)

print("DIKU PROJECTS-----------------")

print(DIKU_project_list)
print(len(DIKU_project_list))

print("-----------------DIKU PROJECTS")

# for project in projects_list:
#     print(project)
#     print('----------------')
#     match = re.search(author_pattern, project , re.DOTALL)
#     if match:
#         author = match.group(1)
#         list_of_authors.append(author)
#         # print(author)
#     else:
#         list_of_authors.append('No author found')

# finrd the index there is no author
no_author_index = [index for index, author in enumerate(list_of_authors) if author == 'No author found']

print(no_author_index)

# print(list_of_authors)

# remove \n and \t from the author name
list_of_authors = [author.replace('\n', ' ').replace('\t', ' ') for author in list_of_authors]

print(list_of_authors)

# regular expression to get the title of the project
title_pattern = r'<strong>(.*?)</strong>'

list_of_titles = []

for project in projects_list:
    match = re.search(title_pattern, project, re.DOTALL)
    if match:
        title = match.group(1)
        list_of_titles.append(title)
    else:
        list_of_titles.append('No title found')

print(list_of_titles)

# find the index there is no title

no_title_index = [index for index, title in enumerate(list_of_titles) if title == 'No title found']

if(len(no_title_index) > 0):
    print(no_title_index)
else:
    print('ALL TITLES FOUND')

print(len(list_of_authors) == len(list_of_titles))

# regular expression to get the degree level
degree_pattern = r'\b(?:BSc|MSc|Msc|Bsc)\b'

list_of_degrees = []

for project in projects_list:
    match = re.search(degree_pattern, project, re.DOTALL)
    if match:
        degree = match.group(0)
        list_of_degrees.append(degree)
    else:
        list_of_degrees.append('No degree found')

no_degree_index = [index for index, degree in enumerate(list_of_degrees) if degree == 'No degree found']

if(len(no_degree_index) > 0):
    print(no_degree_index)
else:
    print('ALL DEGREES FOUND')

print(projects_list[21])

# this is project 19 which doesnt seem to get the author name even though the pattern is correct
# <p>W. Pema N. H. Malling, Louis Marott Normann, Oliver
# B. K. Petersen, Kristoffer A. Kortbæk: <strong>Extending Futhark’s
# multicore C backend to utilize SIMD using ISPC</strong>. BSc thesis. Department of
# Computer Science, University of Copenhagen.
# June 2022. (<a href="student-projects/ispc-bsc-thesis.pdf">pdf</a>)</p>

# print(projects_list[19])

# match = re.search(author_pattern, "<p>W. Pema N. H. Malling, Louis Marott Normann, Oliver B. K. Petersen, Kristoffer A. Kortbæk: <strong>")
# if match:
#     print(match.group(1))
# else:
#     print('No author found')

# NOTE ELEMENT 14 SHOULD NOT BE INCLUDED AS IT IS NOT A BSC NOR MSC THESIS
# NOTE ELEMENT 30,21 SHOULD NOT BE INCLUDED AS IT DOES NOT MENTION WHAT KIND OF THESIS IT IS
# NOTE ELEMENT 29,31,32 SHOULD  BE INCLUDED AS IT IS MSC THESIS

print(list_of_degrees)
# element 29, 31, 32 shoulde be 'MSc'

list_of_degrees[29] = 'MSc'
list_of_degrees[31] = 'MSc'
list_of_degrees[32] = 'MSc'

print(list_of_degrees)

no_degree_index = [index for index, degree in enumerate(list_of_degrees) if degree == 'No degree found']

if(len(no_degree_index) > 0):
    print(no_degree_index)
else:
    print('ALL DEGREES FOUND')

print(len(list_of_authors) == len(list_of_degrees))

# regular expression to get month end year
month_year_pattern = r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}'

list_of_month_years = []

for project in projects_list:
    match = re.search(month_year_pattern, project, re.DOTALL)
    if match:
        month_year = match.group(0)
        list_of_month_years.append(month_year)
    else:
        list_of_month_years.append('No month year found')

no_month_year_index = [index for index, month_year in enumerate(list_of_month_years) if month_year == 'No month year found']


# change the month year for element 43 to June 2020
list_of_month_years[43] = 'June 2020'

print(list_of_month_years)

# get the pdf link

pdf_pattern = r'<a href="(.*?)">pdf</a>'
list_of_pdfs = []

for project in projects_list:
    match = re.search(pdf_pattern, project, re.DOTALL)
    if match:
        pdf = match.group(1)
        # add the full link to the pdf
        pdf = 'https://futhark-lang.org/' + pdf
        list_of_pdfs.append(pdf)
    else:
        list_of_pdfs.append('No pdf found')

no_pdf_index = [index for index, pdf in enumerate(list_of_pdfs) if pdf == 'No pdf found']

print(no_pdf_index)

# add the pdf link for element 43 https://futhark-lang.org/student-projects/niels-write-construct.pdf
# list_of_pdfs[43] = 'https://futhark-lang.org/student-projects/niels-write-construct.pdf'

# print(list_of_pdfs)


# print(no_uni_index)

# print(projects_list[18])


# print(list_of_unis)
# create a csv file with the information extracted 
# df = pd.DataFrame({
#     'author': list_of_authors,
#     'title': list_of_titles,
#     'degree': list_of_degrees,
#     'month_year': list_of_month_years,
#     'pdf': list_of_pdfs
# })

# print(df)

# df.to_csv('futhark_projects.csv', index=False)

# print("LIST OF PROJECTS...")

# print(projects_list)