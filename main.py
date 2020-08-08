
from flask import Flask, render_template, request
import pymysql
app = Flask(__name__)
try:
    connection = pymysql.connect(host='localhost',
                                 user='John',
                                 password='Doe',
                                 db='sample',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
except:
    print('provide proper database credentials')
    exit(0)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        uname = request.form['uname']
        pwd = request.form['pwd']
        cur = connection.cursor()
        cur.execute(f'select * from users where uname="{uname}";')
        try:
            '''
            even if the username does not exist the same message is shown for better security reasons
            '''
            pwdindb = cur.fetchall()[0]['password']
            if pwd != pwdindb:
                raise Exception()
        except:
            return render_template('failed.html', message='Invalid Email ID or Password')
        connection.commit()
        cur.close()
        return render_template('dashboard.html', uname=uname)


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        uname = request.form['uname']
        pwd = request.form['pwd']

        if len(pwd) < 6:
            if len(uname) == 0 or len(request.form['fullname']) == 0:
                return render_template('failed.html', message="Field(s) cannot be empty")
            return render_template('failed.html', message="Password should be above 6 characters")


        cur = connection.cursor()
        cur.execute(f'select * from users where uname="{uname}";')
        if len(cur.fetchall()) > 0:
            return render_template('failed.html', message='Username already exists')

        cur.execute(f'insert into users(fullname, uname, password) values("dummy", "{request.form["uname"]}", "{request.form["pwd"]}");')
        connection.commit()
        cur.close()
        return render_template('dashboard.html', uname=uname)


if __name__ == "__main__":
    app.run(debug=True)
