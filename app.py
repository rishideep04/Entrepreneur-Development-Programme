from flask import Flask, render_template, request, redirect, url_for
import psycopg2  # pip install psycopg2
import psycopg2.extras
from datetime import date

app = Flask(__name__, template_folder='./templates', static_folder='./static')
app.secret_key = "cairocoders-ednalan"

DB_HOST = "localhost"
DB_NAME = "EDP"
DB_USER = "postgres"
DB_PASS = "Lowkik0909$ai"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/instructor')
def inst():
    return render_template('signup.html')


@app.route('/participant')
def user():
    return render_template('signupuser.html')

#Instructor:

@app.route('/credentials', methods=['POST'])
def add_credentials():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    username = request.form['username']
    name = request.form['name']
    email = request.form['email']
    password = request.form['pass']
    qualification = request.form['qual']
    experience = request.form['exp']
    cur.execute("INSERT INTO credentials (id, name, email,password) VALUES (%s,%s,%s,%s)",
                (username, name, email, password))
    conn.commit()
    cur.execute(
        "INSERT INTO instructor (InstructorID, InstructorName, InstructorEmail,Qualification,Experience) VALUES (%s,%s,%s,%s,%s)",
        (username, name, email, qualification, experience))
    conn.commit()

    print('Student Added successfully')
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def validate():
    username = request.form['username']
    password = request.form['pass']

    # Check if the username exists
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT id, password FROM credentials WHERE id = %s", (username,))
    user_data = cur.fetchone()

    if user_data is None or user_data['id'] != username:
        print('Username not exists')
        return render_template('login.html')

    # Check if the password matches (assuming passwords are stored as plaintext)
    if password != user_data['password']:
        print('Wrong Password')
        return render_template('login.html')

    # Successful login
    print(username, " logged in")
    cur.execute(
        "SELECT Course.CourseName FROM Course WHERE Course.CourseID NOT IN ( SELECT TaughtBy.CourseID FROM TaughtBy WHERE TaughtBy.InstructorID = %s)",
        (username,))
    list_courses = cur.fetchall()
    images = {
        "Database Fundamentals": "https://ethanmesecar.tech/wp-content/uploads/2022/10/data-base-fubnd.png",
        "Python Programming": "https://www.digitalnest.in/blog/wp-content/uploads/2019/07/10-Benefits-of-Learning-Python-Programming-Language-and-Its-Use-Cases.png",
        "Data Science Essentials": "https://connecteddataacademy.com/wp-content/uploads/2019/09/Data-Science-Essentials-300x157.png",
        "Web Design": "https://kinsta.com/wp-content/uploads/2020/02/web-design-best-practices.jpg",
        "Mobile App Development": "https://www.velvetech.com/wp-content/uploads/2021/08/mobile-app-development-process-tw.jpg"
    }
    return render_template('home.html', username=username, list_courses=list_courses, images=images)


@app.route('/loginpage')
def login_page():
    return render_template('login.html')

@app.route('/teacherprofile')
def teacherprof():
    return render_template('teacher_profile.html')


@app.route('/home/<username>')
def gethome(username):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        "SELECT DISTINCT Course.CourseName FROM Course WHERE Course.CourseID NOT IN ( SELECT TaughtBy.CourseID FROM TaughtBy WHERE TaughtBy.InstructorID = %s)",
        (username,))
    list_courses = cur.fetchall()
    images = {
        "DatabaseFundamentals": "https://ethanmesecar.tech/wp-content/uploads/2022/10/data-base-fubnd.png",
        "PythonProgramming": "https://www.digitalnest.in/blog/wp-content/uploads/2019/07/10-Benefits-of-Learning-Python-Programming-Language-and-Its-Use-Cases.png",
        "DataScienceEssentials": "https://connecteddataacademy.com/wp-content/uploads/2019/09/Data-Science-Essentials-300x157.png",
        "WebDesign": "https://kinsta.com/wp-content/uploads/2020/02/web-design-best-practices.jpg",
        "MobileAppDevelopment": "https://www.velvetech.com/wp-content/uploads/2021/08/mobile-app-development-process-tw.jpg"
    }
    return render_template('home.html', username=username, list_courses=list_courses, images=images)


