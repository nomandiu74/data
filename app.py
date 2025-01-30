from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'Noman'  # Change this to a secure random key

# MySQL Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',       # Change to your MySQL username
        password='root',       # Change to your MySQL password
        database='form'  # The database where you want to store the data
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']

    # Save data to MySQL
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", (name, email, age))
    conn.commit()
    cursor.close()
    conn.close()

    return "Data saved successfully!"

# Admin page with password protection
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'logged_in' not in session:  # Check if the user is logged in
        return redirect(url_for('login'))

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to get all users
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    # Render the data in an HTML table
    return render_template('admin.html', users=users)

# Login page for admin
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']

        if password == 'Noman':  # Change this to a secure password
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return "Incorrect password, please try again."

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
