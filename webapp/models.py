from flask_mongoengine import MongoEngine
mongo = MongoEngine()

class Project(mongo.Document):
	project_name = mongo.StringField(required=True)
	date_created = mongo.DateTimeField(required=True)

class Task(mongo.Document):
	date_created = mongo.DateTimeField(required=True)
	category = mongo.IntField(required=True)
	target = mongo.StringField(required=True)
	project = mongo.ReferenceField(Project,required=True)
	# celery task info
	celery_id = mongo.StringField()
	status = mongo.StringField(default='PENDING')
	result = mongo.ListField(default=[])

class Vuln(mongo.Document):
	date_created = mongo.DateTimeField(required=True)
	title = mongo.StringField(required=True, unique=True)
	exploits = mongo.ListField(default=[])

class Note(mongo.Document):
	date_created = mongo.DateTimeField(required=True)
	title = mongo.StringField(required=True)
	code = mongo.StringField(default='')
	parent = mongo.ReferenceField('self',default=None)
	has_child = mongo.BooleanField(default=False)