@app.route('/courses/<username>')
def get_course(username):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        "SELECT DISTINCT Course.CourseName FROM Course JOIN TaughtBy ON Course.CourseID = TaughtBy.CourseID JOIN Instructor ON TaughtBy.InstructorID = Instructor.InstructorID WHERE Instructor.InstructorID = %s",
        (username,))
    list_users = cur.fetchall()
    images = {
        "DatabaseFundamentals": "https://ethanmesecar.tech/wp-content/uploads/2022/10/data-base-fubnd.png",
        "PythonProgramming": "https://www.digitalnest.in/blog/wp-content/uploads/2019/07/10-Benefits-of-Learning-Python-Programming-Language-and-Its-Use-Cases.png",
        "DataScienceEssentials": "https://connecteddataacademy.com/wp-content/uploads/2019/09/Data-Science-Essentials-300x157.png",
        "WebDesign": "https://kinsta.com/wp-content/uploads/2020/02/web-design-best-practices.jpg",
        "MobileAppDevelopment": "https://www.velvetech.com/wp-content/uploads/2021/08/mobile-app-development-process-tw.jpg"
    }
    print(list_users)
    return render_template('courses.html', username=username, list_users=list_users, images=images)


@app.route('/playlist/<username>')
def get_student_list(username):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        "SELECT DISTINCT Users.UserID, Users.Name, Users.Email,Course.Coursename FROM Users JOIN Enrollment ON Users.UserID = Enrollment.UserID JOIN Course ON Enrollment.CourseID = Course.CourseID JOIN TaughtBy ON Course.CourseID = TaughtBy.CourseID WHERE TaughtBy.InstructorID = %s",
        (username,))
    list_users = cur.fetchall()
    return render_template('playlist.html', username=username, list_users=list_users)


@app.route('/aboutcourse/<coursename>/<username>')
def get_course_details(coursename, username):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print(coursename)
    cur.execute("SELECT coursename,coursedescription,courseduration,coursefee FROM COURSE WHERE COURSENAME = %s",
                (coursename,))
    course_details = cur.fetchall()
    return render_template('aboutcourse.html', course_details=course_details, username=username, coursename=coursename)


@app.route('/uploadresource/<username>/<coursename>')
def redirect_resource(username, coursename):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT COURSEID FROM COURSE WHERE COURSENAME = %s', (coursename,))
    id = cur.fetchone()
    if id:
        courseid = id[0]
    cur.execute('SELECT * FROM resource WHERE courseid = %s', (courseid,))
    data = cur.fetchall()
    cur.close()
    return render_template('resources.html', username=username, coursename=coursename, data=data)


@app.route('/addresource/<coursename>/<username>', methods=['POST'])
def upload_resource(coursename, username):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM COURSE WHERE COURSENAME = %s", (coursename,))
    course_data = cur.fetchone()

    courseid = course_data['courseid']  # Adjust this based on the actual column name
    restype = request.form['restype']
    reslink = request.form['reslink']
    resname = request.form['resname']
    upldate = date.today()

    cur.execute(
        "INSERT INTO RESOURCE(courseid,resourcetype,resourcelink,resourcename,uploaddate) VALUES(%s,%s,%s,%s,%s)",
        (courseid, restype, reslink, resname, upldate))
    conn.commit()

    return render_template('courses.html', username=username)


@app.route('/viewresource/<username>/<coursename>', methods=['GET', 'POST'])
def view(username, coursename):
    if request.method == 'POST':
        # Handle POST request logic if needed
        pass
    else:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT COURSEID FROM COURSE WHERE COURSENAME = %s', (coursename,))
        id = cur.fetchone()
        if id:
            courseid = id[0]
        cur.execute('SELECT * FROM resource WHERE courseid = %s', (courseid,))
        data = cur.fetchall()
        cur.close()

        return render_template('resources.html', coursename=coursename, username=username, data=data)


@app.route('/edit/<id>/<username>', methods=['POST', 'GET'])
def get_resource(id, username):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('SELECT * FROM resource WHERE resourceid = %s', (id))
    data = cur.fetchall()
    cur.close()
    return render_template('resources.html', username=username, data=data)


@app.route('/delete/<string:id>/<username>', methods=['POST', 'GET'])
def delete_resource(id, username):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('DELETE FROM resource WHERE resourceid = {0}'.format(id))
    conn.commit()
    return render_template('resources.html', username=username)


