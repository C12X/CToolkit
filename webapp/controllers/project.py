from flask import (
	Blueprint,
	render_template)

project_blueprint = Blueprint(
	'project',
	__name__,
	template_folder='../templates/project',
	url_prefix='/project')

@project_blueprint.route('/')
def overview():
	return render_template('project_overview.html')

@project_blueprint.route('/<project_id>')
def project(project_id):
	return render_template('project_detail.html')