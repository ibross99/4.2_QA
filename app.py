# app.py

import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)
app.config['DATABASE'] = 'project_requests.db'

# --- Database Connection Handling ---

def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Return rows as dictionaries
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    """
    Closes the database again at the end of the request.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

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
    
    # Fetch the current record to prepopulate the form
    record = db.execute("SELECT * FROM requests WHERE id = ?", (id,)).fetchone()
    projects = ["Pro1", "Pro2", "Pro3"]
    return render_template('update.html', record=record, projects=projects)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_request(id):
    db = get_db()
    db.execute("DELETE FROM requests WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for('index'))

# NOTE: The if __name__ == '__main__' block has been removed.
# A production WSGI server like Gunicorn will be used to run the app.