@app.route('/setschedule/<username>/<coursename>')
def set_schedule(username, coursename):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT COURSEID FROM COURSE WHERE COURSENAME = %s", (coursename,))
    id = cur.fetchone()  # Use fetchone instead of fetchall
    if id:
        courseid = id[0]
    cur.execute("SELECT DATE,TIME,LOCATION,scheduleid FROM SCHEDULE WHERE COURSEID=%s", (courseid,))
    data = cur.fetchall()
    return render_template('schedule.html', username=username, coursename=coursename, data=data)


@app.route('/setscheduledetails/<username>/<coursename>', methods=['POST'])
def set_scheduledetails(username, coursename):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT COURSEID FROM COURSE WHERE COURSENAME = %s", (coursename,))
    id = cur.fetchone()  # Use fetchone instead of fetchall
    if id:
        courseid = id[0]
    date = request.form['date']
    time = request.form['time']
    loc = request.form['loc']
    cur.execute("INSERT INTO Schedule (CourseID, Date, Time, Location) VALUES (%s,%s,%s,%s)",
                (courseid, date, time, loc,))
    conn.commit()
    cur.execute("SELECT DATE,TIME,LOCATION,scheduleid FROM SCHEDULE WHERE COURSEID=%s", (courseid,))
    data = cur.fetchall()

    return render_template('schedule.html', username=username, coursename=coursename, data=data)


@app.route('/editschedule/<id>/<username>/<coursename>', methods=['POST', 'GET'])
def edit_schedule(id, username, coursename):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT COURSEID FROM COURSE WHERE COURSENAME = %s", (coursename,))
    courseid = cur.fetchone()  # Use fetchone instead of fetchall
    courseid = courseid[0]
    cur.execute("SELECT DATE,TIME,LOCATION,scheduleid FROM SCHEDULE WHERE COURSEID=%s", (courseid,))
    data = cur.fetchall()
    cur.close()
    return render_template('editschedule.html', username=username, id=id, courseid=courseid, data=data,
                           coursename=coursename)


