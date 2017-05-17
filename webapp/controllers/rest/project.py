from flask_restful import Resource
from .parsers import project_get_parser, project_post_parser
from webapp.models import Project
import datetime

class ProjectApi(Resource):

	def get(self, project_id=None):
		# specific id, return itself
		if project_id:
			project = Project.objects(id=project_id).first_or_404()
			return {'id':str(project.id), 'project_name':project.project_name}
		# without id, return top 10
		projects = Project.objects.order_by('-date_created').all()
		return [{'project_id':str(i.id),'project_name':i.project_name,'date_created':i.date_created.strftime('%Y-%m-%d %H:%M:%S')} for i in projects]

	def post(self, project_id=None):
		# specific id, illegal
		if project_id:
			return {'error':'illegal param'}
		# create new project and return id
		args = project_post_parser.parse_args()
		project = Project()
		project.project_name = args['project_name']
		project.date_created = datetime.datetime.now()
		project.save(write_concern={"w":1, "j":True})
		return {'id':str(project.id)}

	def put(self, project_id=None):
		if project_id:
			return {}

	def delete(self, project_id=None):
		if not project_id:
			return {'error':'illegal param'}
		else:
			project = Project.objects(id=project_id).first()
			project.delete()
			return {'project_id':project_id}