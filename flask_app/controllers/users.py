from flask_app import app, render_template, redirect, request, session, flash, bcrypt
from flask_app.models.user import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register_user')
def register_user():
    return render_template('register.html')

#REGISTER
@app.route('/register', methods=['POST'])
def register():
    #validate user
    if not User.validate_user(request.form):
        return redirect('/')

    #hash the password
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])

    #save the user to the DB
    temp_user = {
        'user_name':request.form['user_name'],
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':hashed_pw
    }
    user = User.save(temp_user)

    #log them in
    session['user_id'] = user
    session['first_name'] = request.form['first_name']

    return redirect('/mycookbook')

#LOGIN
@app.route('/login', methods=['POST'])
def login():
    #see if the email is in the DB
    user = User.find_by_email(request.form['email'])
    if not user:
        flash("Invalid credentials")
        return redirect('/')
    #see if the password is correct
    password_valid = bcrypt.check_password_hash(user.password,request.form['password'])
    if not password_valid:
        flash("Invalid credentials")
        return redirect('/')
        #log them in
    session['user_id']=user.id
    session['first_name']=user.first_name
    session['last_name']=user.last_name
    
    return redirect('/mycookbook')

#LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')