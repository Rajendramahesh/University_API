from flask import Flask, render_template, request, redirect


app = Flask(__name__)
@app.route('/')
def home():
    return "hello !, this is home page" 

@app.route('/about')
def about():
    return "This is about page"


@app.route('/contact')
def conact():
    return "This is contact page"

@app.route('/hello/<name>')
def hello(name):
    return f"Hello {name}, welcome to our website!"

@app.route('/square/<int:number>')
def square(number):
    res = number**2
    return f"The square of {number} is {res}"

@app.route('/greet/<name>')
def greet(name):
    return render_template('index.html',nam = name)

# Sample data for demonstration
students_list = [f"Student {i}" for i in range(1, 51)]  # 50 students


@app.route('/students')
def show_students():
    page = int(request.args.get('page', 1))
    search_query = request.args.get('search', '').lower()
    page_size = 10

    # Filter students if search_query exists
    if search_query:
        filtered_students = [s for s in students_list if search_query in s.lower()]
    else:
        filtered_students = students_list

    # Pagination logic
    start = (page - 1) * page_size
    end = start + page_size
    paginated_students = filtered_students[start:end]
    total_pages = (len(filtered_students) + page_size - 1) // page_size

    return render_template('students.html', 
                           students=paginated_students,
                           page=page, 
                           total_pages=total_pages,
                           search=search_query)

@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        students_list.append(name)
        return redirect('/students')
    
    # If it's a GET request
    return render_template('add_student.html')


if __name__ == '__main__':
    app.run(debug=True)