from flask import (
	Blueprint,
	render_template)

note_blueprint = Blueprint(
	'note',
	__name__,
	template_folder='../templates/note',
	url_prefix='/note')

@note_blueprint.route('/')
def overview():
	return render_template('note_overview.html')