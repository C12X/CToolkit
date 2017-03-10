from flask import (
	Blueprint,
	request,
	jsonify,
	render_template)

scan_blueprint = Blueprint(
	"scan",
	__name__,
	template_folder='../templates/scan',
	url_prefix="/scan")

@scan_blueprint.route('/')
def index():
	return render_template('404.html')

@scan_blueprint.route('/port')
def port_scan():
	host = request.args.get('host',None)
	return jsonify({"host":host})

@scan_blueprint.route('/dir')
def path_scan():
	return "dir"