@app.route('/update/<id>/<username>/<coursename>', methods=['POST'])
def update_schedule(id, username, coursename):
    date = request.form['date']
    time = request.form['time']
    loc = request.form['loc']

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
            UPDATE schedule
            SET date = %s,
                time = %s,
                location = %s
            WHERE scheduleid = %s
        """, (date, time, loc, id))
    conn.commit()
    cur.execute("SELECT COURSEID FROM COURSE WHERE COURSENAME = %s", (coursename,))
    id = cur.fetchone()  # Use fetchone instead of fetchall
    if id:
        courseid = id[0]
    cur.execute("SELECT DATE,TIME,LOCATION,scheduleid FROM SCHEDULE WHERE COURSEID=%s", (courseid,))
    data = cur.fetchall()
    return render_template('schedule.html', username=username, coursename=coursename, data=data)


@app.route('/deleteschedule/<string:id>/<username>/<coursename>', methods=['POST', 'GET'])
def delete_schedule(id, username, coursename):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT COURSEID FROM COURSE WHERE COURSENAME = %s", (coursename,))
    courseid = cur.fetchone()  # Use fetchone instead of fetchall
    courseid = courseid[0]
    cur.execute('DELETE FROM schedule WHERE scheduleid = {0}'.format(id))
    conn.commit()
    cur.execute("SELECT DATE,TIME,LOCATION,scheduleid FROM SCHEDULE WHERE COURSEID=%s", (courseid,))
    data = cur.fetchall()
    return render_template('schedule.html', username=username, coursename=coursename, data=data)


@app.route('/instenroll/<username>/<coursename>')
def enroll(username, coursename):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT COURSEID FROM COURSE WHERE COURSENAME = %s", (coursename,))
    id = cur.fetchone()  # Use fetchone instead of fetchall
    if id:
        courseid = id[0]
        cur.execute("INSERT INTO TAUGHTBY VALUES(%s, %s)", (courseid, username))
        conn.commit()
    return render_template('courses.html', username=username)


@app.route('/profile/<username>')
def profile(username):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        "SELECT count(DISTINCT Course.CourseName) FROM Course JOIN TaughtBy ON Course.CourseID = TaughtBy.CourseID JOIN Instructor ON TaughtBy.InstructorID = Instructor.InstructorID WHERE Instructor.InstructorID = %s",
        (username,))
    count = cur.fetchall()
    count = count[0]
    images = {
        "DatabaseFundamentals": "https://ethanmesecar.tech/wp-content/uploads/2022/10/data-base-fubnd.png",
        "PythonProgramming": "https://www.digitalnest.in/blog/wp-content/uploads/2019/07/10-Benefits-of-Learning-Python-Programming-Language-and-Its-Use-Cases.png",
        "DataScienceEssentials": "https://connecteddataacademy.com/wp-content/uploads/2019/09/Data-Science-Essentials-300x157.png",
        "WebDesign": "https://kinsta.com/wp-content/uploads/2020/02/web-design-best-practices.jpg",
        "MobileAppDevelopment": "https://www.velvetech.com/wp-content/uploads/2021/08/mobile-app-development-process-tw.jpg"
    }
    cur.execute(
        "SELECT count(DISTINCT Users.UserID) FROM Users JOIN Enrollment ON Users.UserID = Enrollment.UserID JOIN Course ON Enrollment.CourseID = Course.CourseID JOIN TaughtBy ON Course.CourseID = TaughtBy.CourseID WHERE TaughtBy.InstructorID = %s",
        (username,))
    countuser = cur.fetchall()
    countuser = countuser[0]
    return render_template('profile.html', username=username, count=count, countuser=countuser)


@app.route('/update/<username>')
def updprofile(username):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('select email from credentials where id=%s', (username,))
    email = cur.fetchone()
    cur.execute('select name from credentials where id=%s', (username,))
    name = cur.fetchone()

    return render_template('update.html', name=name, email=email, username=username)


@app.route('/updatedprofile/<username>/<name>/<email>', methods=['POST'])
def updated_profile(username, name, email):
    oldpassword = request.form['old_pass']
    password = request.form['pass']

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT password FROM credentials WHERE id = %s", (username,))

    oldpass = cur.fetchone()
    oldpass = oldpass['password']
    print("Original password ", oldpass, " ", "Entered old password", oldpassword, " ", "New password", password)

    if oldpass != oldpassword:
        print("Entered wrong old password")
        return render_template('update.html', name=name, email=email, username=username)
    name = request.form['name']
    email = request.form['email']

    cur.execute("UPDATE CREDENTIALS SET NAME=%s WHERE ID=%s", (name, username))
    conn.commit()

    cur.execute("UPDATE CREDENTIALS SET EMAIL=%s WHERE ID=%s", (email, username))
    conn.commit()

    cur.execute("UPDATE CREDENTIALS SET PASSWORD=%s WHERE ID=%s", (password, username))
    conn.commit()
    print("Successfully Updated")
    return render_template('profile.html', username=username, name=name, email=email)


@app.route('/teachers/<username>')
def assessment(username):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
    SELECT Assessment.AssessmentID, Assessment.AssessmentType, Assessment.PassMarks, Assessment.TotalMarks, course.coursename
    FROM Assessment
    JOIN Course ON Assessment.CourseID = Course.CourseID
    JOIN TaughtBy ON Course.CourseID = TaughtBy.CourseID
    WHERE TaughtBy.InstructorID = %s
    """, (username,))
    data = cur.fetchall()
    return render_template('teachers.html', username=username, data=data)


@app.route('/createassessment/<username>', methods=['POST'])
def create_assessment_page(username):
    coursename = request.form.get('Course')

    return render_template('createassessment.html', username=username, coursename=coursename)


@app.route('/createassess/<username>/<coursename>', methods=['POST'])
def create_assessment(coursename, username):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT COURSEID FROM COURSE WHERE COURSENAME = %s", (coursename,))
    courseid = cur.fetchone()  # Use fetchone instead of fetchall
    courseid = courseid[0]
    asstype = request.form['asstype']
    passmarks = request.form['pm']
    totalmarks = request.form['tm']
    cur.execute("INSERT INTO ASSESSMENT (COURSEID,ASSESSMENTTYPE,PASSMARKS,TOTALMARKS) VALUES (%s,%s,%s,%s)",
                (courseid, asstype, passmarks, totalmarks))
    conn.commit()
    cur.execute("""
        SELECT Assessment.AssessmentID, Assessment.AssessmentType, Assessment.PassMarks, Assessment.TotalMarks, course.coursename
        FROM Assessment
        JOIN Course ON Assessment.CourseID = Course.CourseID
        JOIN TaughtBy ON Course.CourseID = TaughtBy.CourseID
        WHERE TaughtBy.InstructorID = %s
        """, (username,))
    data = cur.fetchall()
    return render_template('teachers.html', username=username, data=data)


