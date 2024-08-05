from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField,SelectField, SubmitField
from wtforms.validators import DataRequired, URL, Regexp
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-secret-key'
Bootstrap5(app)

class CafeForm(FlaskForm):
    cafe = StringField('Cafe Name', validators=[DataRequired()])
    cafe_location = StringField('Cafe Google Maps Location', validators=[DataRequired(), URL(message="Please enter a valid Google Maps location!")])
    opening_time = StringField('Opening Time', validators=[DataRequired(), Regexp(regex=r'^(0?[1-9]|1[0-2]):[0-5][0-9](?::[0-5][0-9])?\s?(AM|PM)$', message="Please use a 12-hour format with AM or PM")])
    closing_time = StringField('Closing Time', validators=[DataRequired(), Regexp(regex=r'^(0?[1-9]|1[0-2]):[0-5][0-9](?::[0-5][0-9])?\s?(AM|PM)$', message="Please use a 12-hour format with AM or PM")])
    coffee_rating = SelectField('Coffee Rating', validators=[DataRequired()], choices=['☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'])
    wifi = SelectField('WiFi Availability', validators=[DataRequired()],
                                choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'])
    power = SelectField('Power Availability', validators=[DataRequired()],
                       choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe = form.cafe.data
        cafe_location = form.cafe_location.data
        opening_time = form.opening_time.data
        closing_time = form.closing_time.data
        coffee_rating = form.coffee_rating.data
        wifi = form.wifi.data
        power = form.power.data

        with open(r'cafe-data.csv', 'a', encoding="utf-8", newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([cafe, cafe_location, opening_time, closing_time, coffee_rating, wifi, power])
        return render_template("index.html")

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run()
