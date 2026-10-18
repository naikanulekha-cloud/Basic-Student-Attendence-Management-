from flask import Flask, render_template, request, redirect
import mysql.connector
print("APP STARTED")
app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="attendance_system"
)

cursor = db.cursor()

# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')

# ================= STUDENTS =================

@app.route('/students')
def students():
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    return render_template('students.html', students=data)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    mail = request.form['mail']
    ph_no = request.form['ph_no']

    sql = "INSERT INTO students(name, mail, ph_no) VALUES(%s,%s,%s)"
    values = (name, mail, ph_no)

    cursor.execute(sql, values)
    db.commit()

    return redirect('/students')

# ================= TEACHERS =================

@app.route('/teachers')
def teachers():
    cursor.execute("SELECT * FROM teachers")
    data = cursor.fetchall()
    return render_template('teachers.html', teachers=data)

@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    name = request.form['name']
    mail = request.form['mail']
    ph_no = request.form['ph_no']

    sql = "INSERT INTO teachers(name, mail, ph_no) VALUES(%s,%s,%s)"
    values = (name, mail, ph_no)

    cursor.execute(sql, values)
    db.commit()

    return redirect('/teachers')

# ================= COURSES =================

@app.route('/courses')
def courses():
    cursor.execute("SELECT * FROM courses")
    data = cursor.fetchall()

    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()

    return render_template('courses.html',
                           courses=data,
                           teachers=teachers)

@app.route('/add_course', methods=['POST'])
def add_course():
    course_code = request.form['course_code']
    course_name = request.form['course_name']
    teacher_id = request.form['teacher_id']

    sql = """
    INSERT INTO courses(course_code, course_name, teacher_id)
    VALUES(%s,%s,%s)
    """

    values = (course_code, course_name, teacher_id)

    cursor.execute(sql, values)
    db.commit()

    return redirect('/courses')

# ================= CLASSES =================

@app.route('/classes')
def classes():
    cursor.execute("SELECT * FROM classes")
    data = cursor.fetchall()

    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    return render_template('classes.html',
                           classes=data,
                           courses=courses)

@app.route('/add_class', methods=['POST'])
def add_class():
    class_date = request.form['class_date']
    room_no = request.form['room_no']
    course_id = request.form['course_id']

    sql = """
    INSERT INTO classes(class_date, room_no, course_id)
    VALUES(%s,%s,%s)
    """

    values = (class_date, room_no, course_id)

    cursor.execute(sql, values)
    db.commit()

    return redirect('/classes')

# ================= ATTENDANCE =================

@app.route('/attendance')
def attendance():

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()

    cursor.execute("SELECT * FROM classes")
    classes = cursor.fetchall()

    return render_template('attendance.html',
                           students=students,
                           teachers=teachers,
                           classes=classes)

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():

    student_id = request.form['student_id']
    teacher_id = request.form['teacher_id']
    class_id = request.form['class_id']
    status = request.form['status']
    remarks = request.form['remarks']

    sql = """
    INSERT INTO attendance
    (student_id, teacher_id, class_id, status, remarks)
    VALUES(%s,%s,%s,%s,%s)
    """

    values = (
        student_id,
        teacher_id,
        class_id,
        status,
        remarks
    )

    cursor.execute(sql, values)
    db.commit()

    return redirect('/attendance')

# ================= REPORT =================

@app.route('/reports')
def reports():

    sql = """
    SELECT students.name,
           teachers.name,
           classes.class_date,
           attendance.status,
           attendance.remarks

    FROM attendance

    JOIN students
    ON attendance.student_id = students.student_id

    JOIN teachers
    ON attendance.teacher_id = teachers.teacher_id

    JOIN classes
    ON attendance.class_id = classes.class_id
    """

    cursor.execute(sql)

    data = cursor.fetchall()

    return render_template('reports.html',
                           records=data)

if __name__ == '__main__':
    app.run(debug=True)