from flask import (
	Blueprint,
	request,
	jsonify,
	render_template)

project_blueprint = Blueprint(
	"project",
	__name__,
	template_folder='../templates/project',
	url_prefix="/project")

@project_blueprint.route('/')
def overview():
	return render_template('project_overview.html')

@project_blueprint.route('/<project_id>')
def project(project_id):
	return render_template('project_detail.html')

@project_blueprint.route('/overview')
def host_list():
	host = request.args.get('host',None)
	return jsonify({"host":host})

@project_blueprint.route('/dir')
def path_over():
	return "dir"