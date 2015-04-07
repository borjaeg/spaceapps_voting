import MySQLdb as mdb

def add_hash(project_name):
    return '#' + project_name

def insert_project(connection, project_name):
    query = "INSERT INTO projects(hashtag) VALUES ('%s')" %  project_name
    print query
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def get_connection():
    return mdb.connect("localhost", "root", "", "spaceapps")

def close_connection(connection):
    connection.close()

# dummy data with projects
projects = ['energy2people', 'mycupuola','open_curiosity']

connection = get_connection()
for project in projects:
    print add_hash(project)
    insert_project(connection, add_hash(project))

