from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firstapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model
class Student(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'{self.sno} - {self.fname}'

# Home + Add
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        age = int(request.form['age'])
        city = request.form['city']
        new_student = Student(fname=fname, lname=lname, age=age, city=city)
        db.session.add(new_student)
        db.session.commit()
        return redirect('/')
    
    students = Student.query.all()
    return render_template('index.html', students=students)

# Delete
@app.route('/delete/<int:sno>')
def delete_student(sno):
    student = Student.query.get_or_404(sno)
    db.session.delete(student)
    db.session.commit()
    return redirect('/')

# Edit
@app.route('/edit/<int:sno>', methods=['GET', 'POST'])
def edit_student(sno):
    student = Student.query.get_or_404(sno)
    if request.method == 'POST':
        student.fname = request.form['fname']
        student.lname = request.form['lname']
        student.age = request.form['age']
        student.city = request.form['city']
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', student=student)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
