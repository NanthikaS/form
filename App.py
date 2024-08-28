
from flask import Flask, request, render_template
from datetime import datetime
import sqlite3

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form['name']
    dob = request.form['dob']
    
    dob_date = datetime.strptime(dob, '%Y-%m-%d')
    today = datetime.today()
    age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))

    if age < 18:
        # Return the form with an error message
        return render_template('form.html', error="You must be at least 18 years old to register.")
    
    # Store data in the database
    conn = sqlite3.connect('database/students.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (name, dob) VALUES (?, ?)", (name, dob))
    conn.commit()
    conn.close()

    # Return a styled success message
    return '''
    <html>
    <body style="
        display: flex; 
        justify-content: center; 
        align-items: center; 
        height: 100vh;
        margin: 0;
        background-color: #EBD3F8; 
        color: #4b0082;
        font-family: Arial, sans-serif; 
    ">
        <div style="
            text-align: center; 
            font-size: 55px; 
            font-weight: bold; 
            font-style: italic;
        ">
            Thanks for your submission!
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
