from flask import Flask , render_template , url_for , request , redirect
import sqlite3 as sq

def db_init():
    conn = sq.connect('todo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              description TEXT NOT NULL,
              status INTEGER DEFAULT 0,
              date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              due_date DATE,
              priority TEXT DEFAULT 'Normal' )''')
    conn.commit()
    conn.close()

db_init()

app = Flask(__name__)

@app.route('/',methods = ['POST','GET'])
def home():
    conn = sq.connect('todo.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.commit()
    conn.close()
    return render_template('index.html',tasks = tasks)

@app.route('/add' , methods = ['POST'])
def add_task():
    title = request.form['title']
    desc = request.form['desc']
    due_date = request.form.get('due_date', None) if "due_date" in request.form else None
    priority = request.form.get('priority','normal')
    conn = sq.connect('todo.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (title,description,due_date,priority) VALUES(?,?,?,?) ',(title,desc,due_date,priority))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/toggle',methods = ['POST','GET'])
def toggle():
    task_id = request.form['task_id']
    conn = sq.connect('todo.db')
    c = conn.cursor()
    c.execute('SELECT status from tasks WHERE id = ?',(task_id,))
    result = c.fetchone()
    if result is not None :
        curr_status = result[0]  # this zero is used to fetch the value as fetchone returns tuple
        new_status = 1 if curr_status == 0 else 0
        c.execute('UPDATE tasks SET status = ? WHERE id = ? ',(new_status,task_id))
        conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/delete' , methods = ['POST'])
def delete():
    task_id = request.form['task_id']
    conn = sq.connect('todo.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?',(task_id,))
    c.execute('SELECT COUNT(*) FROM tasks')
    count = c.fetchone()[0]
    if count==0:
        c.execute("DELETE FROM sqlite_sequence WHERE name='tasks';")
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run( debug = True )



    

