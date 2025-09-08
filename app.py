# app.py

import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)
DATABASE = 'project_requests.db'

def get_db():
    """Opens a new database connection for the current request."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row # Allows accessing columns by name
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Closes the database at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database and creates the table if it doesn't exist."""
    with app.app_context():
        db = get_db()
        with open('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# --- Routes ---

@app.route('/')
def index():
    db = get_db()
    records = db.execute("SELECT * FROM requests").fetchall()
    return render_template('index.html', records=records)

@app.route('/add', methods=['GET', 'POST'])
def add_request():
    if request.method == 'POST':
        name = request.form['name']
        reason = request.form['reason']
        project = request.form['project']
        
        db = get_db()
        db.execute(
            "INSERT INTO requests (name, reason, project) VALUES (?, ?, ?)",
            (name, reason, project)
        )
        db.commit()
        return redirect(url_for('index'))
    
    projects = ["Pro1", "Pro2", "Pro3"]
    return render_template('add.html', projects=projects)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_request(id):
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        reason = request.form['reason']
        project = request.form['project']
        
        db.execute(
            "UPDATE requests SET name = ?, reason = ?, project = ? WHERE id = ?",
            (name, reason, project, id)
        )
        db.commit()
        return redirect(url_for('index'))
    
    record = db.execute("SELECT * FROM requests WHERE id = ?", (id,)).fetchone()
    projects = ["Pro1", "Pro2", "Pro3"]
    return render_template('update.html', record=record, projects=projects)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_request(id):
    db = get_db()
    db.execute("DELETE FROM requests WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for('index'))

# --- Main execution block to run the development server ---
if __name__ == '__main__':
    # Initialize the database when the app starts
    init_db()
    # Run the Flask development server
    app.run(host='0.0.0.0', port=5500, debug=True)