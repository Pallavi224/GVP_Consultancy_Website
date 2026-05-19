from flask import Flask, render_template, request
import os
import sqlite3
import smtplib
import urllib.request
import base64
from email.message import EmailMessage
from urllib.parse import urlparse, urlencode

try:
    import psycopg2
except Exception as e:
    psycopg2 = None
    print('psycopg2 import failed:', e)

try:
    import pg8000
except Exception as e:
    pg8000 = None
    print('pg8000 import failed:', e)

app = Flask(__name__)

def get_db_connection():
    """Get database connection based on environment"""
    database_url = os.environ.get('DATABASE_URL')
    use_postgresql = database_url is not None

    if use_postgresql:
        parsed = urlparse(database_url)
        conn_args = {
            "host": parsed.hostname,
            "port": parsed.port or 5432,
            "database": parsed.path[1:],  # Remove leading slash
            "user": parsed.username,
            "password": parsed.password,
        }

        if parsed.hostname not in ("localhost", "127.0.0.1"):
            conn_args["sslmode"] = "require"

        if psycopg2 is not None:
            return psycopg2.connect(**conn_args)
        elif pg8000 is not None:
            # pg8000 uses ssl=True for remote connections
            if parsed.hostname not in ("localhost", "127.0.0.1"):
                conn_args["ssl"] = True
            return pg8000.connect(**conn_args)
        else:
            raise RuntimeError("No PostgreSQL driver is available. Install psycopg2 or pg8000.")
    else:
        # Use SQLite locally
        return sqlite3.connect('students.db')


def send_email_notification(subject, body):
    mail_server = os.environ.get('MAIL_SERVER')
    if not mail_server:
        print('Email notification skipped: MAIL_SERVER is not configured.')
        return

    mail_port = int(os.environ.get('MAIL_PORT', '587'))
    mail_username = os.environ.get('MAIL_USERNAME')
    mail_password = os.environ.get('MAIL_PASSWORD')
    mail_from = os.environ.get('MAIL_FROM', mail_username)
    mail_to = os.environ.get('MAIL_TO', 'rajnavigvt224@gmail.com')

    if not mail_username or not mail_password:
        print('Email notification skipped: MAIL_USERNAME or MAIL_PASSWORD is missing.')
        print('Email notification skipped: MAIL_USERNAME, MAIL_PASSWORD, or MAIL_TO is missing.')
        return

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = mail_from
    msg['To'] = mail_to
    msg.set_content(body)

    try:
        with smtplib.SMTP(mail_server, mail_port) as server:
            if os.environ.get('MAIL_USE_TLS', 'true').lower() in ('true', '1', 'yes'):
                server.starttls()
            server.login(mail_username, mail_password)
            server.send_message(msg)
        print('Email notification sent.')
    except Exception as e:
        print('Email notification error:', e)


def send_whatsapp_notification(body):
    account_sid = os.environ.get('WHATSAPP_ACCOUNT_SID')
    auth_token = os.environ.get('WHATSAPP_AUTH_TOKEN')
    from_number = os.environ.get('WHATSAPP_FROM')
    to_number = os.environ.get('WHATSAPP_TO', '9060168350')

    if not (account_sid and auth_token and from_number and to_number):
        print('WhatsApp notification skipped: Twilio WhatsApp credentials are not configured.')
        return

    url = f'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json'
    data = urlencode({
        'From': f'whatsapp:{from_number}',
        'To': f'whatsapp:{to_number}',
        'Body': body,
    }).encode('utf-8')

    auth = base64.b64encode(f'{account_sid}:{auth_token}'.encode('utf-8')).decode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST', headers={
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/x-www-form-urlencoded',
    })

    try:
        with urllib.request.urlopen(req) as resp:
            print('WhatsApp notification status:', resp.status)
    except Exception as e:
        print('WhatsApp notification error:', e)


def init_db():
    """Initialize database tables"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        use_postgresql = os.environ.get('DATABASE_URL') is not None

        if use_postgresql:
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
        print(f"Database initialized ({'PostgreSQL' if use_postgresql else 'SQLite'})")
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
        use_postgresql = os.environ.get('DATABASE_URL') is not None

        if use_postgresql:
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

        notification_body = (
            f"New contact form submission:\n"
            f"Name: {name}\n"
            f"Mobile: {mobile}\n"
            f"Email: {email}\n"
            f"Course: {course}\n"
            f"City: {city}\n"
        )

        send_email_notification('New contact form submission', notification_body)
        send_whatsapp_notification(notification_body)

        return "Registration Successful!"



    return render_template('contact.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)