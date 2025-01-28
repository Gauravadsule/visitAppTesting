from flask import Flask, render_template_string, request
from db import get_db_connection  # Assuming get_db_connection is defined in db.py

app = Flask(__name__)

@app.route('/filter_visitors', methods=['GET', 'POST'])
def filter_visitors():
    rows = []
    visit_reason = None
    
    if request.method == 'POST':
        visit_reason = request.form.get('visit_reason')
        try:
            # Query visitors by the selected reason
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM visitors WHERE visit_reason = %s", (visit_reason,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            return f"An error occurred: {e}"

    # Render the page with a form and results
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
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
                <td>{{ row[3] }}</td>
                <td>{{ row[4] }}</td>
                <td>{{ row[5] }}</td>
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
