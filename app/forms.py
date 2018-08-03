from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired
import work

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class MerchantForm(FlaskForm):
    starting_position = SelectField('Starting island', choices=[(x.name, x.name) for x in work.getIslandList()],
                                    validators=[DataRequired()])
    destination = SelectField('Destination island', choices=[(x.name, x.name) for x in work.getIslandList()],
                              validators=[DataRequired()])
    pig_bool = BooleanField('Pigs')
    chicken_bool = BooleanField('Chickens')
    snake_bool = BooleanField('Snakes')
    gunpowder_bool = BooleanField('Gunpowder')
    submit = SubmitField('Go!')

