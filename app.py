from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect('courses.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            roll_number TEXT NOT NULL,
            department TEXT NOT NULL,
            course_name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""

    if request.method == 'POST':
        student_name = request.form['student_name'].strip()
        roll_number = request.form['roll_number'].strip()
        department = request.form['department'].strip()
        course_name = request.form['course_name'].strip()

        if not all([student_name, roll_number, department, course_name]):
            message = "Please fill all the fields."
        else:
            conn = sqlite3.connect('courses.db')
            conn.execute('''
                INSERT INTO registrations
                (student_name, roll_number, department, course_name)
                VALUES (?, ?, ?, ?)
            ''', (student_name, roll_number, department, course_name))
            conn.commit()
            conn.close()
            message = "Course registration successful!"

    conn = sqlite3.connect('courses.db')
    conn.row_factory = sqlite3.Row
    students = conn.execute('SELECT * FROM registrations').fetchall()
    conn.close()

    return render_template('index.html',
                           students=students,
                           message=message)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)