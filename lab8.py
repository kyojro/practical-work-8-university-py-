from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired
import requests, json, os

download_folder = os.path.expanduser(r'~\Downloads')
download_folder = r'D:\\'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'passwordispassword'
Bootstrap(app)

class RegisterForm(FlaskForm):
    first_name = StringField("first_name", validators=[InputRequired()], render_kw={"placeholder": "Ім'я"})
    second_name = StringField("second_name", validators=[InputRequired()], render_kw={"placeholder": "Прізвище"})
    age = StringField("age", validators=[InputRequired()], render_kw={"placeholder": "Вік"})
    country  = StringField("country", validators=[InputRequired()],render_kw={"placeholder": "Країна"})
    city = StringField("city", validators=[InputRequired()], render_kw={"placeholder": "Місто"})
    def clear(self):
        self.first_name.data = ""
        self.second_name.data = ""
        self.age.data = ""
        self.country.data = ""
        self.city.data = ""


def get_currency():
    return requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json').json()

def get_currency_to_date(date):
    return requests.get(f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date={date}&json').json()


@app.route('/')
def index():
    return render_template('index.html')

    
@app.route('/Currency')
def currency():
    return render_template('currency.html', data = get_currency())

@app.route('/Currency/<date>')
def currency_to_date(date):
    return render_template('currency.html', data = get_currency_to_date(date))

@app.route('/Currency/Choose', methods=['GET', 'POST'])
def currency_choose_date():
    if request.method == "POST":
        print(request.form["dateform"])
        return redirect(url_for('currency_to_date', date = request.form["dateform"] ))
    return render_template('choose.html')

@app.route('/Registration' , methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        path = f"{download_folder}\{form.first_name.data}_{form.second_name.data}.txt"
        with open(path, 'w') as file:
            file.write(f"{form.first_name.data} {form.second_name.data}\n{form.age.data}\n{form.country.data}, {form.city.data}")
    form.clear()

    return render_template('registration.html', form = form)




if __name__ == "__main__":
    app.run()