import MySQLdb as mdb
import csv

def insert_project(connection, project_name):
    query = "INSERT INTO projects(hashtag) VALUES ('%s')" %  project_name
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

def get_connection():
    return mdb.connect("localhost", "root", "", "spaceapps")

def close_connection(connection):
    connection.close()

def add_projects():    
    projects = ['NATUREVENT', 'EYE OF HORUS','ISSDATA','PISTACHOFLOW']
    connection = get_connection()
    for project in projects:
        insert_project(connection, project)

def add_participants():
    #Importing parcticipants
    connection = get_connection()
    cursor = connection.cursor()
    with open('/Users/b3j90/Downloads/2015-04-11T17-27-37Z zaragoza Attendees.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            query = "INSERT INTO participants(email) VALUES('%s')" % (row['Email'])
            cursor.execute(query)
            connection.commit()

    close_connection(connection)

if __name__ == "__main__":
    add_projects()
    add_participants()

