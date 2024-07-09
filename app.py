from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB connection
try:
    client = pymongo.MongoClient('localhost', 27017)
    db = client['iw_DATABASE']
    users = db['users']
    tasks = db['tasks']
    categories = db['categories']
    print("Connected to MongoDB")
except pymongo.errors.ConnectionFailure as ex:
    print("Failed to connect to MongoDB:", ex)
    exit(1)

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        users.insert_one({'username': username, 'email': email, 'password': hashed_password})
        return redirect(url_for('login'))
    return render_template('register.html')

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('login.html')

# User Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# User Profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    user = users.find_one({'username': username})
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_email = request.form['new_email']
        new_password = request.form['new_password']
        if new_username and new_username != username:
            users.update_one({'username': username}, {'$set': {'username': new_username}})
            tasks.update_many({'username': username}, {'$set': {'username': new_username}})
            categories.update_many({'username': username}, {'$set': {'username': new_username}})
            session['username'] = new_username
        if new_email:
            users.update_one({'username': session['username']}, {'$set': {'email': new_email}})
        if new_password:
            hashed_password = generate_password_hash(new_password)
            users.update_one({'username': session['username']}, {'$set': {'password': hashed_password}})
        return redirect(url_for('profile'))
    return render_template('profile.html', user=user)

# Home Page
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    user_tasks = tasks.find({'username': username})
    user_categories = categories.find({'username': username})
    return render_template('index.html', tasks=user_tasks, categories=user_categories)

# Add Task
@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_categories = list(categories.find({'username': session['username']}))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        priority = request.form.get('priority')
        due_date = request.form.get('due_date')
        
        if not title or not category or not priority or not due_date:
            flash("All fields except description are required", "danger")
            return redirect(url_for('add_task'))
        
        tasks.insert_one({
            'username': session['username'], 
            'title': title, 
            'description': description,
            'category': category, 
            'priority': priority,
            'due_date': due_date,
            'status': 'to do'
        })
        return redirect(url_for('index'))
    
    return render_template('add_task.html', categories=user_categories)

# Update Task Status
@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    status = request.form['status']
    tasks.update_one({'_id': ObjectId(task_id)}, {'$set': {'status': status}})
    return redirect(url_for('index'))

# Add Category
@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        category = request.form.get('category')
        if category:
            categories.insert_one({'username': session['username'], 'category': category})
            flash('Category added successfully', 'success')
            return redirect(url_for('add_task'))
        else:
            flash('Category name cannot be empty', 'danger')
    return render_template('add_category.html')


# Filter Tasks
@app.route('/filter_tasks', methods=['GET', 'POST'])
def filter_tasks():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    query = {'username': username}
    if request.method == 'POST':
        category = request.form['category']
        status = request.form['status']
        priority = request.form['priority']
        if category:
            query['category'] = category
        if status:
            query['status'] = status
        if priority:
            query['priority'] = priority
    filtered_tasks = tasks.find(query)
    user_categories = categories.find({'username': username})
    return render_template('index.html', tasks=filtered_tasks, categories=user_categories)

if __name__ == '__main__':
    app.run(debug=True)
