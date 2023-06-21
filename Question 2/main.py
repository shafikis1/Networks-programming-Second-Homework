from flask import Flask, render_template, request
app = Flask(__name__)

#loading main html page
@app.route('/')
def index():
    return render_template('index.html')

#handling form data
@app.route('/students', methods =["POST"])
def handle_input():
       # getting input with name = fname in HTML form
       student_name = request.form.get("studentname")
       # getting input with name = lname in HTML form
       student_number = request.form.get("studentnumber")
       return render_template("more.html", name=student_name)

if __name__ == '__main__' :
    #running flask app
    app.run(port=9999)