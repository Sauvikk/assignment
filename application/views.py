from application import app, db, lm
from flask import render_template, request,url_for, redirect, g, flash, after_this_request
from .forms import RegisterForm, LoginForm, FileUploadForm, FibonacciForm
from .models import User
from datetime import datetime
import re
from flask.ext.login import login_user , logout_user , current_user , login_required


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        registered_user = form.validate_on_submit()
        if registered_user is False:
            return render_template('login.html', title='Login', form=form)
        else:
            login_user(registered_user)
            flash('Logged in successfully')
            return redirect(request.args.get('next') or url_for('home'))
    elif request.method == 'GET':
        return render_template('login.html', title='Login', form=form)


@app.route('/home')
@login_required
def home():
    return render_template('home.html', user=g.user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        if form.validate_on_submit() is False:
            return render_template('register.html', form=form)
        else:
            new_user = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('User successfully registered')
            return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('register.html', form=form)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=g.user)


@app.route('/fileUpload', methods=['GET', 'POST'])
@login_required
def fileUpload():
    form = FileUploadForm()
    if request.method == 'POST':
        file = request.files['file']
        if file:
            if file.filename.split('.')[1] == 'txt':
                show = form.showFile.data
                data = file.read().decode("utf-8")
                lc = len(data.split('\n'))
                cc = len(re.findall('[a-zA-Z]', data))
                wc = len(re.findall(r'\w+', data))
                return render_template('upload_file.html', user=g.user, form=form, lc=lc, cc=cc, wc=wc, data=data, show=show)
            else:
                flash("Please upload a text file (.txt)")
                return render_template('upload_file.html', user=g.user, form=form)
        else:
            flash("Upload a valid file")
            return render_template('upload_file.html', user=g.user, form=form)
    else:
        return render_template('upload_file.html', user=g.user, form=form)


@app.route('/fibonacci', methods=['GET', 'POST'])
@login_required
def fibonacci():
    form = FibonacciForm()
    if request.method == 'POST':
        if form.validate_on_submit() is False:
            return render_template('fibonacci.html', user=g.user, form=form)
        n = form.number.data
        output = fibo(int(n))
        return render_template('fibonacci.html', user=g.user, form=form, output=output)
    else:
        return render_template('fibonacci.html', user=g.user, form=form)


def fibo(n):
    a, b = 0, 1
    result = [0]
    for _ in range(n-1):
        a, b = b, a + b
        result.append(a)
    return result


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@lm.user_loader
def load_user(uid):
    return User.query.get(int(uid))


# Middleware
@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        @after_this_request
        def attach_cookie(response):
            val = datetime.utcnow()
            print('set cookie')
            response.set_cookie('last_access_t', value=str(val))
            return response





