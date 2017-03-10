from flask import (
	Blueprint,
	request,
	jsonify,
	render_template)

home_blueprint = Blueprint(
	'home',
	__name__,
	template_folder='../templates/home',
	url_prefix='/home')

@home_blueprint.route('/')
def index():
	return render_template('home.html')