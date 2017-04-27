from flask_restful import Resource
from .parsers import task_get_parser
from .parsers import task_post_parser
from webapp.models import Project
from webapp.models import Task
from webapp.extensions import celery
from webapp.extensions import redis_store
from webapp.controllers.tasks import port_scanner
from webapp.process.xml_to_dict import xmltodict
import datetime

class TaskApi(Resource):
	def get(self, task_id=None):
		if task_id:
			args = task_get_parser.parse_args()
			if args.get('process'):
				stdout = redis_store.hget('task_stdout',task_id).decode('utf-8').strip()
				return {'process': stdout}
			task = Task.objects(id=task_id).first()
			if not task.result:
				result = celery.AsyncResult(task.celery_id).get()
				if 'path' in result.keys():
					# task.result = {'path':result['path'],'raw':open(result['path']).read()}
					# read the nmap output xml and save useful data into mongodb
					task.result = xmltodict(result['path'])
				else:
					task.result = result
				task.save()
			return {'task_id':str(task.id), 'task_result':task.result}
		else:
			args = task_get_parser.parse_args()
			# specified project
			if args.project_id:
				tasks = Task.objects(project=args.project_id).order_by('-date_created').paginate(1,10).items
			# all projects
			else:
				tasks = Task.objects.order_by('-date_created').all()
			# format output
			task_list = []
			for i in tasks:
				# li => list item
				li = {}
				li['task_id'] = str(i.id)
				li['task_category'] = i.category
				li['date_created'] = i.date_created.strftime('%Y-%m-%d %H:%M:%S')
				li['task_target'] = i.target
				if i.status != 'SUCCESS':
					i.status = celery.AsyncResult(i.celery_id).status
					i.save()
				li['task_status'] = i.status
				task_list.append(li)

			return task_list

	def post(self, task_id=None):
		if task_id:
			return {'error':'illegal param'}
		else:
			#args: category, target, level, project_id
			args = task_post_parser.parse_args()

			#category: 0-portscanner, 1-webdirburp, 2-subdomain
			task = Task()
			task.category = args.category
			task.target = args.target
			task.date_created = datetime.datetime.now()
			task.project = Project.objects(id=args.project_id).first()
			task.save(write_concern={"w":1, "j":True})

			if args.category == 0:
				celery_task = port_scanner.run_nmap.apply_async([args.target, str(task.id), args.level])
			elif args.category == 1:
				celery_task = port_scanner.scan.apply_async([args.target])
			elif args.category ==2:
				celery_task = port_scanner.scan.apply_async([args.target])
			# after above, create a celery task with celery_task.id

			task.celery_id = celery_task.id
			# task.status = celery_task.status
			task.save(write_concern={"w":1, "j":True})
			return {'celery_id':task.celery_id,'task_category':task.category, 'task_target':task.target, 'task_status':task.status, 'date_created':task.date_created.strftime('%Y-%m-%d %H:%M:%S'),'task_id':str(task.id)}

	def delete(self, task_id=None):
		if not task_id:
			return {'error':'illegal param'}
		else:
			task = Task.objects(id=task_id).first()
			task.delete()
			return {'task_id':task_id}