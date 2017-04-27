from flask_restful import reqparse
from werkzeug import datastructures

post_get_parser = reqparse.RequestParser()
post_get_parser.add_argument(
	'page',
	type=int,
	location=['args', 'headers'])

post_post_parser = reqparse.RequestParser()
post_post_parser.add_argument(
	'post1',
	type=int,
	required=True,
	help='post1 is required')
post_post_parser.add_argument(
	'post2',
	type=str)

post_put_parser = reqparse.RequestParser()
post_put_parser.add_argument(
	'put',
	type=str,
	help="put is required",
	required=True)
# above all are test

#ProjectApi
#get method
project_get_parser = reqparse.RequestParser()
#post method
project_post_parser = reqparse.RequestParser()
project_post_parser.add_argument(
	'project_name',
	type=str,
	required=True)

#TaskApi
#get method
task_get_parser = reqparse.RequestParser()
task_get_parser.add_argument(
	'project_id',
	type=str)
task_get_parser.add_argument(
	'process',
	type=bool,
	default=False)
#post method
task_post_parser = reqparse.RequestParser()
task_post_parser.add_argument(
	'category',
	type=int,
	required=True)
task_post_parser.add_argument(
	'target',
	type=str,
	required=True)
task_post_parser.add_argument(
	'level',
	type=int,
	required=True)
task_post_parser.add_argument(
	'project_id',
	type=str,
	required=True)

#VulnApi
#get method
#post method
vuln_post_parser = reqparse.RequestParser()
vuln_post_parser.add_argument(
	'title',
	type=str,)
#put method
vuln_put_parser = reqparse.RequestParser()
vuln_put_parser.add_argument(
	'exp_index',
	type=int,)
vuln_put_parser.add_argument(
	'exp_title',
	type=str,)
vuln_put_parser.add_argument(
	'method',
	type=str,
	choices=['get','post','file'],
	required=True)
vuln_put_parser.add_argument(
	'target',
	type=str,
	required=True)
vuln_put_parser.add_argument(
	'payload',
	type=str)
vuln_put_parser.add_argument(
	'cookie',
	type=str)
vuln_put_parser.add_argument(
	'user_agent',
	type=str)
vuln_put_parser.add_argument(
	'content_type',
	type=str)
vuln_put_parser.add_argument(
	'proxy',
	type=str)
vuln_put_parser.add_argument(
	'file',
	type=datastructures.FileStorage,
	location='files')
vuln_put_parser.add_argument(
	'save',
	type=bool,
	default=False)
#delete method
vuln_delete_parser = reqparse.RequestParser()
vuln_delete_parser.add_argument(
	'exp_index',
	type=int,
	required=True)

# #FileApi
# file_get_parser = reqparse.RequestParser()
# file_post_parser = reqparse.RequestParser()
# file_put_parser = reqparse.RequestParser()
# file_delete_parser = reqparse.RequestParser()

#NoteApi
#get method
note_get_parser = reqparse.RequestParser()
note_get_parser.add_argument(
	'code',
	type=bool,
	default=False)
#post method
note_post_parser = reqparse.RequestParser()
note_post_parser.add_argument(
	'title',
	type=str,
	required=True)
#put method
note_put_parser = reqparse.RequestParser()
note_put_parser.add_argument(
	'code',
	type=str,
	required=True)
#delete method
note_delete_parser = reqparse.RequestParser()