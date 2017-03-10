from flask_wtf import Form, RecaptchaField
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL

class scan_port_target(Form):
	pass