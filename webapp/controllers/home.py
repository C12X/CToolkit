from flask import (
	Blueprint,
	render_template)

home_blueprint = Blueprint(
	'home',
	__name__,
	template_folder='../templates/home',
	url_prefix='/home')

@home_blueprint.route('/')
def index():
	with open('README.md','rb') as f:
		readme = f.read()
	return render_template('home.html',readme=readme.decode('utf-8'))