# User:


@app.route('/usercredentials', methods=['POST'])
def add_usercredentials():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    username = request.form['username']
    name = request.form['name']
    email = request.form['email']
    password = request.form['pass']
    qualification = request.form['qual']
    cur.execute("INSERT INTO users (UserID , Name, Email , Password, Role) VALUES (%s,%s,%s,%s,%s)",(username, name, email, password, qualification))
    conn.commit()

    print('Student Added successfully')
    return render_template('userlogin.html')


@app.route('/userlogin', methods=['POST'])
def uservalidate():
    username = request.form['username']
    password = request.form['pass']

    # Check if the username exists
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT userid, password FROM users WHERE userid = %s", (username,))
    user_data = cur.fetchone()

    if user_data is None or user_data['userid'] != username:
        print('Username not exists')
        return render_template('login.html')

    # Check if the password matches (assuming passwords are stored as plaintext)
    if password != user_data['password']:
        print('Wrong Password')
        return render_template('login.html')

    # Successful login
    print(username, " logged in")
    cur.execute("""
    
    """,(username,))
    list_courses = cur.fetchall()
    print(list_courses)
    images = {
        "Database Fundamentals": "https://ethanmesecar.tech/wp-content/uploads/2022/10/data-base-fubnd.png",
        "Python Programming": "https://www.digitalnest.in/blog/wp-content/uploads/2019/07/10-Benefits-of-Learning-Python-Programming-Language-and-Its-Use-Cases.png",
        "Data Science Essentials": "https://connecteddataacademy.com/wp-content/uploads/2019/09/Data-Science-Essentials-300x157.png",
        "Web Design": "https://kinsta.com/wp-content/uploads/2020/02/web-design-best-practices.jpg",
        "Mobile App Development": "https://www.velvetech.com/wp-content/uploads/2021/08/mobile-app-development-process-tw.jpg"
    }
    return render_template('userhome.html', username=username, list_courses=list_courses, images=images)


@app.route('/userloginpage')
def userlogin_page():
    return render_template('userlogin.html')

@app.route('/userhome/<username>')
def getuserhome(username):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
    
    """,(username,))
    list_courses = cur.fetchall()
    images = {
        "DatabaseFundamentals": "https://ethanmesecar.tech/wp-content/uploads/2022/10/data-base-fubnd.png",
        "PythonProgramming": "https://www.digitalnest.in/blog/wp-content/uploads/2019/07/10-Benefits-of-Learning-Python-Programming-Language-and-Its-Use-Cases.png",
        "DataScienceEssentials": "https://connecteddataacademy.com/wp-content/uploads/2019/09/Data-Science-Essentials-300x157.png",
        "WebDesign": "https://kinsta.com/wp-content/uploads/2020/02/web-design-best-practices.jpg",
        "MobileAppDevelopment": "https://www.velvetech.com/wp-content/uploads/2021/08/mobile-app-development-process-tw.jpg"
    }
    return render_template('userhome.html', username=username, list_courses=list_courses, images=images)


@app.route('/userteacherprofile')
def userteacherprof():
    return render_template('userteacher_profile.html')


@app.route('/usercourses/<username>')
def userget_course(username):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
    SELECT DISTINCT Course.CourseID, Course.CourseName, Course.CourseDescription, Course.CourseDuration, Course.CourseFee
    FROM Course
    JOIN Enrollment ON Course.CourseID = Enrollment.CourseID
    JOIN Users ON Enrollment.UserID = Users.UserID
    WHERE Users.UserID = %s
    """,(username,))
    list_users = cur.fetchall()
    images = {
        "DatabaseFundamentals": "https://ethanmesecar.tech/wp-content/uploads/2022/10/data-base-fubnd.png",
        "PythonProgramming": "https://www.digitalnest.in/blog/wp-content/uploads/2019/07/10-Benefits-of-Learning-Python-Programming-Language-and-Its-Use-Cases.png",
        "DataScienceEssentials": "https://connecteddataacademy.com/wp-content/uploads/2019/09/Data-Science-Essentials-300x157.png",
        "WebDesign": "https://kinsta.com/wp-content/uploads/2020/02/web-design-best-practices.jpg",
        "MobileAppDevelopment": "https://www.velvetech.com/wp-content/uploads/2021/08/mobile-app-development-process-tw.jpg"
    }
    print(list_users)
    return render_template('usercourses.html', username=username, list_users=list_users, images=images)


