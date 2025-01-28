from flask import Flask, render_template_string, request, redirect
from db import get_db_connection  # Assuming get_db_connection is defined in db.py
from datetime import datetime

app = Flask(__name__)

@app.route('/add_visitor', methods=['GET', 'POST'])
def add_visitor():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form.get('email')
        contact_person = request.form.get('contact_person')
        visit_reason = request.form['visit_reason']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            # Database operations
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO visitors 
                (name, mobile, email, contact_person, visit_reason, timestamp) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, mobile, email, contact_person, visit_reason, timestamp))
            conn.commit()
            cursor.close()
            conn.close()
            return "Visitor added successfully! <br> <a href='/'>Back to Home</a>"
        except Exception as e:
            return f"An error occurred: {e}"

    # Render form for GET request
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Add Visitor</title>
    </head>
    <body>
        <h1>Add New Visitor</h1>
        <form action="" method="post">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required><br>

            <label for="mobile">Mobile No.:</label>
            <input type="text" id="mobile" name="mobile" required><br>

            <label for="email">Email:</label>
            <input type="email" id="email" name="email"><br>

            <label for="contact_person">Contact Person Name:</label>
            <input type="text" id="contact_person" name="contact_person"><br>

            <label for="visit_reason">Reason for Visit:</label>
            <select id="visit_reason" name="visit_reason">
                <option value="purchasing">Purchasing</option>
                <option value="enquiry">Enquiry</option>
                <option value="dispute">Dispute</option>
                <option value="meeting">Meeting</option>
                <option value="presentation">Presentation</option>
                <option value="others">Others</option>
            </select><br>

            <input type="submit" name="submit" value="Add Visitor">
        </form>
        <br>
        <a href="/">Back to Home</a>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
