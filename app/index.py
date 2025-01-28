from flask import Flask, render_template_string
from add_visitor import add_visitor
from fetch_all import all_visitors
from fetch_by_reason import filter_visitors

app = Flask(__name__)

# Registering the routes from other modules
app.register_blueprint(add_visitor, url_prefix="")
app.register_blueprint(all_visitors, url_prefix="")
app.register_blueprint(filter_visitors, url_prefix="")

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)