@app.route('/userplaylist/<username>')
def userget_instructor_list(username):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        "SELECT DISTINCT Users.UserID, Users.Name, Users.Email,Course.Coursename FROM Users JOIN Enrollment ON Users.UserID = Enrollment.UserID JOIN Course ON Enrollment.CourseID = Course.CourseID JOIN TaughtBy ON Course.CourseID = TaughtBy.CourseID WHERE TaughtBy.InstructorID = %s",
        (username,))
    list_users = cur.fetchall()
    return render_template('userplaylist.html', username=username, list_users=list_users)


@app.route('/useraboutcourse/<coursename>/<username>')
def userget_course_details(coursename, username):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print(coursename)
    cur.execute("SELECT coursename,coursedescription,courseduration,coursefee FROM COURSE WHERE COURSENAME = %s",
                (coursename,))
    course_details = cur.fetchall()
    return render_template('useraboutcourse.html', course_details=course_details, username=username, coursename=coursename)


@app.route('/usergetresources/<username>/<coursename>')
def userredirect_resource(username, coursename):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT COURSEID FROM COURSE WHERE COURSENAME = %s', (coursename,))
    id = cur.fetchone()
    if id:
        courseid = id[0]
    cur.execute('SELECT * FROM resource WHERE courseid = %s', (courseid,))
    data = cur.fetchall()
    cur.close()
    return render_template('userresources.html', username=username, coursename=coursename, data=data)


@app.route('/getsresource/<coursename>/<username>', methods=['POST'])
def userget_resource(coursename, username):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM COURSE WHERE COURSENAME = %s", (coursename,))
    course_data = cur.fetchone()

    courseid = course_data['courseid']  # Adjust this based on the actual column name
    restype = request.form['restype']
    reslink = request.form['reslink']
    resname = request.form['resname']
    upldate = date.today()

    cur.execute(
        "INSERT INTO RESOURCE(courseid,resourcetype,resourcelink,resourcename,uploaddate) VALUES(%s,%s,%s,%s,%s)",
        (courseid, restype, reslink, resname, upldate))
    conn.commit()

    return render_template('usercourses.html', username=username)


@app.route('/userviewresource/<username>/<coursename>', methods=['GET', 'POST'])
def userview(username, coursename):
    if request.method == 'POST':
        # Handle POST request logic if needed
        pass
    else:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT COURSEID FROM COURSE WHERE COURSENAME = %s', (coursename,))
        id = cur.fetchone()
        if id:
            courseid = id[0]
        cur.execute('SELECT * FROM resource WHERE courseid = %s', (courseid,))
        data = cur.fetchall()
        cur.close()

        return render_template('userresources.html', coursename=coursename, username=username, data=data)


@app.route('/usergetschedule/<username>/<coursename>')
def userget_schedule(username, coursename):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT COURSEID FROM COURSE WHERE COURSENAME = %s", (coursename,))
    id = cur.fetchone()  # Use fetchone instead of fetchall
    if id:
        courseid = id[0]
    cur.execute("SELECT DATE,TIME,LOCATION,scheduleid FROM SCHEDULE WHERE COURSEID=%s", (courseid,))
    data = cur.fetchall()
    return render_template('userschedule.html', username=username, coursename=coursename, data=data)


@app.route('/getscheduledetails/<username>/<coursename>', methods=['POST'])
def userget_scheduledetails(username, coursename):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT COURSEID FROM COURSE WHERE COURSENAME = %s", (coursename,))
    id = cur.fetchone()  # Use fetchone instead of fetchall
    if id:
        courseid = id[0]
    date = request.form['date']
    time = request.form['time']
    loc = request.form['loc']
    cur.execute("INSERT INTO Schedule (CourseID, Date, Time, Location) VALUES (%s,%s,%s,%s)",
                (courseid, date, time, loc,))
    conn.commit()
    cur.execute("SELECT DATE,TIME,LOCATION,scheduleid FROM SCHEDULE WHERE COURSEID=%s", (courseid,))
    data = cur.fetchall()

    return render_template('userschedule.html', username=username, coursename=coursename, data=data)



