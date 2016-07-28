from application import app, db
from flask import render_template, request, session, url_for, redirect
from .forms import SignupForm, SigninForm, FileUpload, FibonacciForm
from .models import User
import re


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/test_db')
def test_db():
    if db.session.query("1").from_statement("SELECT 1").all():
        return 'It works.'
    else:
        return 'Something is broken.'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if 'email' in session:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        if form.validate() is False:
            return render_template('signup.html', form=form)
        else:
            new_user = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = new_user.email
            return redirect(url_for('profile'))

    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.route('/profile')
def profile():
    if 'email' not in session:
        return redirect(url_for('signin'))
    user = User.query.filter_by(email = session['email']).first()
    if user is None:
        return redirect(url_for('signin'))
    else:
        return render_template('profile.html')


@app.route('/fileUpload', methods=['GET', 'POST'])
def fileUpload():
    # if 'email' not in session:
    #     return redirect(url_for('signin'))
    form = FileUpload()
    if request.method == 'POST':
        file = request.files['file']
        if file:
            data = file.read().decode("utf-8")
            lc = len(data.split('\n'))
            cc = len(re.findall('[a-zA-Z]', data))
            wc = len(re.findall(r'\w+', data))
            return render_template('upload_file.html', form=form, lc=lc, cc=cc, wc=wc, data=data)
    else:
        return render_template('upload_file.html', form=form)


@app.route('/fibonacci', methods=['GET', 'POST'])
def fibonacci():
    # if 'email' not in session:
    #     return redirect(url_for('signin'))
    form = FibonacciForm()
    if request.method == 'POST':
        n = form.number.data
        output = fibo(int(n))
        return render_template('fibonacci.html', form=form, output=output)
    else:
        print('here')
        return render_template('fibonacci.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if 'email' in session:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        if form.validate() is False:
            return render_template('signin.html', form=form)
        else:
            session['email'] = form.email.data
            return redirect(url_for('profile'))

    elif request.method == 'GET':
        return render_template('signin.html', form=form)


@app.route('/signout')
def signout():
    if 'email' not in session:
        return redirect(url_for('signin'))

    session.pop('email', None)
    return redirect(url_for('home'))


def fibo(n):
    a, b = 0, 1
    result = [0]
    for _ in range(n-1):
        a, b = b, a + b
        result.append(a)
    return result



