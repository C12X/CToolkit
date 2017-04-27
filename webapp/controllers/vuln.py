from flask import (
	Blueprint,
	request,
	jsonify,
	render_template)

vuln_blueprint = Blueprint(
	'vuln',
	__name__,
	template_folder='../templates/vuln',
	url_prefix='/vuln')

@vuln_blueprint.route('/')
def overview():
	return render_template('vuln_overview.html')

@vuln_blueprint.route('/<vuln_title>')
def custom(vuln_title):
	return render_template('vuln_custom.html')