@app.route('/userenroll/<username>/<coursename>')
def userenroll(username, coursename):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT COURSEID FROM COURSE WHERE COURSENAME = %s", (coursename,))
    courseid = cur.fetchone()  # Use fetchone instead of fetchall
    enrdate = date.today()
    courseid = courseid[0]
    cur.execute("INSERT INTO enrollment (UserID, CourseID, EnrollmentDate, EnrollmentStatus) VALUES(%s, %s,%s,'active')", (username,courseid,enrdate))
    conn.commit()
    return render_template('usercourses.html', username=username)


@app.route('/userprofile/<username>')
def userprofile(username):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        "SELECT count(DISTINCT Course.CourseName) FROM Course JOIN TaughtBy ON Course.CourseID = TaughtBy.CourseID JOIN Instructor ON TaughtBy.InstructorID = Instructor.InstructorID WHERE Instructor.InstructorID = %s",
        (username,))
    count = cur.fetchall()
    count = count[0]
    images = {
        "DatabaseFundamentals": "https://ethanmesecar.tech/wp-content/uploads/2022/10/data-base-fubnd.png",
        "PythonProgramming": "https://www.digitalnest.in/blog/wp-content/uploads/2019/07/10-Benefits-of-Learning-Python-Programming-Language-and-Its-Use-Cases.png",
        "DataScienceEssentials": "https://connecteddataacademy.com/wp-content/uploads/2019/09/Data-Science-Essentials-300x157.png",
        "WebDesign": "https://kinsta.com/wp-content/uploads/2020/02/web-design-best-practices.jpg",
        "MobileAppDevelopment": "https://www.velvetech.com/wp-content/uploads/2021/08/mobile-app-development-process-tw.jpg"
    }
    cur.execute(
        "SELECT count(DISTINCT Users.UserID) FROM Users JOIN Enrollment ON Users.UserID = Enrollment.UserID JOIN Course ON Enrollment.CourseID = Course.CourseID JOIN TaughtBy ON Course.CourseID = TaughtBy.CourseID WHERE TaughtBy.InstructorID = %s",
        (username,))
    countuser = cur.fetchall()
    countuser = countuser[0]
    return render_template('userprofile.html', username=username, count=count, countuser=countuser)


@app.route('/userupdate/<username>')
def userupdprofile(username):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('select email from credentials where id=%s', (username,))
    email = cur.fetchone()
    cur.execute('select name from credentials where id=%s', (username,))
    name = cur.fetchone()

    return render_template('userupdate.html', name=name, email=email, username=username)


@app.route('/userupdatedprofile/<username>/<name>/<email>', methods=['POST'])
def userupdated_profile(username, name, email):
    oldpassword = request.form['old_pass']
    password = request.form['pass']

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT password FROM credentials WHERE id = %s", (username,))

    oldpass = cur.fetchone()
    oldpass = oldpass['password']
    print("Original password ", oldpass, " ", "Entered old password", oldpassword, " ", "New password", password)

    if oldpass != oldpassword:
        print("Entered wrong old password")
        return render_template('update.html', name=name, email=email, username=username)
    name = request.form['name']
    email = request.form['email']

    cur.execute("UPDATE CREDENTIALS SET NAME=%s WHERE ID=%s", (name, username))
    conn.commit()

    cur.execute("UPDATE CREDENTIALS SET EMAIL=%s WHERE ID=%s", (email, username))
    conn.commit()

    cur.execute("UPDATE CREDENTIALS SET PASSWORD=%s WHERE ID=%s", (password, username))
    conn.commit()
    print("Successfully Updated")
    return render_template('userprofile.html', username=username, name=name, email=email)


@app.route('/userteachers/<username>')
def user_assessment(username):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
    SELECT Assessment.AssessmentID, Assessment.AssessmentType, Assessment.PassMarks, Assessment.TotalMarks, course.coursename
    FROM Assessment
    JOIN Course ON Assessment.CourseID = Course.CourseID
    JOIN TaughtBy ON Course.CourseID = TaughtBy.CourseID
    WHERE TaughtBy.InstructorID = %s
    """, (username,))
    data = cur.fetchall()
    return render_template('userteachers.html', username=username, data=data)
