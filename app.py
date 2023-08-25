from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, current_user, LoginManager, logout_user, UserMixin, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo
from sqlalchemy.sql.expression import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['WEATHER_API_KEY'] = '06d4370f849007b44929f69c1e87dc5b'
app.config['CITY'] = None

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.secret_key = 'gianluca_secret'

login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_weather(city):
    num_days = 4
    api_key = app.config['WEATHER_API_KEY']
    base_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&cnt={num_days*8}'
    response = requests.get(base_url)
    data = response.json()
    forecast = []
    for i in range(0, num_days * 8 , 8):
        day_data = data['list'][i]
        date = day_data['dt_txt']
        temp = day_data['main']['temp']
        description = day_data['weather'][0]['description']
        
        forecast.append({'date': date, 'temp': temp, 'description': description})
    return forecast

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    score = db.Column(db.Integer, default=0)

    def is_active(self):
        return True

    def get_id(self):
        return self.id

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)
    options = db.relationship('Option', back_populates='quiz')
    
class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)   
    correct = db.Column(db.Boolean, nullable=False, default=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    quiz = db.relationship('Quiz', back_populates='options')

@app.route('/')
def home():
    city = request.args.get('city') 
    weather_data = None
    if city:
        app.config['CITY'] = city
    if app.config['CITY']:
        weather_data = get_weather(city)
    return render_template('home.html', weather_data=weather_data)


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

class QuizForm(FlaskForm):
    submit = SubmitField('Submit')

def generate_quiz_form(questions):
    class GeneratedQuizForm(QuizForm):
        pass

    for question in questions:
        choices = [(str(option.id), option.text) for option in question.options]
        setattr(
            GeneratedQuizForm,
            str(question.id),
            RadioField(
                question.text,
                choices=choices,
                validators=[DataRequired()],
            ),
        )

    return GeneratedQuizForm()

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    questions = Quiz.query.order_by(func.random()).all()
    form = generate_quiz_form(questions)

    if form.validate_on_submit():
        score = 0  # Inizializza il punteggio dell'utente

        for question in questions:
            selected_option_id = int(getattr(form, str(question.id)).data)
            selected_option = Option.query.get(selected_option_id)
            if selected_option.correct :
                score += 1

        current_user.score += score
        db.session.commit()
        flash(f'You scored {score} points!', 'success')
        return redirect(url_for('home'))
    return render_template('quiz.html', form=form)

@app.route('/leaderboard')
def leaderboard():
    # Implement leaderboard logic here
    return render_template('leaderboard.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
