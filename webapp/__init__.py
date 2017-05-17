from flask import(
	Flask,
	render_template,
	redirect,
	url_for,
	flash)
from .models import mongo
from .extensions import(
	rest_api,
	celery,
	redis_store)
from .controllers.home import home_blueprint
from .controllers.project import project_blueprint
from .controllers.vuln import vuln_blueprint
from .controllers.note import note_blueprint

from .controllers.rest.project import ProjectApi
from .controllers.rest.task import TaskApi
from .controllers.rest.vuln import VulnApi
from .controllers.rest.note import NoteApi

def create_app(object_name):
	app = Flask(__name__)
	app.config.from_object(object_name)

	#database
	mongo.init_app(app)

	#redis
	redis_store.init_app(app)

	#blueprint
	app.register_blueprint(home_blueprint)
	app.register_blueprint(project_blueprint)
	# app.register_blueprint(scan_blueprint)
	app.register_blueprint(vuln_blueprint)
	app.register_blueprint(note_blueprint)

	#restful
	rest_api.add_resource(
		ProjectApi,
		'/api/project/',
		'/api/project/<project_id>',
		endpoint='api.project')
	rest_api.add_resource(
		TaskApi,
		'/api/task/',
		'/api/task/<task_id>',
		endpoint='api.task')
	rest_api.add_resource(
		VulnApi,
		'/api/vuln/',
		'/api/vuln/<title>',
		endpoint='api.vuln')
	rest_api.add_resource(
		NoteApi,
		'/api/note/',
		'/api/note/<note_id>',
		endpoint='api.note')
	rest_api.init_app(app)

	#celery
	celery.init_app(app)

	@app.route('/')
	def index():
		return redirect(url_for('home.index'))

	@app.route('/test')
	def test():
		return render_template('test.html')
	# @app.route('/home')
	# def home():
	# 	return render_template('frame.html')

	return app

if __name__ == '__main__':
	app.run()