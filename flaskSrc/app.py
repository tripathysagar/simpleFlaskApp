from flask import Flask, redirect, url_for, render_template, request, json
from werkzeug.exceptions import HTTPException
import mysql.connector
#import os

app = Flask(__name__)
conection = None

class DBManger:
    def __init__(self, database='MARKS', host='db', user= 'root', password_file=None):
        file = open(password_file, 'r')
        self.connection = mysql.connector.connect(
            user= user,
            password = file.read(),
            host = host,
            database='MARKS',
            auth_plugin='mysql_native_password')
        self.cursor = self.connection.cursor()
        #self.cursor.execute('CREATE DATABASE MARKS;')
        file.close()
        
    
    def create_table(self):
        
        self.cursor.execute('DROP TABLE IF EXISTS RESULT;')

        self.cursor.execute('CREATE TABLE RESULT (name VARCHAR(20),math float,physics float,chemistry float);')
        self.connection.commit()
    
    def insert_db(self, data):
        insert_stmt = "INSERT INTO RESULT (name,math,physics,chemistry)  VALUES (%s, %s, %s, %s ) ;"
        self.cursor.execute(insert_stmt, data)
        self.connection.commit()
        
    def query_result(self, name=None):
        
        if name:
            stmt = f'SELECT * FROM RESULT where name = %s;'
            self.cursor.execute(stmt, (name,))
            name_lis = self.cursor.fetchall()
            return name_lis


        self.cursor.execute('SELECT * FROM RESULT;')
        record = self.cursor.fetchall()
        #return [rec[0][i] for i in range(len(rec))]
        name_lis = []
        for lis in record:
            name_lis.append(lis[0])
        return name_lis
        
        



@app.route("/")
def base():
    global conection 
    record = None
    if not conection:
        conection = DBManger(password_file='/run/secrets/db-password')
        conection.create_table()
    else:
        record = conection.query_result()
    app.logger.info(record)

    return render_template('index.html', record=record)

@app.route("/marks/<int:score>")
def marks(score):
    return f'total marks: {score}'

@app.route("/result", methods= ['POST', 'GET'] )
def result():
    
    if request.method == 'POST':
        global conection 
        totalScore = 0
        
        name = str(request.form['name'])
        math =  float(request.form['math'])
        physics = float(request.form['physics'])
        chemistry = float(request.form['chemistry'])
        
        totalScore = int(math+physics+chemistry)
        conection.insert_db((name,math,physics,chemistry))
        return redirect(url_for("marks",score=totalScore))
    
    return render_template('result.html')
    
@app.route("/student/<string:name>")
def student(name):
    rec = conection.query_result(name)
    app.logger.info("+++++++++++++++++")
    app.logger.info(rec)
    app.logger.info("+++++++++++++++++")
    rec = rec[0]
    record = {'name':rec[0], 'math':rec[1], 'physics':rec[2], 'chemistry':rec[3]}
    app.logger.info(record)
    return render_template('student.html', student=record)
    

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

