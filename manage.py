import os, sys
from flask_script import Manager, Server
from webapp import create_app
from webapp.models import mongo
from webapp.models import Project
from webapp.controllers.tasks import port_scanner as ps
from webapp.extensions import celery, redis_store

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('webapp.config.%sConfig' % env.capitalize())

manager = Manager(app)
manager.add_command("server", Server(host="test"))

@manager.shell
def make_shell_context():
	return dict(
		app=app,
		mongo=mongo,
		Project=Project,
		ps=ps,
		celery=celery,
		redis=redis_store
	)

if __name__ == '__main__':
	# print sys.argv
	if len(sys.argv) == 1:
		sys.argv.append('server')

	manager.run()