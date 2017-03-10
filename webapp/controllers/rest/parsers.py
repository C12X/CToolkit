from flask_restful import reqparse

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
project_get_parser = reqparse.RequestParser()
project_get_parser.add_argument(
	'limit',
	type=int,
	required=False)
project_post_parser = reqparse.RequestParser()
project_post_parser.add_argument(
	'project_name',
	type=str,
	required=True)

#TaskApi
task_post_parser = reqparse.RequestParser()
task_post_parser.add_argument(
	'type',
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