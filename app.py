from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize and create the database if it doesn't exist
def init_db():
    conn = sqlite3.connect('project_requests.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS requests
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 reason TEXT NOT NULL,
                 project TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Route to show the list of all entries
@app.route('/')
def index():
    conn = sqlite3.connect('project_requests.db')
    c = conn.cursor()
    c.execute("SELECT * FROM requests")
    records = c.fetchall()
    conn.close()
    return render_template('index.html', records=records)

# Route to add a new request
@app.route('/add', methods=['GET', 'POST'])
def add_request():
    if request.method == 'POST':
        name = request.form['name']
        reason = request.form['reason']
        project = request.form['project']
        
        conn = sqlite3.connect('project_requests.db')
        c = conn.cursor()
        c.execute("INSERT INTO requests (name, reason, project) VALUES (?, ?, ?)", (name, reason, project))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    
    projects = ["Pro1", "Pro2", "Pro3"]
    return render_template('add.html', projects=projects)

# Route to update an existing request
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_request(id):
    conn = sqlite3.connect('project_requests.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        reason = request.form['reason']
        project = request.form['project']
        
        c.execute("UPDATE requests SET name = ?, reason = ?, project = ? WHERE id = ?", (name, reason, project, id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    
    # Fetch the current record to prepopulate the form
    c.execute("SELECT * FROM requests WHERE id = ?", (id,))
    record = c.fetchone()
    conn.close()

    projects = ["Pro1", "Pro2", "Pro3"]
    return render_template('update.html', record=record, projects=projects)

# Route to delete a request
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_request(id):
    conn = sqlite3.connect('project_requests.db')
    c = conn.cursor()
    c.execute("DELETE FROM requests WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(host='0.0.0.0', port=5500, debug =True)
 