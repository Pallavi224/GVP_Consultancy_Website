from flask import Flask, render_template, request
from pyngrok import ngrok

import sqlite3



app = Flask(__name__)



# Create database

def init_db():

    conn = sqlite3.connect('students.db')

    cur = conn.cursor()



    cur.execute('''

        CREATE TABLE IF NOT EXISTS students (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            mobile TEXT,

            email TEXT,

            course TEXT,

            city TEXT

        )

    ''')



    conn.commit()

    conn.close()



init_db()



@app.route('/')

def home():

    return render_template('home.html')



@app.route('/courses')

def courses():

    return render_template('courses.html')



@app.route('/contact', methods=['GET', 'POST'])

def contact():



    if request.method == 'POST':



        name = request.form['name']

        mobile = request.form['mobile']

        email = request.form['email']

        course = request.form['course']

        city = request.form['city']



        conn = sqlite3.connect('students.db')

        cur = conn.cursor()



        cur.execute('''

            INSERT INTO students

            (name, mobile, email, course, city)

            VALUES (?, ?, ?, ?, ?)

        ''', (name, mobile, email, course, city))



        conn.commit()

        conn.close()



        return "Registration Successful!"



    return render_template('contact.html')



if __name__ == '__main__':

    print("Local URL: http://127.0.0.1:5000")
    try:
        public_url = ngrok.connect(5000, "http").public_url
        print(f"ngrok tunnel available at: {public_url}")
    except Exception as e:
        print("Warning: ngrok tunnel could not be started.", e)
        print("If ngrok is unavailable, open http://127.0.0.1:5000 locally instead.")

    app.run(host='0.0.0.0', debug=True)