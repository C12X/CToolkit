from flask import abort
from flask_restful import (
	Resource,
	fields,
	marshal_with)
from .parsers import post_get_parser, post_post_parser, post_put_parser

post_fields = {
	'title': fields.String(),
	'text': fields.String(),
	'publish_date': fields.DateTime(dt_format='iso8601')
}

#path: /api/post
class PostApi(Resource):
	def get(self, post_id=None):
		if post_id:
			return {'post_id': post_id}
		else:
			args = post_get_parser.parse_args()
			return args
	
	def post(self, post_id=None):
		if post_id:
			return {'test':'test'}
		else:
			args = post_post_parser.parse_args()
			return args

	def put(self, post_id=None):
		if post_id:
			return {'test':'test'}
		else:
			args = post_put_parser.parse_args()
			return args

#path: /api/task /api/task
class task_status(Resource):
	def get(self, task_id=None):
		if task_id:
			return {'task_id': task_id}
		return {'Error': 'task_id is required'}