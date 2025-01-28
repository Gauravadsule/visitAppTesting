from flask import Blueprint, render_template_string
from db import get_db_connection

all_visitors = Blueprint("all_visitors", __name__)

@all_visitors.route('/all_visitors', methods=['GET'])
def view_all_visitors():
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
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] }}</td>
            <td>{{ row[4] }}</td>
            <td>{{ row[5] }}</td>
        </tr>
        {% endfor %}
    </table>
    <br><a href="/">Back to Home</a>
    """, rows=rows)