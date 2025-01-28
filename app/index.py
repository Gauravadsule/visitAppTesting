from flask import Flask, render_template_string, request, redirect
from db import get_db_connection
from datetime import datetime

app = Flask(__name__)

# Home Page
@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Visitor Management</title>
    </head>
    <body>
        <h1>Visitor Management System - Sycatel</h1>
        <ul>
            <li><a href="/add_visitor">Add New Visitor</a></li>
            <li><a href="/all_visitors">View All Visitors</a></li>
            <li><a href="/filter_visitors">Filter Visitors by Reason</a></li>
        </ul>
    </body>
    </html>
    """)

# Add Visitor
@app.route('/add_visitor', methods=['GET', 'POST'])
def add_visitor():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form.get('email')
        contact_person = request.form.get('contact_person')
        visit_reason = request.form['visit_reason']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
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
# View All Visitors
@app.route('/all_visitors', methods=['GET'])
def all_visitors():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM visitors")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        return f"An error occurred: {e}"

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>All Visitors</title>
    </head>
    <body>
        <h1>All Visitors</h1>
        <table border="1">
            <tr>
                <th>Name</th>
                <th>Mobile</th>
                <th>Email</th>
                <th>Contact Person</th>
                <th>Visit Reason</th>
                <th>Timestamp</th>
            </tr>
            {% for row in rows %}
            <tr>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
                <td>{{ row[3] }}</td>
                <td>{{ row[4] }}</td>
                <td>{{ row[5] }}</td>
                <td>{{ row[6] }}</td>
            </tr>
            {% endfor %}
        </table>
        <br>
        <a href="/">Back to Home</a>
    </body>
    </html>
    """, rows=rows)

# Filter Visitors by Reason
@app.route('/filter_visitors', methods=['GET', 'POST'])
def filter_visitors():
    rows = []
    visit_reason = None
    
    if request.method == 'POST':
        visit_reason = request.form.get('visit_reason')
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM visitors WHERE visit_reason = %s", (visit_reason,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            return f"An error occurred: {e}"

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Visitors by Reason</title>
    </head>
    <body>
        <h1>Filter Visitors by Reason</h1>
        <form action="/filter_visitors" method="post">
            <label for="visit_reason">Reason for Visit:</label>
            <select id="visit_reason" name="visit_reason">
                <option value="purchasing" {% if visit_reason == "purchasing" %}selected{% endif %}>Purchasing</option>
                <option value="enquiry" {% if visit_reason == "enquiry" %}selected{% endif %}>Enquiry</option>
                <option value="dispute" {% if visit_reason == "dispute" %}selected{% endif %}>Dispute</option>
                <option value="meeting" {% if visit_reason == "meeting" %}selected{% endif %}>Meeting</option>
                <option value="presentation" {% if visit_reason == "presentation" %}selected{% endif %}>Presentation</option>
                <option value="others" {% if visit_reason == "others" %}selected{% endif %}>Others</option>
            </select><br>
            <input type="submit" name="filter" value="Filter">
        </form>

        {% if rows %}
        <table border="1">
            <tr>
                <th>Name</th>
                <th>Mobile</th>
                <th>Email</th>
                <th>Contact Person</th>
                <th>Visit Reason</th>
                <th>Timestamp</th>
            </tr>
            {% for row in rows %}
            <tr>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
                <td>{{ row[3] }}</td>
                <td>{{ row[4] }}</td>
                <td>{{ row[5] }}</td>
                <td>{{ row[6] }}</td>
            </tr>
            {% endfor %}
        </table>
        {% endif %}
        
        <br>
        <a href="/">Back to Home</a>
    </body>
    </html>
    """, rows=rows, visit_reason=visit_reason)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
