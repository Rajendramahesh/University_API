from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)




# Home page route
@app.route('/')
def home():
    return render_template('api_project_home.html')

# API route to get student data with pagination 
@app.route('/students', methods=['GET'])
def get_students():
    try:
        # Connect to the database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        # Get page and page_size from query parameters, with defaults
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))

        # Get total count
        cursor.execute("SELECT COUNT(*) as total FROM student")
        total_count = cursor.fetchone()['total']
        
        # Calculate total pages
        total_pages = (total_count + page_size - 1) // page_size

        # Validate page number
        if page < 1 or page > total_pages:
            return jsonify({
                "code": 0,
                "msg": f"Page out of range. Total pages: {total_pages}",
                "data": None
            })

        offset = (page - 1) * page_size

        # JOIN query to get student + course info
        cursor.execute("""
            SELECT 
                s.ID AS student_id,
                s.name AS student_name,
                s.dept_name,
                t.course_id,
                t.sec_id AS section_id,
                t.semester,
                t.year
            FROM student s
            LEFT JOIN takes t ON s.ID = t.ID
            ORDER BY s.ID LIMIT %s OFFSET %s
        """, (page_size, offset))

        rows = cursor.fetchall()
        conn.close()
        
        # Structure the output
        student_dict = {}

        for row in rows:
            sid = row['student_id']
            if sid not in student_dict:
                student_dict[sid] = {
                    "id": sid,
                    "name": row['student_name'],
                    "dept_name": row['dept_name'],
                    "courses": []
                }

            # Only add course if exists (in case of LEFT JOIN where no course)
            if row['course_id']:
                student_dict[sid]["courses"].append({
                    "course_id": row['course_id'],
                    "section_id": row['section_id'],
                    "semester": row['semester'],
                    "year": row['year']
                })

        
        
        response = {
                "code": 1,
                "msg": "Success",
                "data": {
                    "records": list(student_dict.values()),
                    "total": len(student_dict)
                }
            }
    
    except Exception as e:
        response = {
            "code": 0,
            "msg": "Error",
            "data": None
        }
        print("Error:", e)

    return jsonify(response) 
# Test the response with url like: /students?page=1&page_size=5

# API route to get department data with pagination
@app.route('/departments', methods=['GET'])
def get_departments():
    try:
            # Connect to the database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            # Get page and page_size from query parameters, with defaults
            page = int(request.args.get('page', 1))
            page_size = int(request.args.get('page_size', 10))

            # Get total count
            cursor.execute("SELECT COUNT(*) as total FROM department")
            total_count = cursor.fetchone()['total']
            
            # Calculate total pages
            total_pages = (total_count + page_size - 1) // page_size

            # Validate page number
            if page < 1 or page > total_pages:
                return jsonify({
                    "code": 0,
                    "msg": f"Page out of range. Total pages: {total_pages}",
                    "data": None
                })

            offset = (page - 1) * page_size

            # JOIN query to get department and instructor info
            cursor.execute("""
                SELECT 
                   d.dept_name, 
                   d.building,
                   d.budget, 
                   i.id, i.name, 
                   i.salary
                FROM department d 
                LEFT JOIN instructor i ON d.dept_name = i.dept_name
                LIMIT %s OFFSET %s
            """, (page_size, offset))

            rows = cursor.fetchall()
            conn.close()
            
            # Structure the output
            department_dict = {}

            for row in rows:
                dpname = row['dept_name']
                if dpname not in department_dict:
                    department_dict[dpname] = {
                        "dep_name": dpname,
                        "building": row['building'],
                        "budget": row['budget'],
                        "instructors": []
                    }

                # Only add instructor if exists (in case of LEFT JOIN where no course)
                if row['id']:
                    department_dict[dpname]["instructors"].append({
                        "id": row['id'],
                        "name": row['name'],
                        "salary": row['salary']
                    })

            
            
            response = {
                    "code": 1,
                    "msg": "Success",
                    "data": {
                        "records": list(department_dict.values()),
                        "total": len(department_dict)
                    }
                }
    
    except Exception as e:
        response = {
            "code": 0,
            "msg": "Error",
            "data": None
        }
        print("Error:", e)

    return jsonify(response)
# Test the response with url like: /departments?page=1&page_size=5

# API route to get course data with pagination
@app.route('/courses', methods=['GET'])
def courses():
    try:
            # Connect to the database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            # Get page and page_size from query parameters, with defaults
            page = int(request.args.get('page', 1))
            page_size = int(request.args.get('page_size', 10))

            # Get total count
            cursor.execute("SELECT COUNT(*) as total FROM course")
            total_count = cursor.fetchone()['total']
            
            # Calculate total pages
            total_pages = (total_count + page_size - 1) // page_size

            # Validate page number
            if page < 1 or page > total_pages:
                return jsonify({
                    "code": 0,
                    "msg": f"Page out of range. Total pages: {total_pages}",
                    "data": None
                })

            offset = (page - 1) * page_size

            # JOIN query to get course and instructor info
            cursor.execute("""
                SELECT 
                    c.course_id,
                    c.title,
                    c.dept_name,
                    i.ID AS instructor_id,
                    i.name,
                    s.sec_id AS section,
                    s.semester,
                    s.year
                FROM course c
                LEFT JOIN instructor i ON c.dept_name = i.dept_name
                LEFT JOIN section s ON c.course_id = s.course_id
                LIMIT %s OFFSET %s
            """, (page_size, offset))

            rows = cursor.fetchall()
            conn.close()
            
            # Structure the output
            course_dict = {}

            for row in rows:
                cid = row['course_id']
                if cid not in course_dict:
                    course_dict[cid] = {
                        "course_id": cid,
                        "title": row['title'],
                        "dept_name": row['dept_name'],
                        "instructors": []
                    }

                # Only add instructor if exists (in case of LEFT JOIN where no course)
                if row['instructor_id']:
                    course_dict[cid]["instructors"].append({
                        "instructor_id": row['instructor_id'],
                        "name": row['name'],
                        "section": row['section'],
                        "semester": row['semester'],
                        "year": row['year']
                    })

            
            
            response = {
                    "code": 1,
                    "msg": "Success",
                    "data": {
                        "records": list(course_dict.values()),
                        "total": len(course_dict)
                    }
                }
    
    except Exception as e:
        response = {
            "code": 0,
            "msg": "Error",
            "data": None
        }
        print("Error:", e)

    return jsonify(response)
# Test the response with url like: /courses?page=1&page_size=5



if __name__ == '__main__':
    app.run(debug=True)