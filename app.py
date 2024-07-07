from flask import Flask, render_template, request, jsonify
import mysql.connector as connection

app = Flask(__name__)


# @app.route('/', methods=['GET', 'POST']) # To render Homepage
# def home_page():
#     return render_template('index.html')

# @app.route('/math', methods=['POST'])  # This will be called from UI
# def math_operation():
#     if (request.method=='POST'):
#         operation=request.form['operation']
#         num1=int(request.form['num1'])
#         num2 = int(request.form['num2'])
#         if(operation=='add'):
#             r=num1+num2
#             result= 'the sum of '+str(num1)+' and '+str(num2) +' is '+str(r)
#         if (operation == 'subtract'):
#             r = num1 - num2
#             result = 'the difference of ' + str(num1) + ' and ' + str(num2) + ' is ' + str(r)
#         if (operation == 'multiply'):
#             r = num1 * num2
#             result = 'the product of ' + str(num1) + ' and ' + str(num2) + ' is ' + str(r)
#         if (operation == 'divide'):
#             r = num1 / num2
#             result = 'the quotient when ' + str(num1) + ' is divided by ' + str(num2) + ' is ' + str(r)
#         return render_template('results.html',result=result)

def connect_db(dbname, host, user, password):
    try:
        mydb = connection.connect(host=host, user=user, passwd=password)
        if mydb.is_connected():
            status = {"msg" : "Database connected!!", "code" : 200}
        else:
            status = {"msg":"Some error occured!!", "code" : 400}
    except:
        status = {"msg" : "Error!!", "code" : 404}
    return status,mydb



@app.route('/mysql/createDB', methods=['POST'])  # for calling the API from Postman/SOAPUI
def create_database():
    if request.method == 'POST':
        dbname = request.json['dbname']
        host = request.json['host']
        user = request.json['user']
        password = request.json['password']

        status,mydb = connect_db(dbname,host,user,password)

        if status["code"] == 200:
            try:
                query = f'Create database {dbname};'
                cursor = mydb.cursor()
                cursor.execute(query)
                mydb = connection.connect(host=host, database=dbname, user=user, passwd=password, use_pure=True)
                # cursor = mydb.cursor()
                status = {"msg" : "database created and connected","code" : 200}
            except:
                status = {"msg": "database creation error", "code": 400}

        return jsonify({'status': status})

@app.route('/mysql/createTable', methods=['POST'])  # for calling the API from Postman/SOAPUI
def create_table():
    if request.method == 'POST':
        dbname = request.json['dbname']
        host = request.json['host']
        user = request.json['user']
        password = request.json['password']
        table = request.json['tableName']

        status,mydb = connect_db(dbname,host,user,password)

        if status["code"] == 200:
            try:
                query = f'CREATE TABLE {table} (name varchar(16),age int(10));'
                mydb = connection.connect(host=host, database=dbname, user=user, passwd=password, use_pure=True)
                cursor = mydb.cursor()
                cursor.execute(query)
                status = {"msg" : "table created","code" : 200}
            except:
                status = {"msg": "table creation error", "code": 400}

        return jsonify({'status': status})

@app.route('/mysql/insert', methods=['POST'])  # for calling the API from Postman/SOAPUI
def insert():
    if request.method == 'POST':
        dbname = request.json['dbname']
        host = request.json['host']
        user = request.json['user']
        password = request.json['password']
        table = request.json['tableName']
        name = str(request.json['name'])
        age = int(request.json['age'])

        status,mydb = connect_db(dbname,host,user,password)

        if status["code"] == 200:
            try:
                query = f'INSERT INTO {dbname}.{table} (name,age) VALUES ("{name}",{age});'
                mydb = connection.connect(host=host, database=dbname, user=user, passwd=password, use_pure=True)
                cursor = mydb.cursor()
                cursor.execute(query)
                mydb.commit()
                status = {"msg" : "values inserted","code" : 200}
            except:
                status = {"msg": "values insertation error", "code": 400}

        return jsonify({'status': status})

@app.route('/mysql/display', methods=['POST'])  # for calling the API from Postman/SOAPUI
def display():
    if request.method == 'POST':
        dbname = request.json['dbname']
        host = request.json['host']
        user = request.json['user']
        password = request.json['password']
        table = request.json['tableName']

        status,mydb = connect_db(dbname,host,user,password)

        if status["code"] == 200:
            try:
                query = f"Select * from {table};"
                mydb = connection.connect(host=host, database=dbname, user=user, passwd=password, use_pure=True)
                cursor = mydb.cursor()
                cursor.execute(query)
                data = cursor.fetchall()
                status = {"msg" : "data fetched","code" : 200,"data" : data}
            except:
                status = {"msg": "data detch error", "code": 400}

        return jsonify({'status': status})

if __name__ == '__main__':
    app.run()
