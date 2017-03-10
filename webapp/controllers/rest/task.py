from flask_restful import Resource
from .parsers import task_post_parser
from webapp.models import Task
from webapp.controllers.tasks import port_scanner

class TaskApi(Resource):
	def get(self, task_id=None):
		if task_id:
			return {'task_id':task_id}
		else:
			# return [{'task_id':'task_id_1'},{'task_id':'task_id_2'}]
			result = port_scanner.test.delay()
			return result

	def post(self, task_id=None):
		if task_id:
			return {'error':'illegal param'}
		else:
			args = task_post_parser.parse_args()
			task = {}[args.type]
			return args