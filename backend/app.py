from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

#database
def init_db():
    conn = sqlite3.connect("jobportal.db")
    cursor = conn.cursor()

    #user db
    cursor.execute(""" CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   email TEXT,
                   password TEXT,
                   role TEXT)""")
    #jobs table
    cursor.execute(""" CREATE TABLE IF NOT EXISTS jobs(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT,
                   company TEXT,
                   salary TEXT,
                   description TEXT)""")
    #application table
    cursor.execute("""CREATE TABLE IF NOT EXISTS applications(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   job_id INTEGER )""")
    conn.commit()
    conn.close()

#insert demo jobs
def insert_job():
    conn = sqlite3.connect("jobportal.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*)FROM jobs")
    count = cursor.fetchone()[0]
    
    if count ==0:
        jobs = [
            ("Frontend Developer", "TCS", "6 LPA", "React, HTML, CSS"),
            ("Python Developer", "Infosys", "5 LPA", "Flask, APIs"),
            ("Full Stack Developer", "Wipro", "7 LPA", "React + Python"),
            ("Backend Developer", "Zoho", "8 LPA", "Python, Django, REST API"),
            ("Data Analyst", "Accenture", "6.5 LPA", "Excel, SQL, Power BI"),
            ("Machine Learning Engineer", "IBM", "10 LPA", "Python, ML, AI"),
            ("DevOps Engineer", "Tech Mahindra", "9 LPA", "AWS, Docker, CI/CD"),
            ("UI/UX Designer", "Capgemini", "5 LPA", "Figma, Adobe XD"),
            ("Software Engineer", "HCL", "6 LPA", "Java, DSA, Problem Solving"),
            ("Cloud Engineer", "Amazon", "12 LPA", "AWS, Cloud Computing")
            ]
        cursor.executemany("INSERT INTO jobs(title,company,salary,description)VALUES(?,?,?,?)",jobs)
        conn.commit()
    conn.close()
init_db()
insert_job()

#register
@app.route("/register", methods =["POST"])
def register():
    data =  request.json

    conn = sqlite3.connect("jobportal.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (name, email, password, role) VALUES (?,?,?,?)",(data.get("name"),data.get("email"),data.get("password"),data.get("role")))
    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully"})

#login
@app.route("/login" , methods = ["POST"])
def login():
    data = request.json
    conn = sqlite3.connect("jobportal.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email =? AND password = ?", (data.get("email"),data.get("password")) )
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            "message": "Login Successful",
            "user_name" : user[1],
            "user_id" : user[0],
            "role" : user[4]
        })
    else:
         return jsonify({"message": "Invalid credentials"}), 401
    
#get jobs
@app.route ("/jobs", methods =["GET"])
def get_jobs():
    conn = sqlite3.connect("jobportal.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()
    conn.close()

    job_list= []
    for job in jobs:
        job_list.append({
            "id":job[0],
            "title": job[1],
            "company": job[2],
            "salary": job[3],
            "description": job[4]
        })
    return jsonify(job_list)

#apply job
@app.route ("/apply" , methods = ["POST"])
def apply_job():
    data = request.json

    conn = sqlite3.connect("jobportal.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO applications (user_id,job_id)VALUES (?, ?)",(data.get("user_id"),data.get("job_id")))
    conn.commit()
    conn.close()
    return jsonify({"message" :"Applied Successfully "})

# view applications
@app.route ("/applications/<int:user_id>", methods = ["GET"])
def get_applications(user_id):
    conn = sqlite3.connect("jobportal.db")
    cursor = conn.cursor()

    cursor.execute(""" SELECT jobs.title, jobs.company 
                   FROM applications 
                   JOIN jobs ON applications.job_id = jobs.id
                   WHERE applications.user_id = ? """,(user_id,))
    
    data = cursor.fetchall()
    conn.close()

    result = []
    for row in data:
        result.append({
            "title":row[0],
            "company":row[1]
        })
    return jsonify(result)
    
if __name__ == "__main__":
    app.run(debug=True)
