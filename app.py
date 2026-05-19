from flask import Flask, render_template, request
import os
import sqlite3
import psycopg2
from urllib.parse import urlparse

app = Flask(__name__)

# Detect database type
DATABASE_URL = os.environ.get('DATABASE_URL')
USE_POSTGRESQL = DATABASE_URL is not None

def get_db_connection():
    """Get database connection based on environment"""
    if USE_POSTGRESQL:
        # Parse PostgreSQL URL
        parsed = urlparse(DATABASE_URL)
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path[1:],  # Remove leading slash
            user=parsed.username,
            password=parsed.password
        )
        return conn
    else:
        # Use SQLite locally
        return sqlite3.connect('students.db')

def init_db():
    """Initialize database tables"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if USE_POSTGRESQL:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    name TEXT,
                    mobile TEXT,
                    email TEXT,
                    course TEXT,
                    city TEXT
                )
            ''')
        else:
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
        print(f"Database initialized ({'PostgreSQL' if USE_POSTGRESQL else 'SQLite'})")
    except Exception as e:
        print(f"Database initialization error: {e}")

init_db()



@app.route('/')

def home():

    return render_template('home.html')



@app.route('/contact', methods=['GET', 'POST'])

def contact():



    if request.method == 'POST':



        name = request.form['name']

        mobile = request.form['mobile']

        email = request.form['email']

        course = request.form['course']

        city = request.form['city']



        conn = get_db_connection()

        cur = conn.cursor()

        if USE_POSTGRESQL:
            cur.execute('''
                INSERT INTO students
                (name, mobile, email, course, city)
                VALUES (%s, %s, %s, %s, %s)
            ''', (name, mobile, email, course, city))
        else:
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
    app.run(host='0.0.0.0', debug=False)